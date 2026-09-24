# ACID Properties — Visual Diagram

A Mermaid diagram showing how the four ACID properties work together.

---

## Transaction Lifecycle

```mermaid
flowchart TD
    A[Transaction Starts] --> B{Atomicity Check}
    B -->|All operations succeed| C[Consistency Check]
    B -->|Any operation fails| D[ROLLBACK]
    C -->|Rules satisfied| E[Isolation Check]
    C -->|Rules violated| D
    E -->|No conflicts| F[Durability Check]
    E -->|Conflicts detected| D
    F -->|WAL written| G[COMMIT]
    F -->|WAL write fails| D
    G --> H[Data Persisted]
    D --> I[Transaction Aborted]
    
    style A fill:#e1f5fe
    style G fill:#c8e6c9
    style D fill:#ffcdd2
    style I fill:#ffcdd2
    style H fill:#c8e6c9
```

---

## How Each Property Works

```mermaid
flowchart LR
    subgraph Atomicity
        A1[Operation 1] --> A2[Operation 2] --> A3[Operation 3]
        A3 --> A4{Success?}
        A4 -->|Yes| A5[COMMIT ALL]
        A4 -->|No| A6[ROLLBACK ALL]
    end
    
    subgraph Consistency
        C1[Valid State] --> C2[Transaction] --> C3[Valid State]
        C2 --> C4{Rules OK?}
        C4 -->|Yes| C3
        C4 -->|No| C5[REJECT]
    end
    
    subgraph Isolation
        I1[Transaction A] --> I2[Read/Write]
        I3[Transaction B] --> I4[Read/Write]
        I2 --> I5{Conflict?}
        I4 --> I5
        I5 -->|No| I6[Both proceed]
        I5 -->|Yes| I7[One waits/rolls back]
    end
    
    subgraph Durability
        D1[COMMIT] --> D2[Write to WAL]
        D2 --> D3[Write to Disk]
        D3 --> D4[Crash?]
        D4 -->|No| D5[Data safe]
        D4 -->|Yes| D6[Recover from WAL]
        D6 --> D5
    end
```

---

## Isolation Levels Hierarchy

```mermaid
flowchart TD
    A[READ UNCOMMITTED] --> B[READ COMMITTED]
    B --> C[REPEATABLE READ]
    C --> D[SERIALIZABLE]
    
    A -.- A1[Dirty reads possible]
    B -.- B1[No dirty reads]
    C -.- C1[No non-repeatable reads]
    D -.- D1[Full isolation]
    
    style A fill:#ffcdd2
    style B fill:#fff9c4
    style C fill:#c8e6c9
    style D fill:#a5d6a7
```

---

## WAL (Write-Ahead Log) Flow

```mermaid
sequenceDiagram
    participant Client
    participant DB
    participant WAL
    participant Disk
    
    Client->>DB: BEGIN TRANSACTION
    DB->>DB: Execute operations
    Client->>DB: COMMIT
    DB->>WAL: Write changes to WAL
    WAL->>Disk: fsync (flush to disk)
    Disk-->>WAL: Acknowledged
    WAL-->>DB: WAL write complete
    DB-->>Client: COMMIT acknowledged
    DB->>Disk: Apply changes to data files (later)
    
    Note over DB,Disk: If crash happens here...
    DB->>WAL: Read WAL on restart
    WAL->>DB: Replay committed transactions
    DB->>Disk: Re-apply changes
```

---

## ACID vs. BASE Comparison

```mermaid
flowchart LR
    subgraph ACID
        A1[Atomicity]
        A2[Consistency]
        A3[Isolation]
        A4[Durability]
    end
    
    subgraph BASE
        B1[Basic Availability]
        B2[Available]
        B3[Soft State]
        B4[Eventually Consistent]
    end
    
    A1 -.-> B1
    A2 -.-> B4
    A3 -.-> B3
    A4 -.-> B2
    
    style A1 fill:#e1f5fe
    style A2 fill:#e1f5fe
    style A3 fill:#e1f5fe
    style A4 fill:#e1f5fe
    style B1 fill:#fff3e0
    style B2 fill:#fff3e0
    style B3 fill:#fff3e0
    style B4 fill:#fff3e0
```

---

## When to Use Each

```mermaid
flowchart TD
    A{What do you need?} --> B[Data Integrity Critical?]
    A --> C[High Availability Critical?]
    A --> D[Low Latency Critical?]
    
    B -->|Yes| E[Use ACID Database]
    B -->|No| F{Can you tolerate inconsistency?}
    
    C -->|Yes| G[Use BASE/NoSQL]
    C -->|No| E
    
    D -->|Yes| H[Consider caching layer]
    D -->|No| E
    
    F -->|Yes| G
    F -->|No| E
    
    style E fill:#c8e6c9
    style G fill:#fff3e0
    style H fill:#fff9c4
```
