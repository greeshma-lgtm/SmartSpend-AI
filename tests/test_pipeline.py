"""
Test Pipeline Module
Tests for the complete SmartSpend AI expense categorization pipeline.

Tests cover:
1. Raw data collection and file creation
2. Data preprocessing (cleaning, deduplication)
3. Model training and artifact saving
4. Prediction functionality
5. Database integration and data loading
"""

import unittest
import os
import sys
import pandas as pd
import joblib
import sqlite3

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.predict import predict_category
from database.db_operations import fetch_all_expenses


class TestDataCollection(unittest.TestCase):
    """Test cases for Step 1: Data Collection"""
    
    def test_raw_csv_exists(self):
        """Test that data/raw/expenses_raw.csv exists"""
        csv_path = "data/raw/expenses_raw.csv"
        self.assertTrue(os.path.exists(csv_path), 
                       f"Raw CSV file not found: {csv_path}")
    
    def test_raw_csv_has_correct_columns(self):
        """Test that raw CSV has required columns: Date, Amount, Description, Category"""
        csv_path = "data/raw/expenses_raw.csv"
        df = pd.read_csv(csv_path)
        
        required_columns = {'Date', 'Amount', 'Description', 'Category'}
        actual_columns = set(df.columns)
        
        self.assertEqual(required_columns, actual_columns,
                        f"Column mismatch. Expected {required_columns}, got {actual_columns}")
    
    def test_raw_csv_has_data(self):
        """Test that raw CSV has at least 250 records as expected"""
        csv_path = "data/raw/expenses_raw.csv"
        df = pd.read_csv(csv_path)
        
        self.assertGreaterEqual(len(df), 250,
                               f"Expected at least 250 records, got {len(df)}")


class TestDataPreprocessing(unittest.TestCase):
    """Test cases for Step 2: Data Preprocessing"""
    
    def test_clean_csv_exists(self):
        """Test that data/processed/expenses_clean.csv exists"""
        csv_path = "data/processed/expenses_clean.csv"
        self.assertTrue(os.path.exists(csv_path),
                       f"Cleaned CSV file not found: {csv_path}")
    
    def test_clean_csv_no_duplicates(self):
        """Test that cleaned CSV has no duplicate rows"""
        csv_path = "data/processed/expenses_clean.csv"
        df = pd.read_csv(csv_path)
        
        duplicates_count = df.duplicated().sum()
        self.assertEqual(duplicates_count, 0,
                        f"Found {duplicates_count} duplicate rows in cleaned data")
    
    def test_clean_csv_no_missing_values(self):
        """Test that cleaned CSV has no missing values"""
        csv_path = "data/processed/expenses_clean.csv"
        df = pd.read_csv(csv_path)
        
        missing_count = df.isnull().sum().sum()
        self.assertEqual(missing_count, 0,
                        f"Found {missing_count} missing values in cleaned data")
    
    def test_descriptions_are_lowercase(self):
        """Test that descriptions in cleaned CSV are lowercase"""
        csv_path = "data/processed/expenses_clean.csv"
        df = pd.read_csv(csv_path)
        
        for desc in df['Description'].head(10):
            self.assertEqual(desc, desc.lower(),
                           f"Description not lowercase: '{desc}'")
    
    def test_descriptions_no_special_chars(self):
        """Test that descriptions have no special characters (only alphanumeric and spaces)"""
        csv_path = "data/processed/expenses_clean.csv"
        df = pd.read_csv(csv_path)
        
        import re
        for desc in df['Description'].head(10):
            # Check for non-alphanumeric characters (except spaces)
            if re.search(r'[^a-z0-9\s]', desc):
                self.fail(f"Description contains special characters: '{desc}'")


class TestModelTraining(unittest.TestCase):
    """Test cases for Step 3: Model Training"""
    
    def test_model_file_exists(self):
        """Test that models/expense_classifier.pkl exists"""
        model_path = "models/expense_classifier.pkl"
        self.assertTrue(os.path.exists(model_path),
                       f"Model file not found: {model_path}")
    
    def test_vectorizer_file_exists(self):
        """Test that models/vectorizer.pkl exists"""
        vectorizer_path = "models/vectorizer.pkl"
        self.assertTrue(os.path.exists(vectorizer_path),
                       f"Vectorizer file not found: {vectorizer_path}")
    
    def test_model_can_be_loaded(self):
        """Test that the trained model can be loaded successfully"""
        model_path = "models/expense_classifier.pkl"
        try:
            model = joblib.load(model_path)
            self.assertIsNotNone(model,
                               "Failed to load model (None returned)")
        except Exception as e:
            self.fail(f"Failed to load model: {e}")
    
    def test_vectorizer_can_be_loaded(self):
        """Test that the vectorizer can be loaded successfully"""
        vectorizer_path = "models/vectorizer.pkl"
        try:
            vectorizer = joblib.load(vectorizer_path)
            self.assertIsNotNone(vectorizer,
                               "Failed to load vectorizer (None returned)")
        except Exception as e:
            self.fail(f"Failed to load vectorizer: {e}")


