# RESO ERD Generator

**Version:** 1.1.0  
**Author:** Dan Troup | CEO | Broker Public Portal

A simple Python script that generates a Mermaid Entity Relationship Diagram (ERD) from the RESO Data Dictionary, showing only primary keys and foreign keys with their relationships.

## What it does

- Fetches data from the official RESO Data Dictionary spreadsheet
- Extracts primary keys from the RESO XML schema
- Generates a clean Mermaid ERD with 41 entities, their keys, and relationships
- Shows 14 relationships between entities

## Files

- `reso_erd.py` - Main Python script
- `reso_erd.md` - Generated Mermaid ERD (full version)
- `reso_erd_no_orphans.md` - Generated Mermaid ERD (without orphaned entities)
- `requirements.txt` - Python dependencies

## Setup

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the script:
   ```bash
   # Generate full ERD with all entities
   python3 reso_erd.py
   
   # Generate ERD without orphaned entities (entities with no relationships)
   python3 reso_erd.py --no-orphans
   ```

3. View the generated ERD:
   - Open `reso_erd.md` to see the full Mermaid diagram (41 entities)
   - Open `reso_erd_no_orphans.md` to see the filtered diagram (21 entities)
   - Copy the Mermaid code to any Mermaid viewer (GitHub, Mermaid Live Editor, etc.)

## Output

The script generates two versions:

### Full ERD (`reso_erd.md`)
- **41 entities** with primary keys and foreign keys
- **14 relationships** showing connections between tables
- **20 orphaned entities** (entities with no relationships)

### Filtered ERD (`reso_erd_no_orphans.md`)
- **21 entities** with relationships only
- **14 relationships** showing connections between tables
- **No orphaned entities** for cleaner visualization

Both versions use **clean Mermaid syntax** ready for visualization.

## Data Sources

- **Spreadsheet**: RESO Data Dictionary (Google Sheets)
- **XML Schema**: RESO XML with primary key definitions
- **All data is official** from RESO Standards Organization

## Example Output

The generated ERD shows entities like:
- `Property` with `ListingKey` PK and 12 foreign keys
- `Contacts` with `ContactKey` PK and 3 foreign keys  
- `Association` with `AssociationKey` PK and 0 foreign keys (standalone)
- Relationships like `ContactListings` → `Property` (via Listing FK)

## Requirements

- Python 3.6+
- Internet connection (to fetch RESO data)
- Dependencies listed in `requirements.txt`
