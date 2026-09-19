"""
Step 1: Data Collection Script
Generates a synthetic dataset of 250 expense records with realistic descriptions,
amounts, and categories. Saves to data/raw/expenses_raw.csv.
"""

import pandas as pd
import random
from datetime import datetime, timedelta
import os

# Fixed categories as per project requirements
CATEGORIES = ["Food", "Travel", "Bills", "Shopping", "Entertainment", "Groceries", "Health", "Other"]

# Realistic expense descriptions per category
EXPENSE_TEMPLATES = {
    "Food": [
        "Domino's Pizza",
        "McDonald's lunch",
        "Restaurant dinner",
        "Cafe coffee",
        "Subway sandwich",
        "Starbucks coffee",
        "Burger King meal",
        "Pizza Hut order",
        "Chinese takeout",
        "Biryani lunch"
    ],
    "Travel": [
        "Uber ride to airport",
        "Ola cab ride",
        "Bus ticket",
        "Train ticket",
        "Flight ticket",
        "Taxi ride",
        "Auto rickshaw",
        "Parking fee",
        "Petrol fill-up",
        "Highway toll"
    ],
    "Bills": [
        "Electricity bill payment",
        "Water bill",
        "Internet bill",
        "Mobile phone bill",
        "Gas bill",
        "Rent payment",
        "Insurance premium",
        "Property tax",
        "Electricity charges",
        "Utility payment"
    ],
    "Shopping": [
        "Amazon order - shoes",
        "Flipkart purchase",
        "Myntra clothing",
        "Nike shoes",
        "Adidas apparel",
        "H&M dress",
        "Zara jacket",
        "Watch purchase",
        "Jewelry store",
        "Sunglasses"
    ],
    "Entertainment": [
        "Netflix subscription",
        "Movie ticket",
        "Cinema hall",
        "Gaming subscription",
        "Concert ticket",
        "Spotify premium",
        "YouTube premium",
        "Disney+ subscription",
        "Prime Video membership",
        "Gaming console purchase"
    ],
    "Groceries": [
        "Big Bazaar groceries",
        "Walmart shopping",
        "Dmart vegetables",
        "Supermarket fruits",
        "Food grains purchase",
        "Milk delivery",
        "Bread and dairy",
        "Weekly grocery haul",
        "Veggie market",
        "Farmer's market"
    ],
    "Health": [
        "Pharmacy - medicines",
        "Doctor's appointment",
        "Hospital bill",
        "Dentist checkup",
        "Eye clinic",
        "Lab tests",
        "Gym membership",
        "Medical prescription",
        "Health insurance",
        "Vaccination charge"
    ],
    "Other": [
        "Gift purchase",
        "Donation",
        "Book purchase",
        "Stationery items",
        "Home decoration",
        "Pet supplies",
        "Car wash",
        "Laundry service",
        "Haircut",
        "Personal care items"
    ]
}

# Realistic amount ranges per category (in rupees)
AMOUNT_RANGES = {
    "Food": (150, 600),
    "Travel": (50, 500),
    "Bills": (500, 5000),
    "Shopping": (300, 3000),
    "Entertainment": (100, 1000),
    "Groceries": (200, 1500),
    "Health": (200, 2000),
    "Other": (100, 1000)
}


def generate_random_date(year=2026):
    """
    Generate a random date in the specified year.
    
    Args:
        year (int): Year for the date (default: 2026)
    
    Returns:
        str: Date in YYYY-MM-DD format
    """
    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31)
    random_days = random.randint(0, (end_date - start_date).days)
    random_date = start_date + timedelta(days=random_days)
    return random_date.strftime("%Y-%m-%d")


def generate_expense_record():
    """
    Generate a single expense record with realistic values.
    
    Returns:
        dict: Dictionary with keys: Date, Amount, Description, Category
    """
    # Randomly select a category
    category = random.choice(CATEGORIES)
    
    # Get a random description from the category templates
    description = random.choice(EXPENSE_TEMPLATES[category])
    
    # Get a random amount within the category's realistic range
    min_amount, max_amount = AMOUNT_RANGES[category]
    amount = round(random.uniform(min_amount, max_amount), 2)
    
    # Generate a random date
    date = generate_random_date()
    
    return {
        "Date": date,
        "Amount": amount,
        "Description": description,
        "Category": category
    }


def generate_dataset(num_records=250):
    """
    Generate a dataset of expense records.
    
    Args:
        num_records (int): Number of expense records to generate (default: 250)
    
    Returns:
        pd.DataFrame: DataFrame with expense records
    """
    print(f"Generating {num_records} expense records...")
    
    records = [generate_expense_record() for _ in range(num_records)]
    df = pd.DataFrame(records)
    
    # Sort by date for better readability
    df = df.sort_values("Date").reset_index(drop=True)
    
    print(f"✓ Generated {len(df)} records successfully")
    return df


def save_dataset(df, output_path="data/raw/expenses_raw.csv"):
    """
    Save the dataset to a CSV file.
    
    Args:
        df (pd.DataFrame): DataFrame to save
        output_path (str): Path where CSV should be saved
    
    Returns:
        None
    """
    # Ensure the directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save to CSV
    df.to_csv(output_path, index=False)
    print(f"✓ Dataset saved to {output_path}")
    print(f"  Total records: {len(df)}")


def main():
    """
    Main function to orchestrate data collection.
    Generates the synthetic dataset and saves it to CSV.
    """
    print("=" * 60)
    print("STEP 1: DATA COLLECTION")
    print("=" * 60)
    
    # Generate the dataset
    df = generate_dataset(num_records=250)
    
    # Save to CSV
    save_dataset(df, output_path="data/raw/expenses_raw.csv")
    
    print("=" * 60)
    print("✓ Data collection completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
