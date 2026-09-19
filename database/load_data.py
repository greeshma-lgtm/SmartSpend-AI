"""
Data Loading Script
Reads the cleaned expense data, generates predictions for each record,
and loads everything into the SQLite database.
"""

import sys
import os
import pandas as pd

# Add parent directory to path so we can import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_setup import setup_database, clear_database
from database.db_operations import insert_expense, get_expense_count
from src.predict import predict_category


def load_data_to_database(clean_data_path="data/processed/expenses_clean.csv",
                          db_path="database/expenses.db",
                          clear_existing=True):
    """
    Load cleaned expense data into the database with predictions.
    
    Reads the cleaned CSV file, generates predictions for each description,
    and inserts complete records (actual + predicted category) into the database.
    
    Args:
        clean_data_path (str): Path to the cleaned CSV file
        db_path (str): Path to the SQLite database file
        clear_existing (bool): Whether to clear existing data before loading
    
    Returns:
        int: Number of records successfully inserted
    """
    print("=" * 70)
    print("STEP 4: SQL INTEGRATION (DATA LOADING)")
    print("=" * 70)
    
    # Step 1: Setup database
    print("\n1. Setting up database...")
    setup_database(db_path)
    
    if clear_existing:
        clear_database(db_path)
    
    # Step 2: Load cleaned data
    print("\n2. Loading cleaned data...")
    try:
        df = pd.read_csv(clean_data_path)
        print(f"✓ Loaded {len(df)} records from {clean_data_path}")
    except Exception as e:
        print(f"✗ Error loading data: {e}")
        return 0
    
    # Step 3: Generate predictions and insert into database
    print("\n3. Generating predictions and inserting into database...")
    inserted_count = 0
    
    for idx, row in df.iterrows():
        try:
            # Extract data from the row
            date = row['Date']
            amount = row['Amount']
            description = row['Description']
            category = row['Category']
            
            # Generate prediction
            predicted_category = predict_category(description)
            
            # Insert into database
            success = insert_expense(date, amount, description, category, 
                                    predicted_category, db_path)
            
            if success:
                inserted_count += 1
            
            # Print progress every 50 records
            if (idx + 1) % 50 == 0:
                print(f"  Processed {idx + 1}/{len(df)} records...")
        
        except Exception as e:
            print(f"  ✗ Error processing row {idx}: {e}")
            continue
    
    # Step 4: Print summary
    print("\n" + "=" * 70)
    print("DATA LOADING SUMMARY")
    print("=" * 70)
    print(f"Total records processed: {len(df)}")
    print(f"Records inserted:       {inserted_count}")
    print(f"Database location:      {db_path}")
    
    # Get total count in database
    total_in_db = get_expense_count(db_path)
    print(f"Total in database:      {total_in_db}")
    print("=" * 70)
    
    return inserted_count


if __name__ == "__main__":
    load_data_to_database()
