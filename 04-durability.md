# Durability

> **Definition:** A transaction is **durable** if, once it has been committed, its effects persist even if the system crashes, loses power, or experiences a hardware failure.

---

## The Core Idea

When you `COMMIT` a transaction, you're making a promise: "This data will survive forever (or at least until someone explicitly deletes it)." Durability is the guarantee that the database keeps that promise, even in the face of disasters.

---

## Real-World Example: Write-Ahead Log (WAL)

Imagine you're saving a game in a video game console. You press "Save" and the screen shows "Saved!". Then the power goes out. When you turn the console back on, your save is still there.

Databases work the same way, using a technique called the **Write-Ahead Log (WAL)**:

### How WAL works:

```
1. Transaction wants to commit
2. Database writes the change to the WAL (on disk)
3. Database writes "COMMIT" marker to the WAL
4. Database acknowledges the commit to the client
5. (Later) Database applies the change to the main data files
```

### What happens on crash?

```
Scenario: Crash after step 3 but before step 5

On restart:
1. Database reads the WAL
2. Finds the "COMMIT" marker
3. Re-applies the change to the data files
4. Data is restored!
```

---

## Real-World Example: Bank Deposit

You deposit $500 at an ATM. The machine prints a receipt saying "Deposit Successful." Then the bank's servers crash.

**With durability:** When the servers come back online, your $500 is in your account. The WAL ensured the commit was recorded before the receipt was printed.

**Without durability:** Your $500 might vanish. The receipt was printed, but the actual balance update was lost.

---

## How Databases Implement Durability

1. **Write-Ahead Log (WAL):** The primary mechanism. All changes are logged before being applied.
2. **Checkpointing:** Periodically flushes WAL contents to data files to keep the WAL small.
3. **Redo logs:** Record changes to re-apply on recovery.
4. **Undo logs:** Record "before" states to roll back incomplete transactions.
5. **Disk sync (`fsync`):** Forces data from OS cache to physical disk.

---

## Durability vs. Atomicity

| Property | Question |
|---|---|
| **Atomicity** | If a transaction fails, is it fully rolled back? |
| **Durability** | If a transaction commits, does it survive a crash? |

They're two sides of the same coin:
- **Atomicity** handles failures *during* a transaction.
- **Durability** handles failures *after* a transaction commits.

---

## SQL Syntax

```sql
-- Standard commit (durable by default)
COMMIT;

-- In PostgreSQL, you can control durability
-- (not recommended for production!)
SET TRANSACTION DEFERRABLE;  -- may delay durability for performance

-- Force a checkpoint (flush WAL to data files)
CHECKPOINT;
```

---

## Try It Yourself

Run the demo:

```bash
python demos/durability_demo.py
```

The demo simulates a crash after commit and shows how the WAL allows recovery.

---

## Key Takeaway

> **Durability = Committed data survives crashes.** Once you see "COMMIT", the data is safe — even if the power goes out.
