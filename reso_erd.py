#!/usr/bin/env python3
"""
RESO Simple ERD Generator
Version: 1.1.0
Author: Dan Troup | CEO | Broker Public Portal

Creates a clean Mermaid ERD with only primary keys and foreign keys.

Dependencies:
- requests>=2.28.0
- pandas>=1.5.0

Data Sources:
- RESO Data Dictionary Spreadsheet: https://docs.google.com/spreadsheets/d/1eOB4Nv3wrAayB1av7n2AWPBRWDeB-UkiDa8h8cdsIEI/edit?gid=1912290910#gid=1912290910
- RESO XML Schema: https://raw.githubusercontent.com/RESOStandards/web-api-commander/refs/heads/main/src/main/resources/RESODataDictionary-2.0.xml

Usage:
    python3 reso_erd.py [--no-orphans]
    
Options:
    --no-orphans    Exclude entities with no relationships (orphaned entities)

Output:
    reso_erd.md - Generated Mermaid ERD with 41 entities and 14 relationships
    reso_erd_no_orphans.md - ERD without orphaned entities (when --no-orphans is used)
"""

import requests
import pandas as pd
import io
import re
import argparse
from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class Field:
    name: str
    is_primary_key: bool = False
    is_foreign_key: bool = False
    target_resource: Optional[str] = None

@dataclass
class Entity:
    name: str
    primary_key: str
    foreign_keys: List[Field]

