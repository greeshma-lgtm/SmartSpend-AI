"""
SmartSpend AI - Main Orchestration Script
Runs the complete expense categorization pipeline (Steps 1-4) end-to-end.

Step 1: Data Collection - Generate synthetic expense dataset
Step 2: Data Preprocessing - Clean and normalize the data
Step 3: Model Training - Train ML classifier and save model
Step 4: SQL Integration - Load predictions into SQLite database
"""

import os
import sys
import subprocess


def run_step(step_number, step_name, script_path):
    """
    Run a single step of the pipeline by executing its script.
    
    Args:
        step_number (int): Step number (1-4)
        step_name (str): Name of the step
        script_path (str): Path to the script to execute
    
    Returns:
        bool: True if the step succeeded, False otherwise
    """
    print("\n" + "=" * 70)
    print(f"STEP {step_number}: {step_name}")
    print("=" * 70)
    
    try:
        result = subprocess.run([sys.executable, script_path], 
                              capture_output=False, text=True)
        
        if result.returncode == 0:
            print(f"✓ Step {step_number} completed successfully")
            return True
        else:
            print(f"✗ Step {step_number} failed with exit code {result.returncode}")
            return False
    
    except Exception as e:
        print(f"✗ Error running Step {step_number}: {e}")
        return False


def main():
    """
    Main orchestration function that runs all 4 steps of the pipeline in order.
    """
    print("\n")
    print("#" * 70)
    print("# SMARTSPEND AI - EXPENSE CATEGORIZATION PIPELINE")
    print("#" * 70)
    print("\nRunning complete pipeline: Data Collection → Preprocessing → Training → SQL Integration\n")
    
    steps = [
        (1, "Data Collection", "src/data_collection.py"),
        (2, "Data Preprocessing", "src/preprocess.py"),
        (3, "Model Training", "models/train_model.py"),
        (4, "SQL Integration", "database/load_data.py"),
    ]
    
    completed_steps = 0
    failed_step = None
    
    for step_num, step_name, script_path in steps:
        success = run_step(step_num, step_name, script_path)
        
        if success:
            completed_steps += 1
        else:
            failed_step = step_num
            print(f"\n✗ Pipeline stopped at Step {step_num}")
            break
    
    # Print final summary
    print("\n")
    print("#" * 70)
    print("# PIPELINE SUMMARY")
    print("#" * 70)
    print(f"\nCompleted Steps: {completed_steps}/4")
    
    if completed_steps == 4:
        print("\n✓ All steps completed successfully!")
        print("\nArtifacts created:")
        print("  - data/raw/expenses_raw.csv (250 synthetic records)")
        print("  - data/processed/expenses_clean.csv (cleaned data)")
        print("  - models/expense_classifier.pkl (trained model)")
        print("  - models/vectorizer.pkl (TF-IDF vectorizer)")
        print("  - database/expenses.db (SQLite database with predictions)")
        print("\nNext steps:")
        print("  - Build Step 5 (Streamlit Dashboard) when ready")
        print("  - Run: streamlit run app/dashboard.py")
    else:
        print(f"\n✗ Pipeline failed at Step {failed_step}")
    
    print("\n" + "#" * 70 + "\n")


if __name__ == "__main__":
    main()
