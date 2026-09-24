# ACID Properties — Summary Table

A side-by-side comparison of the four ACID properties.

---

## The Big Picture

| Property | Definition | Example | Implementation | Failure Mode Prevented |
|---|---|---|---|---|
| **Atomicity** | All-or-nothing transaction | Bank transfer: debit + credit | Undo logs, WAL | Partial updates |
| **Consistency** | DB stays in valid state | Foreign key constraint | Constraints, triggers | Invalid data |
| **Isolation** | Concurrent txns don't interfere | Ticket booking | Locks, MVCC | Lost updates, dirty reads |
| **Durability** | Committed data survives crashes | Bank deposit after crash | WAL, checkpoints | Data loss on crash |

---

## Visual Comparison

```
┌─────────────────────────────────────────────────────────────┐
│                    ACID PROPERTIES                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌────────┐│
│  │ ATOMIC   │    │ CONSIST  │    │ ISOLATE  │    │ DURABLE││
│  │          │    │          │    │          │    │        ││
│  │ All or   │    │ Rules    │    │ No       │    │ Survives││
│  │ Nothing  │    │ Always   │    │ Interfere│    │ Crashes││
│  │          │    │ Respected│    │          │    │        ││
│  └──────────┘    └──────────┘    └──────────┘    └────────┘│
│                                                             │
│  Bank Transfer   Foreign Key   Ticket Booking   WAL         │
│  Debit+Credit    Constraint    Concurrent       Recovery    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## When Each Property Matters Most

| Scenario | Most Important Property |
|---|---|
| Financial transactions | Atomicity + Durability |
| Multi-user applications | Isolation |
| Data integrity-critical systems | Consistency |
| High-availability systems | Durability |
| Real-time systems | Isolation (with careful level choice) |

---

## ACID vs. BASE

Not all databases follow ACID. NoSQL databases often follow **BASE** instead:

| ACID | BASE |
|---|---|
| **A**tomicity | **B**asic Availability |
| **C**onsistency | **A**vailable |
| **I**solation | **S**oft state |
| **D**urability | **E**ventually consistent |

**When to use ACID:** Financial systems, inventory management, any system where data integrity is critical.

**When to use BASE:** Social media feeds, caching systems, any system where availability is more important than strict consistency.

---

## The CAP Theorem Connection

The **CAP Theorem** states that a distributed system can only guarantee two of three properties:

- **C**onsistency (ACID's C)
- **A**vailability
- **P**artition tolerance

ACID databases typically choose **CP** (Consistency + Partition tolerance), sacrificing availability during network partitions.

BASE databases typically choose **AP** (Availability + Partition tolerance), sacrificing strict consistency.

---

## Quick Quiz

1. **Q:** A bank transfer fails halfway through. Which property ensures the money is safe?
   **A:** Atomicity

2. **Q:** Two users try to book the last seat on a flight. Which property prevents double-booking?
   **A:** Isolation

3. **Q:** A database crashes after a commit. Which property ensures the data is still there?
   **A:** Durability

4. **Q:** An order references a non-existent customer. Which property prevents this?
   **A:** Consistency
