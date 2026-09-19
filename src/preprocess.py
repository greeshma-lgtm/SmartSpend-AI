"""
Step 2: Data Preprocessing Script
Cleans the raw expense dataset by removing duplicates, handling missing values,
lowercasing descriptions, and stripping punctuation/special characters.
Saves the cleaned data to data/processed/expenses_clean.csv.
"""

import pandas as pd
import re
import os


def load_raw_data(input_path="data/raw/expenses_raw.csv"):
    """
    Load the raw expense dataset from CSV.
    
    Args:
        input_path (str): Path to the raw CSV file
    
    Returns:
        pd.DataFrame: The loaded dataset
    """
    print(f"Loading raw data from {input_path}...")
    df = pd.read_csv(input_path)
    print(f"✓ Loaded {len(df)} records")
    return df


def remove_duplicates(df):
    """
    Remove duplicate rows from the dataset.
    
    Args:
        df (pd.DataFrame): Input dataframe
    
    Returns:
        pd.DataFrame: Dataframe with duplicates removed
    """
    initial_count = len(df)
    df = df.drop_duplicates(keep='first')
    removed_count = initial_count - len(df)
    
    if removed_count > 0:
        print(f"  Removed {removed_count} duplicate rows")
    else:
        print(f"  No duplicates found")
    
    return df


def handle_missing_values(df):
    """
    Remove rows with missing (NaN) values.
    
    Args:
        df (pd.DataFrame): Input dataframe
    
    Returns:
        pd.DataFrame: Dataframe with rows containing missing values removed
    """
    initial_count = len(df)
    df = df.dropna()
    removed_count = initial_count - len(df)
    
    if removed_count > 0:
        print(f"  Removed {removed_count} rows with missing values")
    else:
        print(f"  No missing values found")
    
    return df


def clean_description(description):
    """
    Clean a single description string by:
    - Converting to lowercase
    - Removing punctuation and special characters (keeping alphanumeric and spaces)
    
    Args:
        description (str): The description to clean
    
    Returns:
        str: The cleaned description
    """
    # Convert to lowercase
    description = description.lower()
    
    # Remove punctuation and special characters, keep only alphanumeric and spaces
    description = re.sub(r'[^a-z0-9\s]', '', description)
    
    # Remove extra whitespace
    description = ' '.join(description.split())
    
    return description


def preprocess_descriptions(df):
    """
    Apply cleaning transformations to the Description column.
    
    Args:
        df (pd.DataFrame): Input dataframe
    
    Returns:
        pd.DataFrame: Dataframe with cleaned descriptions
    """
    print(f"  Cleaning descriptions (lowercase + remove punctuation)...")
    df['Description'] = df['Description'].apply(clean_description)
    return df


def save_clean_data(df, output_path="data/processed/expenses_clean.csv"):
    """
    Save the cleaned dataset to a CSV file.
    
    Args:
        df (pd.DataFrame): The cleaned dataframe
        output_path (str): Path where the cleaned CSV should be saved
    
    Returns:
        None
    """
    # Ensure the directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save to CSV
    df.to_csv(output_path, index=False)
    print(f"✓ Cleaned data saved to {output_path}")


def main():
    """
    Main function to orchestrate the preprocessing pipeline.
    Loads raw data, applies all cleaning transformations, and saves the result.
    """
    print("=" * 70)
    print("STEP 2: DATA PREPROCESSING")
    print("=" * 70)
    
    # Load raw data
    df = load_raw_data("data/raw/expenses_raw.csv")
    initial_count = len(df)
    
    print("\nCleaning data...")
    
    # Step 1: Remove duplicates
    df = remove_duplicates(df)
    
    # Step 2: Handle missing values
    df = handle_missing_values(df)
    
    # Step 3: Clean descriptions
    df = preprocess_descriptions(df)
    
    final_count = len(df)
    removed_total = initial_count - final_count
    
    print("\n" + "=" * 70)
    print("PREPROCESSING SUMMARY")
    print("=" * 70)
    print(f"Initial rows:    {initial_count}")
    print(f"Final rows:      {final_count}")
    print(f"Rows removed:    {removed_total}")
    print("=" * 70)
    
    # Save cleaned data
    save_clean_data(df, "data/processed/expenses_clean.csv")
    
    print("=" * 70)
    print("✓ Data preprocessing completed successfully!")
    print("=" * 70)


if __name__ == "__main__":
    main()
