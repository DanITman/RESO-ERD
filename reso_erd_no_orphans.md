# RESO Simple ERD (No Orphans)

Mermaid ERD with only primary keys and foreign keys, excluding orphaned entities.

```mermaid
erDiagram
    HistoryTransactional {
        string HistoryTransactionalKey PK
        string ChangedByMember FK
        string OriginatingSystem FK
        string SourceSystem FK
    }

    ContactListings {
        string ContactListingsKey PK
        string Contact FK
        string Listing FK
    }

    PropertyPowerProduction {
        string PowerProductionKey PK
        string Listing FK
    }

    Prospecting {
        string ProspectingKey PK
        string Contact FK
        string OwnerMember FK
        string SavedSearch FK
    }

    Queue {
        string QueueTransactionKey PK
        string OriginatingSystem FK
        string SourceSystem FK
    }

    ContactListingNotes {
        string ContactKey PK
        string Contact FK
    }

    Property {
        string ListingKey PK
        string BuyerAgent FK
        string BuyerOffice FK
        string BuyerTeam FK
        string CoBuyerAgent FK
        string CoBuyerOffice FK
        string CoListAgent FK
        string CoListOffice FK
        string ListAgent FK
        string ListOffice FK
        string ListTeam FK
        string OriginatingSystem FK
        string SourceSystem FK
    }

    Office {
        string OfficeKey PK
        string MainOffice FK
        string OfficeBroker FK
        string OfficeManager FK
        string OriginatingSystem FK
        string SourceSystem FK
    }

    InternetTracking {
        string EventKey PK
        string ActorOriginatingSystem FK
        string ActorSourceSystem FK
        string EventOriginatingSystem FK
        string EventSourceSystem FK
        string ObjectOriginatingSystem FK
        string ObjectSourceSystem FK
    }

    Rules {
        string RuleKey PK
        string OriginatingSystem FK
        string SourceSystem FK
    }

    SavedSearch {
        string SavedSearchKey PK
        string Member FK
        string OriginatingSystem FK
        string SourceSystem FK
    }

    PropertyUnitTypes {
        string UnitTypeKey PK
        string Listing FK
    }

    PropertyGreenVerification {
        string GreenBuildingVerificationKey PK
        string Listing FK
    }

    OpenHouse {
        string OpenHouseKey PK
        string Listing FK
        string OriginatingSystem FK
        string ShowingAgent FK
        string SourceSystem FK
    }

    PropertyRooms {
        string RoomKey PK
        string Listing FK
    }

    TeamMembers {
        string TeamMemberKey PK
        string Member FK
        string OriginatingSystem FK
        string SourceSystem FK
    }

    Teams {
        string TeamKey PK
        string OriginatingSystem FK
        string SourceSystem FK
        string TeamLead FK
    }

    OUID {
        string OrganizationUniqueIdKey PK
        string ChangedByMember FK
    }

    Contacts {
        string ContactKey PK
        string OriginatingSystem FK
        string OwnerMember FK
        string SourceSystem FK
    }

    Member {
        string MemberKey PK
        string Office FK
        string OriginatingSystem FK
        string SourceSystem FK
    }

    Showing {
        string ShowingKey PK
        string AgentOriginatingSystem FK
        string AgentSourceSystem FK
        string Listing FK
        string ListingOriginatingSystem FK
        string ListingSourceSystem FK
        string ShowingAgent FK
        string ShowingOriginatingSystem FK
        string ShowingSourceSystem FK
    }

        ContactListingNotes ||--o{ Contacts : "Contact"
        ContactListings ||--o{ Contacts : "Contact"
        ContactListings ||--o{ Property : "Listing"
        Member ||--o{ Office : "Office"
        OpenHouse ||--o{ Property : "Listing"
        PropertyGreenVerification ||--o{ Property : "Listing"
        PropertyPowerProduction ||--o{ Property : "Listing"
        PropertyRooms ||--o{ Property : "Listing"
        PropertyUnitTypes ||--o{ Property : "Listing"
        Prospecting ||--o{ Contacts : "Contact"
        Prospecting ||--o{ SavedSearch : "SavedSearch"
        SavedSearch ||--o{ Member : "Member"
        Showing ||--o{ Property : "Listing"
        TeamMembers ||--o{ Member : "Member"
```
