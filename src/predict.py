"""
Prediction Module
Provides the predict_category() function to make category predictions
for new expense descriptions using the trained model and vectorizer.
"""

import joblib
import os


# Global variables to cache loaded model and vectorizer
_model = None
_vectorizer = None


def load_model_and_vectorizer(model_path="models/expense_classifier.pkl",
                              vectorizer_path="models/vectorizer.pkl"):
    """
    Load the trained model and vectorizer from disk.
    
    Args:
        model_path (str): Path to the saved model file
        vectorizer_path (str): Path to the saved vectorizer file
    
    Returns:
        tuple: (model, vectorizer)
    
    Raises:
        FileNotFoundError: If model or vectorizer files don't exist
    """
    global _model, _vectorizer
    
    if _model is None or _vectorizer is None:
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
        if not os.path.exists(vectorizer_path):
            raise FileNotFoundError(f"Vectorizer file not found: {vectorizer_path}")
        
        _model = joblib.load(model_path)
        _vectorizer = joblib.load(vectorizer_path)
    
    return _model, _vectorizer


def predict_category(description: str) -> str:
    """
    Predict the expense category for a given description string.
    
    Loads the trained model and vectorizer (cached after first call),
    vectorizes the input description, and returns the predicted category.
    
    Args:
        description (str): The expense description to categorize
                          (e.g., "starbucks coffee", "uber ride")
    
    Returns:
        str: The predicted category (one of the 8 categories)
    
    Raises:
        FileNotFoundError: If model or vectorizer files are not found
    """
    # Load model and vectorizer (cached)
    model, vectorizer = load_model_and_vectorizer()
    
    # Vectorize the input description
    X_input = vectorizer.transform([description])
    
    # Predict the category
    predicted_category = model.predict(X_input)[0]
    
    return predicted_category


def predict_categories_batch(descriptions: list) -> list:
    """
    Predict categories for a batch of descriptions.
    
    Args:
        descriptions (list): List of expense descriptions
    
    Returns:
        list: List of predicted categories
    """
    model, vectorizer = load_model_and_vectorizer()
    
    X_input = vectorizer.transform(descriptions)
    predictions = model.predict(X_input)
    
    return list(predictions)


if __name__ == "__main__":
    # Test the predict_category function with sample descriptions
    print("=" * 70)
    print("TESTING PREDICTION FUNCTION")
    print("=" * 70)
    
    test_descriptions = [
        "starbucks coffee",
        "uber ride",
        "netflix subscription"
    ]
    
    print("\nSample predictions:")
    for desc in test_descriptions:
        try:
            prediction = predict_category(desc)
            print(f"  '{desc}' → {prediction}")
        except FileNotFoundError as e:
            print(f"  Error: {e}")
    
    print("\n" + "=" * 70)
