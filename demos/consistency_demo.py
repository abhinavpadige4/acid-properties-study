#!/usr/bin/env python3
"""
Consistency Demo: Foreign Key Constraints

This demo shows how consistency ensures that database rules (constraints)
are always respected, preventing invalid data from being inserted.

Run: python demos/consistency_demo.py
"""

import sqlite3
import os

DB_PATH = "/tmp/consistency_demo.db"

def setup_database():
    """Create a fresh database with customers and orders tables."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    
    conn.execute("""
        CREATE TABLE customers (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
    """)
    
    conn.execute("""
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            total REAL CHECK (total >= 0),
            status TEXT CHECK (status IN ('pending', 'shipped', 'delivered')),
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        )
    """)
    
    # Insert some valid customers
    conn.execute("INSERT INTO customers VALUES (1, 'Alice', 'alice@example.com')")
    conn.execute("INSERT INTO customers VALUES (2, 'Bob', 'bob@example.com')")
    conn.execute("INSERT INTO customers VALUES (3, 'Charlie', 'charlie@example.com')")
    
    # Insert some valid orders
    conn.execute("INSERT INTO orders VALUES (1, 1, 50.00, 'shipped')")
    conn.execute("INSERT INTO orders VALUES (2, 2, 75.50, 'pending')")
    
    conn.commit()
    
    return conn

def show_customers(conn):
    """Display all customers."""
    print("\n  Customers:")
    print("  " + "-"*40)
    cursor = conn.execute("SELECT id, name, email FROM customers")
    for row in cursor:
        print(f"  ID: {row[0]:2d} | Name: {row[1]:10s} | Email: {row[2]}")

def show_orders(conn):
    """Display all orders."""
    print("\n  Orders:")
    print("  " + "-"*50)
    cursor = conn.execute("""
        SELECT o.id, o.customer_id, c.name, o.total, o.status 
        FROM orders o 
        JOIN customers c ON o.customer_id = c.id
    """)
    for row in cursor:
        print(f"  Order #{row[0]} | Customer: {row[2]:10s} | Total: ${row[3]:>6.2f} | Status: {row[4]}")

def demo_valid_insert(conn):
    """Demo 1: Valid insert (succeeds)."""
    print("\n" + "="*60)
    print("  DEMO 1: Valid Order Insert")
    print("="*60)
    
    print("\n  Attempting to insert a valid order for customer #1 (Alice)...")
    
    try:
        conn.execute("BEGIN")
        conn.execute("INSERT INTO orders VALUES (3, 1, 100.00, 'pending')")
        conn.execute("COMMIT")
        print("  ✅ Success! Order inserted.")
    except Exception as e:
        conn.execute("ROLLBACK")
        print(f"  ❌ Failed: {e}")

def demo_invalid_customer(conn):
    """Demo 2: Invalid customer (foreign key violation)."""
    print("\n" + "="*60)
    print("  DEMO 2: Invalid Customer (Foreign Key Violation)")
    print("="*60)
    
    print("\n  Attempting to insert an order for non-existent customer #999...")
    
    try:
        conn.execute("BEGIN")
        conn.execute("INSERT INTO orders VALUES (4, 999, 50.00, 'pending')")
        conn.execute("COMMIT")
        print("  ✅ Success! (This shouldn't happen)")
    except sqlite3.IntegrityError as e:
        conn.execute("ROLLBACK")
        print(f"  ❌ Failed: {e}")
        print("  ✅ Consistency ensured: Foreign key constraint prevented invalid data!")

def demo_invalid_total(conn):
    """Demo 3: Invalid total (check constraint violation)."""
    print("\n" + "="*60)
    print("  DEMO 3: Invalid Total (Check Constraint Violation)")
    print("="*60)
    
    print("\n  Attempting to insert an order with negative total...")
    
    try:
        conn.execute("BEGIN")
        conn.execute("INSERT INTO orders VALUES (5, 1, -10.00, 'pending')")
        conn.execute("COMMIT")
        print("  ✅ Success! (This shouldn't happen)")
    except sqlite3.IntegrityError as e:
        conn.execute("ROLLBACK")
        print(f"  ❌ Failed: {e}")
        print("  ✅ Consistency ensured: Check constraint prevented negative total!")

def demo_invalid_status(conn):
    """Demo 4: Invalid status (check constraint violation)."""
    print("\n" + "="*60)
    print("  DEMO 4: Invalid Status (Check Constraint Violation)")
    print("="*60)
    
    print("\n  Attempting to insert an order with invalid status...")
    
    try:
        conn.execute("BEGIN")
        conn.execute("INSERT INTO orders VALUES (6, 1, 50.00, 'invalid_status')")
        conn.execute("COMMIT")
        print("  ✅ Success! (This shouldn't happen)")
    except sqlite3.IntegrityError as e:
        conn.execute("ROLLBACK")
        print(f"  ❌ Failed: {e}")
        print("  ✅ Consistency ensured: Check constraint prevented invalid status!")

def demo_cascade_delete(conn):
    """Demo 5: Cascade delete (referential integrity)."""
    print("\n" + "="*60)
    print("  DEMO 5: Cascade Delete (Referential Integrity)")
    print("="*60)
    
    print("\n  Attempting to delete customer #1 who has orders...")
    
    try:
        conn.execute("BEGIN")
        conn.execute("DELETE FROM customers WHERE id = 1")
        conn.execute("COMMIT")
        print("  ✅ Success! (This shouldn't happen without CASCADE)")
    except sqlite3.IntegrityError as e:
        conn.execute("ROLLBACK")
        print(f"  ❌ Failed: {e}")
        print("  ✅ Consistency ensured: Cannot delete customer with existing orders!")

def main():
    print("\n" + "📋"*30)
    print("  CONSISTENCY DEMO: Foreign Key Constraints")
    print("📋"*30)
    
    conn = setup_database()
    
    show_customers(conn)
    show_orders(conn)
    
    demo_valid_insert(conn)
    demo_invalid_customer(conn)
    demo_invalid_total(conn)
    demo_invalid_status(conn)
    demo_cascade_delete(conn)
    
    show_customers(conn)
    show_orders(conn)
    
    print("\n" + "="*60)
    print("  SUMMARY")
    print("="*60)
    print("""
  Consistency ensures that database rules are ALWAYS respected:
  
  ✅ Foreign keys: Orders must reference existing customers
  ✅ Check constraints: Totals must be non-negative
  ✅ Check constraints: Status must be valid
  ✅ Referential integrity: Cannot delete customers with orders
  
  The database never enters an invalid state!
  """)
    
    conn.close()
    os.remove(DB_PATH)

if __name__ == "__main__":
    main()
