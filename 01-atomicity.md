# Atomicity

> **Definition:** A transaction is **atomic** if it is treated as a single, indivisible unit of work. Either **all** of its operations succeed, or **none** of them do. There is no middle ground.

---

## The Core Idea

Think of a transaction like a magic trick: the audience sees only the beginning and the end. They never see the intermediate steps. If the trick fails halfway through, the magician "un-does" everything and the audience sees nothing happened.

In database terms:

- **Success path:** All operations in the transaction are applied.
- **Failure path:** All operations are rolled back, as if the transaction never started.

---

## Real-World Example: Bank Transfer

You want to transfer $100 from your checking account to your savings account.

```sql
BEGIN;

UPDATE accounts SET balance = balance - 100 WHERE id = 'checking';
UPDATE accounts SET balance = balance + 100 WHERE id = 'savings';

COMMIT;
```

### What could go wrong?

Imagine the server crashes **after** the first `UPDATE` but **before** the second:

| Step | Without Atomicity | With Atomicity |
|---|---|---|
| 1. Debit checking | ✅ Done | ✅ Done |
| 2. Crash | 💥 | 💥 |
| 3. Credit savings | ❌ Never happens | ❌ Rolled back |
| **Final state** | **You lost $100!** | **Nothing changed.** |

With atomicity, the database automatically rolls back the debit when it detects the crash, so your money is safe.

---

## How Databases Implement Atomicity

Databases use a combination of techniques:

1. **Transaction logs (WAL — Write-Ahead Log):** Every change is written to a log *before* it's applied to the actual data. On recovery, the log tells the database what to undo.
2. **Undo logs:** Record the "before" state of every modified row so it can be restored on rollback.
3. **Two-phase commit (2PC):** For distributed transactions, a coordinator ensures all participants agree before anyone commits.

---

## SQL Syntax

```sql
-- Explicit transaction
BEGIN;
  -- ... operations ...
COMMIT;   -- make permanent
-- OR
ROLLBACK; -- undo everything

-- Auto-commit (default in most clients)
-- Each statement is its own transaction
UPDATE accounts SET balance = balance - 100 WHERE id = 'checking';
```

---

## Common Pitfalls

- **Forgetting to commit:** Some databases auto-rollback when the connection closes.
- **Partial commits:** If you split a logical operation across multiple transactions, you lose atomicity.
- **Assuming DDL is atomic:** In some databases, `CREATE TABLE` inside a transaction may auto-commit.

---

## Try It Yourself

Run the demo:

```bash
python demos/atomicity_demo.py
```

The demo shows a bank transfer that fails halfway through and is automatically rolled back.

---

## Key Takeaway

> **Atomicity = All or Nothing.** A transaction either fully succeeds or fully fails. There is no partial state.
