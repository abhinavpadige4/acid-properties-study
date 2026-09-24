# Consistency

> **Definition:** A transaction is **consistent** if it moves the database from one **valid state** to another **valid state**, preserving all defined rules (constraints, triggers, foreign keys, check constraints).

---

## The Core Idea

A database has **invariants** — rules that must always be true. Examples:

- A bank account balance must never be negative.
- An order must reference an existing customer.
- A user's age must be between 0 and 150.

A consistent transaction never violates these rules, even temporarily.

---

## Real-World Example: Foreign Key Constraint

Consider two tables:

```sql
CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    total REAL,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);
```

The **invariant** is: *every order must belong to an existing customer*.

### What could go wrong?

```sql
BEGIN;

-- Try to insert an order for a customer that doesn't exist
INSERT INTO orders (id, customer_id, total) VALUES (101, 9999, 50.00);

COMMIT;
```

**Result:** The database **rejects** the transaction with an error like:

```
FOREIGN KEY constraint failed: orders.customer_id
```

The database never enters an invalid state where an order points to a non-existent customer.

### Another example: Check constraint

```sql
CREATE TABLE accounts (
    id INTEGER PRIMARY KEY,
    balance REAL CHECK (balance >= 0)
);

-- This will fail because it would violate the CHECK constraint
UPDATE accounts SET balance = -50 WHERE id = 1;
```

---

## How Databases Implement Consistency

1. **Constraints:** `PRIMARY KEY`, `FOREIGN KEY`, `UNIQUE`, `CHECK`, `NOT NULL`
2. **Triggers:** Custom logic that runs before/after a change
3. **Stored procedures:** Encapsulate business rules
4. **Application-level validation:** Sometimes rules live in the app, not the DB

---

## Consistency vs. Atomicity

These two properties are often confused. Here's the difference:

| Property | Question it answers |
|---|---|
| **Atomicity** | Did the transaction complete fully, or was it rolled back? |
| **Consistency** | Does the database still satisfy all its rules after the transaction? |

**Atomicity is a mechanism; consistency is a goal.** Atomicity helps achieve consistency by ensuring partial updates don't leave the DB in a broken state.

---

## Try It Yourself

Run the demo:

```bash
python demos/consistency_demo.py
```

The demo shows a foreign key constraint preventing an invalid order from being inserted.

---

## Key Takeaway

> **Consistency = Rules are always respected.** A transaction can only succeed if the database remains in a valid state afterward.