class TestPrediction(unittest.TestCase):
    """Test cases for Prediction Module (src/predict.py)"""
    
    # Valid categories as per project specification
    VALID_CATEGORIES = {'Food', 'Travel', 'Bills', 'Shopping', 
                       'Entertainment', 'Groceries', 'Health', 'Other'}
    
    def test_predict_category_returns_valid_category(self):
        """Test that predict_category() returns a valid category"""
        prediction = predict_category("starbucks coffee")
        self.assertIn(prediction, self.VALID_CATEGORIES,
                     f"Prediction '{prediction}' not in valid categories")
    
    def test_predict_category_multiple_samples(self):
        """Test predict_category() with multiple sample descriptions"""
        test_descriptions = [
            "dominos pizza",
            "uber ride",
            "netflix subscription",
            "electricity bill",
            "big bazaar groceries"
        ]
        
        for desc in test_descriptions:
            prediction = predict_category(desc)
            self.assertIn(prediction, self.VALID_CATEGORIES,
                         f"Prediction for '{desc}': '{prediction}' is not valid")
    
    def test_predict_category_is_string(self):
        """Test that predict_category() returns a string"""
        prediction = predict_category("test expense")
        self.assertIsInstance(prediction, str,
                             f"Expected string, got {type(prediction)}")


class TestSQLIntegration(unittest.TestCase):
    """Test cases for Step 4: SQL Integration"""
    
    def test_database_exists(self):
        """Test that database/expenses.db exists"""
        db_path = "database/expenses.db"
        self.assertTrue(os.path.exists(db_path),
                       f"Database file not found: {db_path}")
    
    def test_expenses_table_exists(self):
        """Test that the expenses table exists in the database"""
        db_path = "database/expenses.db"
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='expenses'
            """)
            
            result = cursor.fetchone()
            conn.close()
            
            self.assertIsNotNone(result,
                               "expenses table not found in database")
        except Exception as e:
            self.fail(f"Failed to check table: {e}")
    
    def test_expenses_table_has_correct_columns(self):
        """Test that expenses table has the correct columns"""
        db_path = "database/expenses.db"
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            cursor.execute("PRAGMA table_info(expenses)")
            columns = cursor.fetchall()
            
            column_names = {col[1] for col in columns}
            required_columns = {'id', 'date', 'amount', 'description', 
                              'category', 'predicted_category'}
            
            self.assertEqual(required_columns, column_names,
                           f"Column mismatch. Expected {required_columns}, got {column_names}")
            
            conn.close()
        except Exception as e:
            self.fail(f"Failed to check columns: {e}")
    
    def test_fetch_all_expenses_returns_data(self):
        """Test that fetch_all_expenses() returns at least 1 row"""
        db_path = "database/expenses.db"
        try:
            expenses = fetch_all_expenses(db_path)
            self.assertGreater(len(expenses), 0,
                             "fetch_all_expenses() returned no data")
        except Exception as e:
            self.fail(f"fetch_all_expenses() failed: {e}")
    
    def test_fetch_all_expenses_row_structure(self):
        """Test that fetched expenses have correct structure"""
        db_path = "database/expenses.db"
        try:
            expenses = fetch_all_expenses(db_path)
            
            if len(expenses) > 0:
                first_row = expenses[0]
                # Should have 6 columns: id, date, amount, description, category, predicted_category
                self.assertEqual(len(first_row), 6,
                               f"Expected 6 columns, got {len(first_row)}")
        except Exception as e:
            self.fail(f"Row structure check failed: {e}")


def run_tests():
    """
    Run all tests and print a summary report.
    """
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestDataCollection))
    suite.addTests(loader.loadTestsFromTestCase(TestDataPreprocessing))
    suite.addTests(loader.loadTestsFromTestCase(TestModelTraining))
    suite.addTests(loader.loadTestsFromTestCase(TestPrediction))
    suite.addTests(loader.loadTestsFromTestCase(TestSQLIntegration))
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Tests run:    {result.testsRun}")
    print(f"Passed:       {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failed:       {len(result.failures)}")
    print(f"Errors:       {len(result.errors)}")
    print("=" * 70)
    
    if result.wasSuccessful():
        print("\n✓ ALL TESTS PASSED!")
    else:
        print("\n✗ SOME TESTS FAILED!")
        if result.failures:
            print("\nFailures:")
            for test, traceback in result.failures:
                print(f"  - {test}")
        if result.errors:
            print("\nErrors:")
            for test, traceback in result.errors:
                print(f"  - {test}")
    
    print("=" * 70 + "\n")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
