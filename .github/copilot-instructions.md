```markdown
# SmartSpend AI — Copilot Agent Instructions

## 1. Project Overview
SmartSpend AI is an AI-powered personal expense tracker. Users enter an 
expense description, the system predicts its category using a trained 
ML model, stores the record in a SQL database, and displays everything 
on a Streamlit dashboard with charts.

**Goal:** Automatically categorize expenses (Food, Travel, Bills, 
Shopping, Entertainment, Groceries, Health, Other) using AI.

**Categories (fixed list — do not change without asking):**
Food, Travel, Bills, Shopping, Entertainment, Groceries, Health, Other

## 2. Tech Stack
- Python 3.x
- pandas → data handling
- scikit-learn → ML classification (Multinomial Naive Bayes + TF-IDF/CountVectorizer)
- sqlite3 → database
- streamlit → dashboard UI
- joblib → save/load trained model and vectorizer

## 3. Folder Structure (fixed — do not change without asking)
```
smartspend-ai/
├── data/
│   ├── raw/
│   │   └── expenses_raw.csv          # Step 1 output
│   └── processed/
│       └── expenses_clean.csv        # Step 2 output
├── models/
│   ├── train_model.py                # Step 3 script
│   ├── expense_classifier.pkl        # saved trained model
│   └── vectorizer.pkl                # saved vectorizer
├── database/
│   ├── db_setup.py                   # creates SQLite table
│   ├── db_operations.py              # insert/fetch functions
│   └── expenses.db                   # SQLite database file
├── src/
│   ├── data_collection.py            # Step 1 script
│   ├── preprocess.py                 # Step 2 script
│   └── predict.py                    # loads model, predicts category
├── app/
│   └── dashboard.py                  # Step 5 - Streamlit dashboard
├── tests/
│   └── test_pipeline.py
├── requirements.txt
├── README.md
└── main.py                           # orchestrates steps 1-4 end to end
```

## 4. Pipeline Specification

### Step 1 — Data Collection (`src/data_collection.py`)
- Generate a synthetic sample dataset of 250 expense records, save to 
  `data/raw/expenses_raw.csv`
- Columns: `Date, Amount, Description, Category`
- Use the 8 fixed categories above
- Descriptions must be realistic (e.g. "Domino's Pizza", "Uber ride to 
  airport", "Electricity bill payment", "Amazon order - shoes", 
  "Netflix subscription", "Big Bazaar groceries", "Pharmacy - medicines")
- Dates: random dates in 2026
- Amounts: realistic per category (e.g. Bills higher than Food)

### Step 2 — Preprocessing (`src/preprocess.py`)
- Read `data/raw/expenses_raw.csv`
- Remove duplicates and rows with missing values
- Lowercase the `Description` column
- Strip punctuation/special characters from `Description`
- Save to `data/processed/expenses_clean.csv`
- Print before/after row counts

### Step 3 — Model Training (`models/train_model.py` + `src/predict.py`)
- Read `data/processed/expenses_clean.csv`
- Vectorize `Description` with TF-IDF or CountVectorizer
- Train/test split (80/20)
- Train Multinomial Naive Bayes to predict `Category` from `Description`
- Print accuracy, precision, recall, confusion matrix on test set
- Save model → `models/expense_classifier.pkl`, vectorizer → 
  `models/vectorizer.pkl` (via joblib)
- `src/predict.py` must expose: `predict_category(description: str) -> str`
  which loads the saved model/vectorizer and returns a predicted category 
  for any new description

### Step 4 — SQL Integration (`database/`)
- `database/db_setup.py`: creates SQLite DB at `database/expenses.db` with:
  ```sql
  expenses(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    amount REAL,
    description TEXT,
    category TEXT,
    predicted_category TEXT
  )
  ```
- `database/db_operations.py` functions:
  - `insert_expense(date, amount, description, category, predicted_category)`
  - `fetch_all_expenses()` → returns all rows
  - `fetch_by_category(category)` → returns filtered rows
- A script/function reads `data/processed/expenses_clean.csv`, runs each 
  description through `predict_category()`, and inserts every row (actual 
  + predicted category) into the `expenses` table

### Step 5 — Streamlit Dashboard (`app/dashboard.py`) — NOT STARTED YET
- Do not build unless explicitly instructed
- When built, must include:
  - Input form for new expenses (date, amount, description)
  - On submit: predict category, insert into SQL, show confirmation
  - Table view of all categorized expenses (from `fetch_all_expenses()`)
  - Pie chart of spending by category
  - Monthly spending trend line/bar chart

### `main.py`
- Runs Steps 1–4 end-to-end in order
- Clear print statements showing progress at each step

## 5. Coding Conventions
- Beginner-readable, well-commented code (this is a student project)
- Clear function names + docstrings on every function
- Print progress statements when scripts run (e.g. "Loaded 250 rows", 
  "Model accuracy: 0.87")
- Always use relative paths (e.g. `data/raw/expenses_raw.csv`) — never 
  hardcoded absolute paths
- Save/load models using `joblib`
- Follow PEP8 style
- `requirements.txt` should list: pandas, scikit-learn, joblib, streamlit

## 6. Current Progress
- ✅ Step 1: Data Collection
- ✅ Step 2: Preprocessing
- ✅ Step 3: Model Training
- ✅ Step 4: SQL Integration
- ⏳ Step 5: Streamlit Dashboard — not started

## 7. Rules for the Agent
- Only work within the scope explicitly requested in the current prompt
- Do not modify the folder structure without asking
- Do not add new top-level folders without asking
- Do not build Step 5 (dashboard) until explicitly instructed
- Do not change the fixed category list without asking
- After generating a file, briefly explain what it does
- If a requirement is ambiguous, make a reasonable assumption and state it 
  rather than stopping to ask
```

