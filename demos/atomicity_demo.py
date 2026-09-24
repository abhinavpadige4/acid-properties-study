#!/usr/bin/env python3
"""
Atomicity Demo: Bank Transfer with Rollback

This demo shows how atomicity ensures that a bank transfer either
completes fully or is rolled back completely.

Run: python demos/atomicity_demo.py
"""

import sqlite3
import os

DB_PATH = "/tmp/atomicity_demo.db"

def setup_database():
    """Create a fresh database with two accounts."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    
    conn.execute("""
        CREATE TABLE accounts (
            id TEXT PRIMARY KEY,
            owner TEXT NOT NULL,
            balance REAL NOT NULL CHECK (balance >= 0)
        )
    """)
    
    conn.execute("INSERT INTO accounts VALUES ('checking', 'Alice', 1000.00)")
    conn.execute("INSERT INTO accounts VALUES ('savings', 'Alice', 500.00)")
    conn.commit()
    
    return conn

def show_balances(conn, label=""):
    """Display current account balances."""
    if label:
        print(f"\n{'='*50}")
        print(f"  {label}")
        print(f"{'='*50}")
    
    cursor = conn.execute("SELECT id, owner, balance FROM accounts")
    for row in cursor:
        print(f"  {row[0]:10s} | {row[1]:10s} | ${row[2]:>8.2f}")

def demo_successful_transfer(conn):
    """Demo 1: Successful transfer (both operations succeed)."""
    print("\n" + "="*60)
    print("  DEMO 1: Successful Bank Transfer")
    print("="*60)
    
    show_balances(conn, "BEFORE TRANSFER")
    
    try:
        conn.execute("BEGIN")
        
        # Step 1: Debit checking account
        conn.execute("UPDATE accounts SET balance = balance - 100 WHERE id = 'checking'")
        print("\n  Step 1: Debited $100 from checking")
        
        # Step 2: Credit savings account
        conn.execute("UPDATE accounts SET balance = balance + 100 WHERE id = 'savings'")
        print("  Step 2: Credited $100 to savings")
        
        # Commit the transaction
        conn.execute("COMMIT")
        print("  Step 3: COMMIT - Transaction successful!")
        
    except Exception as e:
        conn.execute("ROLLBACK")
        print(f"  ERROR: {e}")
    
    show_balances(conn, "AFTER TRANSFER")
    print("\n  ✅ Atomicity ensured: Both operations succeeded together.")

def demo_failed_transfer(conn):
    """Demo 2: Failed transfer (second operation fails, rollback occurs)."""
    print("\n" + "="*60)
    print("  DEMO 2: Failed Bank Transfer (Rollback)")
    print("="*60)
    
    show_balances(conn, "BEFORE TRANSFER")
    
    try:
        conn.execute("BEGIN")
        
        # Step 1: Debit checking account
        conn.execute("UPDATE accounts SET balance = balance - 100 WHERE id = 'checking'")
        print("\n  Step 1: Debited $100 from checking")
        
        # Step 2: Try to credit a non-existent account (will fail)
        print("  Step 2: Trying to credit non-existent account...")
        conn.execute("UPDATE accounts SET balance = balance + 100 WHERE id = 'nonexistent'")
        
        # This will fail because the account doesn't exist
        # In a real scenario, this might be a constraint violation
        # or we can simulate a crash
        
        # Simulate a crash by raising an exception
        raise Exception("Simulated crash! Server went down.")
        
        conn.execute("COMMIT")
        
    except Exception as e:
        print(f"  ⚠️  Error: {e}")
        conn.execute("ROLLBACK")
        print("  Step 3: ROLLBACK - All changes undone!")
    
    show_balances(conn, "AFTER FAILED TRANSFER")
    print("\n  ✅ Atomicity ensured: The debit was rolled back.")
    print("     No money was lost!")

def demo_partial_commit(conn):
    """Demo 3: What would happen WITHOUT atomicity."""
    print("\n" + "="*60)
    print("  DEMO 3: Without Atomicity (Hypothetical)")
    print("="*60)
    
    show_balances(conn, "BEFORE TRANSFER")
    
    print("\n  Step 1: Debit $100 from checking (auto-commit)")
    conn.execute("UPDATE accounts SET balance = balance - 100 WHERE id = 'checking'")
    conn.commit()
    
    show_balances(conn, "AFTER DEBIT (before credit)")
    
    print("\n  Step 2: CRASH! Server goes down before credit...")
    print("  💥 CRASH!")
    
    print("\n  Without atomicity, the debit is permanent!")
    print("  Alice lost $100 with no corresponding credit!")
    
    # Reset for next demo
    conn.execute("UPDATE accounts SET balance = balance + 100 WHERE id = 'checking'")
    conn.commit()

def main():
    print("\n" + "🏦"*30)
    print("  ATOMICITY DEMO: Bank Transfer")
    print("🏦"*30)
    
    conn = setup_database()
    
    demo_successful_transfer(conn)
    demo_failed_transfer(conn)
    demo_partial_commit(conn)
    
    print("\n" + "="*60)
    print("  SUMMARY")
    print("="*60)
    print("""
  Atomicity ensures that a transaction is ALL-OR-NOTHING:
  
  ✅ Success: All operations are applied
  ❌ Failure: All operations are rolled back
  
  This prevents partial updates that could corrupt data.
  """)
    
    conn.close()
    os.remove(DB_PATH)

if __name__ == "__main__":
    main()
