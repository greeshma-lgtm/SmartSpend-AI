"""
Database Setup Script
Creates a SQLite database at database/expenses.db with an expenses table
to store expense records with actual and predicted categories.
"""

import sqlite3
import os


def setup_database(db_path="database/expenses.db"):
    """
    Create the SQLite database and expenses table if they don't exist.
    
    The table schema includes:
    - id: Auto-incrementing primary key
    - date: Date of the expense (TEXT)
    - amount: Amount of the expense (REAL)
    - description: Description of the expense (TEXT)
    - category: Actual category (TEXT)
    - predicted_category: Category predicted by the ML model (TEXT)
    
    Args:
        db_path (str): Path to the SQLite database file
    
    Returns:
        None
    """
    # Ensure the directory exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    # Connect to the database (creates it if it doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create the expenses table if it doesn't already exist
    create_table_query = """
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        amount REAL,
        description TEXT,
        category TEXT,
        predicted_category TEXT
    )
    """
    
    cursor.execute(create_table_query)
    conn.commit()
    
    print(f"✓ Database setup complete at {db_path}")
    print(f"✓ Table 'expenses' created (or already exists)")
    
    conn.close()


def clear_database(db_path="database/expenses.db"):
    """
    Clear all existing data from the expenses table (for fresh runs).
    
    Args:
        db_path (str): Path to the SQLite database file
    
    Returns:
        None
    """
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM expenses")
        conn.commit()
        conn.close()
        print(f"✓ Cleared all existing data from expenses table")


if __name__ == "__main__":
    print("=" * 70)
    print("DATABASE SETUP")
    print("=" * 70)
    setup_database("database/expenses.db")
    print("=" * 70)
