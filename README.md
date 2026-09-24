# ACID Properties in Databases — A Beginner's Study Guide

> **Goal:** Understand the four guarantees that make relational databases trustworthy — **Atomicity, Consistency, Isolation, Durability** — with simple, concrete examples you can run.

---

## What is a Transaction?

A **transaction** is a logical unit of work made up of one or more database operations (reads and writes) that must be treated as a single, indivisible unit. Either **all** of its operations succeed, or **none** of them do.

**Everyday example:** When you transfer $100 from your checking account to your savings account, the database performs two operations:

1. `UPDATE accounts SET balance = balance - 100 WHERE id = 'checking'`
2. `UPDATE accounts SET balance = balance + 100 WHERE id = 'savings'`

If step 1 succeeds but step 2 fails (e.g., the server crashes), you'd lose $100 out of thin air. ACID properties prevent this.

---

## The Four ACID Properties at a Glance

| Property | One-line definition | Real-world analogy |
|---|---|---|
| **A**tomicity | A transaction is all-or-nothing. | A movie ticket purchase: you either get the ticket or your money is refunded. |
| **C**onsistency | A transaction moves the DB from one valid state to another. | A bank account can never have a negative balance if the rules say so. |
| **I**solation | Concurrent transactions don't interfere with each other. | Two people booking the last seat on a plane — only one succeeds. |
| **D**urability | Once committed, changes survive crashes. | A saved game in a video game persists even if the console crashes. |

---

## Table of Contents

1. [Atomicity](./01-atomicity.md) — All-or-nothing transactions
2. [Consistency](./02-consistency.md) — Preserving database invariants
3. [Isolation](./03-isolation.md) — Concurrent transactions don't interfere
4. [Durability](./04-durability.md) — Committed data survives crashes
5. [Summary Table](./summary-table.md) — Side-by-side comparison
6. [Visual Diagram](./diagrams/acid-diagram.md) — Mermaid diagram of the ACID model
7. [Runnable Demos](./demos/) — Python scripts demonstrating each property
8. [Key Takeaways](./takeaways.md) — Checkable study checklist
9. [Resources](./resources.md) — Authoritative references
10. [Notion Page](./notion-page.md) — Ready-to-paste Notion content
11. [Calendar Event](./calendar-event.ics) — Review reminder (2026-09-25 10:00 UTC)

---

## How to Use This Guide

- **Read top-to-bottom** if you're new to databases. Each section builds on the previous one.
- **Run the demos** in `demos/` to see each property in action. They use SQLite (bundled with Python) so no setup is required.
- **Review the takeaways** in `takeaways.md` before your study session.
- **Paste `notion-page.md`** into Notion for a nicely formatted reference page.
- **Import `calendar-event.ics`** into your calendar to schedule a review session.

---

## Prerequisites

- Basic familiarity with SQL (`SELECT`, `INSERT`, `UPDATE`, `DELETE`)
- Python 3.8+ (for the demos)
- No external packages required — demos use only the Python standard library

---

## Learning Objectives

After working through this guide, you should be able to:

- [ ] Define each of the four ACID properties in your own words
- [ ] Explain why each property matters with a concrete example
- [ ] Identify which ACID property is violated in a given failure scenario
- [ ] Describe how databases implement each property (transactions, constraints, locks, WAL)
- [ ] Compare ACID with BASE (the eventual-consistency alternative used in NoSQL)

---

## Quick Reference: SQL Syntax

```sql
-- Start a transaction
BEGIN;

-- Do some work
UPDATE accounts SET balance = balance - 100 WHERE id = 'checking';
UPDATE accounts SET balance = balance + 100 WHERE id = 'savings';

-- Commit (make changes permanent)
COMMIT;

-- OR roll back (undo all changes)
ROLLBACK;
```

---

## Further Reading

See [resources.md](./resources.md) for links to PostgreSQL, MySQL, and academic references.
