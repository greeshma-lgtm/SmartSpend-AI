"""
Database Operations Module
Provides functions to insert and fetch expense records from the SQLite database.
"""

import sqlite3


def insert_expense(date, amount, description, category, predicted_category, 
                   db_path="database/expenses.db"):
    """
    Insert a single expense record into the expenses table.
    
    Args:
        date (str): Date of the expense (YYYY-MM-DD format)
        amount (float): Amount of the expense
        description (str): Description of the expense
        category (str): Actual category (from the dataset)
        predicted_category (str): Category predicted by the ML model
        db_path (str): Path to the SQLite database file
    
    Returns:
        bool: True if insertion was successful, False otherwise
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        insert_query = """
        INSERT INTO expenses (date, amount, description, category, predicted_category)
        VALUES (?, ?, ?, ?, ?)
        """
        
        cursor.execute(insert_query, (date, amount, description, category, predicted_category))
        conn.commit()
        conn.close()
        
        return True
    except Exception as e:
        print(f"Error inserting expense: {e}")
        return False


def fetch_all_expenses(db_path="database/expenses.db"):
    """
    Fetch all expense records from the expenses table.
    
    Args:
        db_path (str): Path to the SQLite database file
    
    Returns:
        list: List of tuples, each representing a row in the expenses table.
              Format: (id, date, amount, description, category, predicted_category)
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        fetch_query = "SELECT * FROM expenses ORDER BY date"
        cursor.execute(fetch_query)
        
        results = cursor.fetchall()
        conn.close()
        
        return results
    except Exception as e:
        print(f"Error fetching all expenses: {e}")
        return []


def fetch_by_category(category, db_path="database/expenses.db"):
    """
    Fetch expense records filtered by a specific category.
    
    Args:
        category (str): The category to filter by
        db_path (str): Path to the SQLite database file
    
    Returns:
        list: List of tuples matching the specified category.
              Format: (id, date, amount, description, category, predicted_category)
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        fetch_query = "SELECT * FROM expenses WHERE category = ? ORDER BY date"
        cursor.execute(fetch_query, (category,))
        
        results = cursor.fetchall()
        conn.close()
        
        return results
    except Exception as e:
        print(f"Error fetching expenses by category: {e}")
        return []


def get_expense_count(db_path="database/expenses.db"):
    """
    Get the total number of expense records in the database.
    
    Args:
        db_path (str): Path to the SQLite database file
    
    Returns:
        int: Total number of records in the expenses table
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM expenses")
        count = cursor.fetchone()[0]
        conn.close()
        
        return count
    except Exception as e:
        print(f"Error getting expense count: {e}")
        return 0
