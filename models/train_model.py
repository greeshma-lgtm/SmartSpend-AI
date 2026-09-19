"""
Step 3: Model Training Script
Trains a Multinomial Naive Bayes classifier to predict expense categories
from expense descriptions. Saves the trained model and vectorizer to the
models/ folder using joblib.
"""

import pandas as pd
import joblib
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix, classification_report
import numpy as np


def load_clean_data(input_path="data/processed/expenses_clean.csv"):
    """
    Load the cleaned expense dataset from CSV.
    
    Args:
        input_path (str): Path to the cleaned CSV file
    
    Returns:
        pd.DataFrame: The loaded dataset
    """
    print(f"Loading cleaned data from {input_path}...")
    # Use dtype_backend='numpy_nullable' to avoid PyArrow-backed dtypes that cause sklearn issues
    df = pd.read_csv(input_path, dtype_backend='numpy_nullable')
    print(f"✓ Loaded {len(df)} records")
    return df


def vectorize_descriptions(descriptions, fit=True, vectorizer=None):
    """
    Vectorize expense descriptions using TF-IDF.
    
    Args:
        descriptions (pd.Series): Series of description text
        fit (bool): Whether to fit the vectorizer (True for training, False for testing)
        vectorizer (TfidfVectorizer): Pre-fitted vectorizer (only used when fit=False)
    
    Returns:
        tuple: (vectorized_data, vectorizer_object)
    """
    if fit:
        print("Vectorizing descriptions using TF-IDF...")
        vectorizer = TfidfVectorizer(max_features=100, lowercase=True, 
                                     stop_words='english', ngram_range=(1, 2))
        X = vectorizer.fit_transform(descriptions)
        print(f"✓ Vectorized to {X.shape[1]} features")
    else:
        X = vectorizer.transform(descriptions)
    
    return X, vectorizer


def train_model(X_train, y_train):
    """
    Train a Multinomial Naive Bayes classifier.
    
    Args:
        X_train: Training feature vectors
        y_train: Training labels (categories)
    
    Returns:
        MultinomialNB: Trained classifier
    """
    print("Training Multinomial Naive Bayes classifier...")
    model = MultinomialNB()
    model.fit(X_train, y_train)
    print("✓ Model trained successfully")
    return model


def evaluate_model(model, X_test, y_test):
    """
    Evaluate the trained model on the test set and print metrics.
    
    Args:
        model (MultinomialNB): Trained classifier
        X_test: Test feature vectors
        y_test: Test labels (categories)
    
    Returns:
        dict: Dictionary containing accuracy, precision, and recall
    """
    print("\nEvaluating model on test set...")
    
    y_pred = model.predict(X_test)
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
    
    print(f"\nAccuracy:  {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    
    # Print confusion matrix
    print("\nConfusion Matrix:")
    cm = confusion_matrix(y_test, y_pred)
    categories = sorted(model.classes_)
    print(f"{'':20} " + " ".join(f"{cat:>10}" for cat in categories))
    for i, cat in enumerate(categories):
        print(f"{cat:20} {cm[i]}")
    
    # Print detailed classification report
    print("\nDetailed Classification Report:")
    print(classification_report(y_test, y_pred, zero_division=0))
    
    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall
    }


def save_model_and_vectorizer(model, vectorizer, 
                               model_path="models/expense_classifier.pkl",
                               vectorizer_path="models/vectorizer.pkl"):
    """
    Save the trained model and vectorizer to disk using joblib.
    
    Args:
        model (MultinomialNB): Trained classifier
        vectorizer (TfidfVectorizer): Fitted vectorizer
        model_path (str): Path to save the model
        vectorizer_path (str): Path to save the vectorizer
    
    Returns:
        None
    """
    # Ensure the directory exists
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    
    # Save model and vectorizer
    joblib.dump(model, model_path)
    joblib.dump(vectorizer, vectorizer_path)
    
    print(f"✓ Model saved to {model_path}")
    print(f"✓ Vectorizer saved to {vectorizer_path}")


def main():
    """
    Main function to orchestrate the model training pipeline.
    Loads data, splits it, trains the model, evaluates it, and saves it.
    """
    print("=" * 70)
    print("STEP 3: MODEL TRAINING")
    print("=" * 70)
    
    # Load cleaned data
    df = load_clean_data("data/processed/expenses_clean.csv")
    
    # Extract features and labels
    X = df['Description'].values
    # Convert Category to plain numpy array to avoid PyArrow dtype issues with train_test_split
    y = df['Category'].astype(str).to_numpy()
    
    print(f"\nDataset Info:")
    print(f"  Total records: {len(df)}")
    print(f"  Categories: {sorted(df['Category'].unique())}")
    
    # Vectorize descriptions
    X_vectorized, vectorizer = vectorize_descriptions(X, fit=True)
    
    # Split data into train/test (80/20)
    print("\nSplitting data into train/test sets (80/20)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X_vectorized, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"✓ Training samples: {X_train.shape[0]}")
    print(f"✓ Test samples: {X_test.shape[0]}")
    
    # Train the model
    model = train_model(X_train, y_train)
    
    # Evaluate the model
    metrics = evaluate_model(model, X_test, y_test)
    
    # Save model and vectorizer
    print("\nSaving model and vectorizer...")
    save_model_and_vectorizer(model, vectorizer)
    
    print("\n" + "=" * 70)
    print("✓ Model training completed successfully!")
    print("=" * 70)


if __name__ == "__main__":
    main()
