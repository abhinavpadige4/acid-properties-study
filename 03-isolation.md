# Isolation

> **Definition:** A transaction is **isolated** if its intermediate state is invisible to other concurrent transactions. Each transaction appears to run alone, as if no other transactions are happening at the same time.

---

## The Core Idea

Databases handle many transactions at once. Without isolation, two transactions could interfere with each other in surprising ways. Isolation ensures that concurrent transactions don't corrupt each other's results.

---

## Real-World Example: Concurrent Ticket Booking

Imagine the last seat on a flight. Two customers, Alice and Bob, try to book it at the same time.

### Without isolation (the "lost update" problem):

```
Time  | Alice                          | Bob
------|--------------------------------|--------------------------------
T1    | Read seat 12A: available       | Read seat 12A: available
T2    | Update seat 12A: booked        | Update seat 12A: booked
T3    | COMMIT                         | COMMIT
------|--------------------------------|--------------------------------
Result: Seat 12A is "booked" but TWO customers think they got it!
```

### With isolation:

```
Time  | Alice                          | Bob
------|--------------------------------|--------------------------------
T1    | Read seat 12A: available       | (waits for Alice)
T2    | Update seat 12A: booked        |
T3    | COMMIT                         | Read seat 12A: BOOKED
T4    |                                | ROLLBACK (seat taken)
------|--------------------------------|--------------------------------
Result: Only Alice gets the seat. Bob is told it's unavailable.
```

---

## The Four Classic Anomalies

Without proper isolation, concurrent transactions can cause:

| Anomaly | Description | Example |
|---|---|---|
| **Dirty Read** | Reading uncommitted data from another transaction | Alice reads Bob's transfer before Bob commits |
| **Non-repeatable Read** | Reading different values for the same row twice | Alice reads balance $100, then $50 after Bob's update |
| **Phantom Read** | New rows appearing/disappearing between reads | Alice counts 5 orders, then sees 6 after Bob inserts |
| **Lost Update** | One transaction's write overwrites another's | Both Alice and Bob update the same seat |

---

## Isolation Levels (SQL Standard)

Databases offer different isolation levels, trading off consistency for performance:

| Level | Dirty Read | Non-repeatable | Phantom | Performance |
|---|---|---|---|---|
| **READ UNCOMMITTED** | ✅ Possible | ✅ Possible | ✅ Possible | Fastest |
| **READ COMMITTED** | ❌ Prevented | ✅ Possible | ✅ Possible | Fast |
| **REPEATABLE READ** | ❌ Prevented | ❌ Prevented | ✅ Possible* | Slower |
| **SERIALIZABLE** | ❌ Prevented | ❌ Prevented | ❌ Prevented | Slowest |

*PostgreSQL's REPEATABLE READ actually prevents phantoms too.

### SQL Syntax

```sql
-- Set isolation level for the current transaction
BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;

-- Or in PostgreSQL
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;

-- MySQL
SET SESSION TRANSACTION ISOLATION LEVEL SERIALIZABLE;
```

---

## How Databases Implement Isolation

1. **Locking:** Pessimistic (acquire locks upfront) or optimistic (detect conflicts at commit)
2. **MVCC (Multi-Version Concurrency Control):** Each transaction sees a snapshot of the data at a point in time. Used by PostgreSQL and MySQL InnoDB.
3. **Timestamp ordering:** Assign timestamps to transactions and order them logically.

---

## Try It Yourself

Run the demo:

```bash
python demos/isolation_demo.py
```

The demo simulates two concurrent ticket bookings and shows how isolation prevents double-booking.

---

## Key Takeaway

> **Isolation = Transactions don't interfere.** Each transaction sees a consistent view of the data, as if it were running alone.
