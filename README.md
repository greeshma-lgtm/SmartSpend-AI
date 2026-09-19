# SmartSpend AI - Expense Tracker

## Overview

**SmartSpend AI** is an AI-powered personal expense tracker that automatically categorizes expenses using machine learning. Users input an expense description, and the system predicts its category (Food, Travel, Bills, Shopping, Entertainment, Groceries, Health, or Other) using a trained Multinomial Naive Bayes classifier. All records are stored in a SQLite database and visualized through an interactive Streamlit dashboard with spending analytics, charts, and category-wise summaries.

## Tech Stack

- **Python 3.x** — Core language
- **pandas** — Data manipulation and CSV handling
- **scikit-learn** — Machine learning (Multinomial Naive Bayes, TF-IDF vectorization)
- **sqlite3** — Database (SQLite)
- **joblib** — Model serialization (save/load)
- **streamlit** — Interactive web dashboard
- **plotly** — Interactive charts and visualizations
- **matplotlib** — Additional charting (optional)

## Project Structure

```
smartspend-ai/
├── data/
│   ├── raw/
│   │   └── expenses_raw.csv          # Step 1: 250 synthetic expense records
│   └── processed/
│       └── expenses_clean.csv        # Step 2: Cleaned and normalized data
├── models/
│   ├── train_model.py                # Step 3: Model training script
│   ├── expense_classifier.pkl        # Trained Naive Bayes model (joblib)
│   └── vectorizer.pkl                # Fitted TF-IDF vectorizer (joblib)
├── database/
│   ├── db_setup.py                   # Creates SQLite database and table
│   ├── db_operations.py              # Insert/fetch functions
│   ├── load_data.py                  # Step 4: Loads predictions into database
│   └── expenses.db                   # SQLite database file
├── src/
│   ├── data_collection.py            # Step 1: Generate synthetic data
│   ├── preprocess.py                 # Step 2: Clean and normalize data
│   └── predict.py                    # Module for category prediction
├── app/
│   └── dashboard.py                  # Step 5: Streamlit dashboard
├── tests/
│   └── test_pipeline.py              # Complete test suite (20 tests)
├── main.py                           # Orchestrates all steps (1-5)
├── requirements.txt                  # Project dependencies
├── README.md                         # This file
└── show_database.py                  # Utility to preview database
```

## Setup Instructions

### 1. Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### 2. Create Virtual Environment (Recommended)

**Windows (PowerShell/CMD):**
```bash
python -m venv venv
.\venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Note:** `sqlite3` is included with Python by default and does not need separate installation.

## Running the Project

### Option 1: Run Complete Pipeline (All Steps 1-5)

Runs all steps sequentially: data collection, preprocessing, model training, SQL loading, and launches the dashboard.

```bash
python main.py
```

Then run the dashboard:
```bash
streamlit run app/dashboard.py
```

### Option 2: Run Individual Steps

**Step 1: Generate Synthetic Data**
```bash
python src/data_collection.py
```
Output: `data/raw/expenses_raw.csv` (250 records)

**Step 2: Preprocess Data**
```bash
python src/preprocess.py
```
Output: `data/processed/expenses_clean.csv` (cleaned data)

**Step 3: Train Model**
```bash
python models/train_model.py
```
Output: `models/expense_classifier.pkl` and `models/vectorizer.pkl`

**Step 4: Load Data into Database**
```bash
python database/load_data.py
```
Output: `database/expenses.db` (SQLite database with predictions)

**Step 5: Launch Dashboard**
```bash
streamlit run app/dashboard.py
```
Opens interactive dashboard at `http://localhost:8501`

## Dashboard Features

The Streamlit dashboard includes three main tabs:

### 📝 Add Expense
- **Date picker** — Select expense date
- **Amount input** — Enter expense amount (₹)
- **Description** — Describe the expense (AI auto-categorizes)
- **Quick stats** — Total spending, count, average, highest
- Real-time database updates

### 📊 Analysis
- **Pie chart** — Spending distribution by category
- **Trend chart** — Monthly spending over time
- **Category summary** — Total, count, and average per category

### 📋 All Expenses
- **Filterable table** — View expenses by category
- **Full details** — Date, amount, description, actual and predicted category
- **Summary metrics** — Total, count, average for filtered view

## Testing

Run the complete test suite to validate all pipeline components:

```bash
python tests/test_pipeline.py
```

**Test Coverage (20 Tests):**

| Component | Tests | Details |
|-----------|-------|---------|
| **Data Collection** | 3 | Raw CSV exists, correct columns, 250+ records |
| **Data Preprocessing** | 5 | Cleaned CSV exists, no duplicates, no missing values, lowercase, no special chars |
| **Model Training** | 4 | Model file exists, vectorizer exists, both load successfully |
| **Prediction** | 3 | Returns valid category, multiple samples work, returns string |
| **SQL Integration** | 5 | Database exists, table exists, correct columns, has data, correct structure |

**Expected Output:**
```
Ran 20 tests in ~0.8s
✓ ALL TESTS PASSED!
```

## Model Performance

### Training Metrics
- **Accuracy:** 84.00%
- **Precision:** 87.70%
- **Recall:** 84.00%

### Category Performance (on 250 records)
| Category | Accuracy | Notes |
|----------|----------|-------|
| Bills | 100.0% | ⭐ Perfect predictions |
| Food | 96.8% | ⭐ Excellent |
| Groceries | 88.6% | ✓ Good |
| Travel | 83.9% | ✓ Good |
| Entertainment | 77.1% | ~ Okay |
| Shopping | 75.0% | ~ Okay |
| Health | 68.6% | ⚠️ Needs improvement |
| Other | 52.4% | ⚠️ Needs improvement |

### Limitations & Notes
- **Small training dataset:** Only 250 synthetic records; real-world performance may vary
- **Limited categories:** 8 categories may need expansion (e.g., Insurance, Charity, Education)
- **Description dependency:** Accuracy depends on clear, descriptive expense text
- **Production use:** Should be retrained with real expense data for better accuracy
- **Health category issues:** Often confused with Entertainment; may need better features

## Requirements File

See `requirements.txt` for exact versions. Core packages:
- pandas, scikit-learn, joblib (data & ML)
- sqlite3 (database — bundled with Python)
- streamlit, plotly, matplotlib (UI & visualization)

## Team Contributions

| Role | Responsibilities |
|------|------------------|
| [Name] | Data Collection & Synthetic Dataset Generation |
| [Name] | Data Preprocessing & Cleaning |
| [Name] | Model Training & ML Pipeline |
| [Name] | Database Design & SQL Integration |
| [Name] | Dashboard Development & Visualization |

## Future Improvements

- [ ] Deploy to cloud (Streamlit Cloud, Heroku, AWS)
- [ ] Add recurring expense tracking
- [ ] Implement budget alerts
- [ ] Export reports (PDF, Excel)
- [ ] User authentication and multi-user support
- [ ] Retrain model with real expense data
- [ ] Add more categories based on user feedback
- [ ] Mobile app version
- [ ] Advanced analytics (spending trends, predictions)

## Getting Help

- Check `tests/test_pipeline.py` to understand data flow
- Review individual step scripts for detailed comments
- Run `python main.py` to see the complete pipeline in action
- Check the dashboard for live data visualization

## License

This is a student project for educational purposes.

---

**Last Updated:** September 2026  
**Status:** ✓ All Steps Complete (Steps 1-5)