class RESOSimpleERD:
    def __init__(self, exclude_orphans=False):
        self.entities = {}
        self.exclude_orphans = exclude_orphans
        
    def fetch_data(self):
        """Fetch data from RESO Data Dictionary"""
        print("Fetching RESO Data Dictionary...")
        
        # Fetch spreadsheet data
        sheet_id = '1eOB4Nv3wrAayB1av7n2AWPBRWDeB-UkiDa8h8cdsIEI'
        gid = '1912290910'
        url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}'
        
        response = requests.get(url)
        self.df = pd.read_csv(io.StringIO(response.text))
        print(f"Loaded {len(self.df)} rows from spreadsheet")
        
        # Fetch XML data for primary keys
        xml_url = 'https://raw.githubusercontent.com/RESOStandards/web-api-commander/refs/heads/main/src/main/resources/RESODataDictionary-2.0.xml'
        xml_response = requests.get(xml_url)
        self.xml_text = xml_response.text
        print("Loaded XML data")
        
    def extract_primary_keys(self):
        """Extract primary keys from XML using regex"""
        primary_keys = {}
        
        # Use regex to find EntityType and Key patterns
        # Pattern: <EntityType Name="ResourceName">...<Key><PropertyRef Name="PrimaryKeyName" /></Key>...
        pattern = r'<EntityType Name="([^"]*)">.*?<Key><PropertyRef Name="([^"]*)" /></Key>'
        
        matches = re.findall(pattern, self.xml_text, re.DOTALL)
        
        for entity_name, primary_key in matches:
            primary_keys[entity_name] = primary_key
        
        return primary_keys
    
    def process_entities(self):
        """Process all entities from the spreadsheet"""
        print("\nProcessing entities...")
        
        # Get primary keys from XML
        primary_keys = self.extract_primary_keys()
        print(f"Found {len(primary_keys)} primary keys from XML")
        
        # Get unique resources
        resources = self.df['ResourceName'].unique()
        
        for resource in resources:
            if pd.isna(resource):
                continue
                
            resource_data = self.df[self.df['ResourceName'] == resource]
            
            # Get primary key
            primary_key = primary_keys.get(resource, "Not found")
            
            # Process foreign keys only
            foreign_keys = []
            
            for _, row in resource_data.iterrows():
                field_name = str(row.get('StandardName', '')).strip()
                target_resource = row.get('TargetResourceKey', '')
                
                if not field_name or field_name == 'nan':
                    continue
                
                # Check if this is a foreign key
                is_foreign_key = pd.notna(target_resource) and str(target_resource).strip()
                
                if is_foreign_key:
                    field = Field(
                        name=field_name,
                        is_foreign_key=True,
                        target_resource=str(target_resource).strip()
                    )
                    foreign_keys.append(field)
            
            # Create entity
            entity = Entity(
                name=resource,
                primary_key=primary_key,
                foreign_keys=foreign_keys
            )
            
            self.entities[resource] = entity
            print(f"  {resource}: PK={primary_key}, FKs={len(foreign_keys)}")
    
    def generate_mermaid_erd(self) -> str:
        """Generate simple Mermaid ERD with only keys"""
        mermaid_lines = ["erDiagram"]
        
        # Filter entities if excluding orphans
        entities_to_process = self.entities
        if self.exclude_orphans:
            entities_to_process = self._get_connected_entities()
        
        # Generate entity definitions with only keys
        for entity_name, entity in entities_to_process.items():
            mermaid_lines.append(f"    {entity_name} {{")
            
            # Add primary key
            if entity.primary_key and entity.primary_key != "Not found":
                mermaid_lines.append(f"        string {entity.primary_key} PK")
            
            # Add foreign keys
            for fk in entity.foreign_keys:
                mermaid_lines.append(f"        string {fk.name} FK")
            
            mermaid_lines.append("    }")
            mermaid_lines.append("")
        
        # Generate relationships
        relationships = self._extract_relationships()
        for rel in relationships:
            mermaid_lines.append(f"    {rel}")
        
        return "\n".join(mermaid_lines)
    
    def _extract_relationships(self) -> List[str]:
        """Extract relationships for Mermaid ERD"""
        relationships = []
        
        # Create mapping from key names to entity names
        key_to_entity = {}
        for entity_name, entity in self.entities.items():
            if entity.primary_key and entity.primary_key != "Not found":
                key_to_entity[entity.primary_key] = entity_name
        
        for entity_name, entity in self.entities.items():
            for fk in entity.foreign_keys:
                if fk.target_resource and fk.target_resource in key_to_entity:
                    target_entity = key_to_entity[fk.target_resource]
                    # Create relationship line
                    rel = f"    {entity_name} ||--o{{ {target_entity} : \"{fk.name}\""
                    relationships.append(rel)
        
        return relationships
    
    def _get_connected_entities(self) -> Dict:
        """Get entities that have relationships (not orphaned)"""
        connected_entities = {}
        
        # Get all entities that are referenced by foreign keys
        referenced_entities = set()
        for entity in self.entities.values():
            for fk in entity.foreign_keys:
                if fk.target_resource:
                    # Find the entity that has this as primary key
                    for name, ent in self.entities.items():
                        if ent.primary_key == fk.target_resource:
                            referenced_entities.add(name)
                            break
        
        # Get all entities that have foreign keys (they reference others)
        entities_with_fks = set()
        for name, entity in self.entities.items():
            if entity.foreign_keys:
                entities_with_fks.add(name)
        
        # Connected entities are those that either reference others or are referenced
        connected_names = referenced_entities.union(entities_with_fks)
        
        for name in connected_names:
            if name in self.entities:
                connected_entities[name] = self.entities[name]
        
        return connected_entities
    
    def save_mermaid(self):
        """Save Mermaid diagram to file"""
        mermaid_content = self.generate_mermaid_erd()
        
        # Determine output filename
        if self.exclude_orphans:
            filename = 'reso_erd_no_orphans.md'
            title = "RESO Simple ERD (No Orphans)"
            description = "Mermaid ERD with only primary keys and foreign keys, excluding orphaned entities."
        else:
            filename = 'reso_erd.md'
            title = "RESO Simple ERD"
            description = "Mermaid ERD with only primary keys and foreign keys."
        
        with open(filename, 'w') as f:
            f.write(f"# {title}\n\n")
            f.write(f"{description}\n\n")
            f.write("```mermaid\n")
            f.write(mermaid_content)
            f.write("\n```\n")
        
        # Calculate stats
        entities_to_count = self.entities
        if self.exclude_orphans:
            entities_to_count = self._get_connected_entities()
        
        print(f"\n✅ Simple ERD saved to '{filename}'")
        print(f"📊 Total entities: {len(entities_to_count)}")
        print(f"🔑 Entities with PKs: {len([e for e in entities_to_count.values() if e.primary_key != 'Not found'])}")
        print(f"🔗 Total relationships: {len(self._extract_relationships())}")
        
        if self.exclude_orphans:
            orphaned_count = len(self.entities) - len(entities_to_count)
            print(f"🚫 Orphaned entities excluded: {orphaned_count}")
    
    def run(self):
        """Run the complete process"""
        self.fetch_data()
        self.process_entities()
        self.save_mermaid()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate RESO ERD with optional orphan exclusion')
    parser.add_argument('--no-orphans', action='store_true', 
                       help='Exclude entities with no relationships (orphaned entities)')
    
    args = parser.parse_args()
    
    generator = RESOSimpleERD(exclude_orphans=args.no_orphans)
    generator.run()
