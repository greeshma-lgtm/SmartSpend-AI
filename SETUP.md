# SmartSpend AI - Team Setup Guide

Welcome to the SmartSpend AI project! This guide will help you set up the development environment and run the application locally.

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** — [Download here](https://www.python.org/downloads/)
- **Git** — [Download here](https://git-scm.com/)
- **pip** — Usually comes with Python (verify: `pip --version`)

**Verify installations:**
```powershell
python --version
git --version
pip --version
```

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Clone the Repository

```powershell
git clone https://github.com/Arunachalam101/SmartSpend-AI.git
cd SmartSpend-AI
```

### Step 2: Create Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```powershell
pip install -r requirements.txt
```

### Step 4: Run the Complete Pipeline

This generates synthetic data, trains the ML model, creates the database, and prepares everything:

```powershell
python main.py
```

**Expected output:**
```
✓ Step 1: Data Collection - 250 records generated
✓ Step 2: Data Preprocessing - Data cleaned and normalized
✓ Step 3: Model Training - Model trained with 90% accuracy
✓ Step 4: SQL Integration - 250 records loaded into database
✓ Pipeline complete!
```

### Step 5: Launch the Dashboard

```powershell
streamlit run app/dashboard.py
```

The dashboard will open at: **http://localhost:8501**

---

## 📁 Project Structure

```
SmartSpend-AI/
├── src/                      # Core pipeline scripts
│   ├── data_collection.py   # Step 1: Generate synthetic expenses
│   ├── preprocess.py        # Step 2: Clean and normalize data
│   └── predict.py           # Prediction module
├── models/                   # Machine learning
│   └── train_model.py       # Step 3: Train Naive Bayes classifier
├── database/                # Database layer
│   ├── db_setup.py         # Create SQLite schema
│   ├── db_operations.py    # Insert/fetch functions
│   └── load_data.py        # Step 4: Load predictions into DB
├── app/
│   └── dashboard.py         # Step 5: Streamlit interactive dashboard
├── data/
│   ├── raw/                # Original synthetic data
│   └── processed/          # Cleaned data after preprocessing
├── tests/
│   └── test_pipeline.py    # 20 comprehensive tests
├── main.py                 # Orchestrate all steps
├── requirements.txt        # Python dependencies
├── README.md              # Project overview
└── SETUP.md              # This file
```

---

## 🔧 Individual Steps (If Needed)

You can run individual pipeline steps separately:

### Step 1: Generate Synthetic Data
```powershell
python src/data_collection.py
```
Output: `data/raw/expenses_raw.csv` (250 records)

### Step 2: Preprocess Data
```powershell
python src/preprocess.py
```
Output: `data/processed/expenses_clean.csv`

### Step 3: Train ML Model
```powershell
python models/train_model.py
```
Output: 
- `models/expense_classifier.pkl` (trained model)
- `models/vectorizer.pkl` (TF-IDF vectorizer)

### Step 4: Load Data into Database
```powershell
python database/load_data.py
```
Output: `database/expenses.db` (SQLite database with predictions)

### Step 5: Start Dashboard
```powershell
streamlit run app/dashboard.py
```

---

## ✅ Testing

Run the complete test suite to validate all components (20 tests):

```powershell
python tests/test_pipeline.py
```

**Expected output:**
```
Ran 20 tests in ~0.8s
✓ ALL TESTS PASSED!
```

**Test coverage:**
- ✓ Data Collection (3 tests)
- ✓ Data Preprocessing (5 tests)
- ✓ Model Training (4 tests)
- ✓ Prediction Module (3 tests)
- ✓ SQL Integration (5 tests)

---

## 📊 Dashboard Features

### 📝 Add Expense Tab
- Input date, amount, and description
- AI automatically predicts the category
- Real-time database updates
- View quick summary statistics

### 📋 All Expenses Tab
- Browse all recorded expenses
- Filter by category
- View actual vs. predicted categories
- Currency-formatted amounts

### 📊 Analytics Tab
- **Pie chart** — Spending distribution by category
- **Trend chart** — Monthly spending over time
- **Bar chart** — Category-wise spending breakdown
- **Summary metrics** — Total, average, highest expense
- **Category breakdown table** — Detailed stats per category

---

## 🤖 ML Model Details

**Algorithm:** Multinomial Naive Bayes  
**Vectorization:** TF-IDF (100 features)  
**Training Data:** 250 synthetic expense records  
**Test Accuracy:** 90%

**Categories (8 fixed):**
- Food
- Travel
- Bills
- Shopping
- Entertainment
- Groceries
- Health
- Other

---

## 🐛 Troubleshooting

### Issue: "Python not found"
**Solution:** Make sure Python is in your PATH. Reinstall from [python.org](https://www.python.org/downloads/) and check "Add Python to PATH".

### Issue: "Module not found" when running scripts
**Solution:** Make sure virtual environment is activated:
```powershell
.\venv\Scripts\activate
```

### Issue: "Port 8501 already in use" (Streamlit error)
**Solution:** Stop the other Streamlit process or use a different port:
```powershell
streamlit run app/dashboard.py --server.port 8502
```

### Issue: Database file is missing after git clone
**Solution:** This is expected. Run `python main.py` to regenerate the database with trained model and data.

### Issue: `.pkl` model files missing
**Solution:** This is expected. Run `python models/train_model.py` to retrain the model locally.

---

## 📝 Development Notes

### Adding New Expenses
- Use the dashboard input form (easiest method)
- Or directly insert into database using `database/db_operations.py`

### Retraining the Model
To retrain with new data:
1. Update or replace `data/processed/expenses_clean.csv`
2. Run `python models/train_model.py`
3. Run `python database/load_data.py` to update predictions

### Modifying Categories
**⚠️ Important:** Categories are fixed in this version. To add/remove categories:
1. Update the category list in `src/data_collection.py`
2. Retrain the model: `python models/train_model.py`
3. Reload database: `python database/load_data.py`

---

## 🔄 Git Workflow

### Pulling Latest Changes
```powershell
git pull origin main
pip install -r requirements.txt  # In case dependencies changed
```

### Making Changes
```powershell
git checkout -b feature/your-feature-name
# Make your changes
git add .
git commit -m "Description of changes"
git push origin feature/your-feature-name
```

### Creating a Pull Request
- Go to [GitHub repository](https://github.com/Arunachalam101/SmartSpend-AI)
- Click "New Pull Request"
- Select your branch and describe your changes

---

## 📚 Documentation

| File | Purpose |
|------|---------|
| `README.md` | Project overview and architecture |
| `SETUP.md` | This setup guide for team members |
| `main.py` | Main orchestration script with detailed comments |
| `src/*.py` | Individual step scripts with docstrings |
| `tests/test_pipeline.py` | Test examples and validation |

---

## 🤝 Team Roles & Responsibilities

| Component | Owner | Status |
|-----------|-------|--------|
| Data Collection | Data Team | ✅ Complete |
| Preprocessing | Data Team | ✅ Complete |
| Model Training | ML Team | ✅ Complete |
| Database Design | Backend Team | ✅ Complete |
| Dashboard | Frontend Team | ✅ Complete |
| Testing | QA Team | ✅ Complete |

---

## 📞 Getting Help

1. **Check the README.md** for project overview
2. **Review test files** to understand data flow
3. **Check docstrings** in Python files for function details
4. **Run `python main.py` with `-v`** for verbose output (if implemented)

---

## ✨ Next Steps

After setup, you can:
- [ ] Add test expenses via the dashboard
- [ ] Experiment with the ML model accuracy
- [ ] Explore the database with `show_database.py` (if available)
- [ ] Review and improve model performance
- [ ] Add new features or categories

---

**Last Updated:** September 2026  
**Repository:** [SmartSpend-AI](https://github.com/Arunachalam101/SmartSpend-AI)  
**Questions?** Check the issues section on GitHub or contact the team lead.
