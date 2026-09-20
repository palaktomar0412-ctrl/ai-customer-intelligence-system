# 📊 E-Commerce Sales Analysis & Demand Prediction System

> **A Data Science Mini Project for Sales Analysis and Demand Forecasting**

[![Python](https://img.shields.io/badge/Python-3.13-blue?style=flat&logo=python)](https://python.org)
[![Pandas](https://img.shields.io/badge/Pandas-2.2-orange?style=flat&logo=pandas)](https://pandas.pydata.org)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.6-green?style=flat&logo=scikitlearn)](https://scikit-learn.org)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-3.10-red?style=flat&logo=matplotlib)](https://matplotlib.org)

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Key Features](#key-features)
3. [Tech Stack](#tech-stack)
4. [Project Structure](#project-structure)
5. [Installation Guide](#installation-guide)
6. [Usage Guide](#usage-guide)
7. [Results](#results)
8. [Business Insights](#business-insights)
9. [Future Scope](#future-scope)

---

## 🎯 Project Overview

This project analyzes historical e-commerce sales data and predicts future product demand to help businesses optimize inventory management and increase profits.

### Problem Statement
E-commerce businesses struggle with inventory management due to unpredictable demand patterns. Overstocking leads to increased costs, while understocking results in lost sales. This project uses machine learning to predict demand and provide actionable insights.

### Objectives
1. Analyze historical sales data to identify patterns
2. Perform comprehensive exploratory data analysis (EDA)
3. Build ML models for demand prediction
4. Generate business insights and recommendations
5. Create interactive visualizations

---

## ✨ Key Features

### 1. Data Preprocessing
- Handle missing values using statistical imputation
- Remove duplicate records
- Convert date columns to proper format
- Feature engineering (time-based, categorical encoding)

### 2. Exploratory Data Analysis (EDA)
- Sales trend over time
- Monthly sales analysis
- Top 10 selling products
- Category-wise sales distribution
- Region-wise performance
- Seasonal demand patterns
- Revenue analysis
- Correlation heatmap

### 3. Machine Learning Models
| Model | Type | Use Case |
|-------|------|----------|
| **Linear Regression** | Linear | Baseline model |
| **Random Forest** | Ensemble | Best performance |

### 4. Performance Metrics
- MAE (Mean Absolute Error)
- MSE (Mean Squared Error)
- RMSE (Root Mean Squared Error)
- R² Score (Coefficient of Determination)

### 5. Visualization Dashboard
- Line Charts (trends)
- Bar Charts (comparisons)
- Pie Charts (distributions)
- Heatmaps (correlations)
- Scatter Plots (relationships)

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Language** | Python 3.13 | Core programming |
| **Data Processing** | Pandas, NumPy | Data manipulation |
| **Visualization** | Matplotlib, Seaborn | Charts and graphs |
| **Machine Learning** | Scikit-learn | Model training |
| **Model Persistence** | Joblib | Save/load models |

---

## 📁 Project Structure

```
ecommerce-sales-analysis/
├── data/                          # Datasets
│   ├── ecommerce_sales_raw.csv    # Raw data (with issues)
│   ├── ecommerce_sales_clean.csv  # Clean data
│   └── ecommerce_sales_processed.csv  # Processed data
│
├── scripts/                       # Python scripts
│   ├── generate_dataset.py        # Dataset generator
│   ├── 01_data_preprocessing.py   # Data cleaning
│   ├── 02_eda_visualization.py    # EDA & charts
│   └── 03_ml_model.py            # ML training
│
├── notebooks/                     # Jupyter notebooks
│   └── (to be created)
│
├── outputs/                       # Generated outputs
│   ├── charts/                    # Visualization images
│   ├── models/                    # Trained ML models
│   └── reports/                   # Generated reports
│
├── docs/                          # Documentation
│   ├── abstract.md
│   ├── problem_statement.md
│   ├── methodology.md
│   ├── results.md
│   └── ppt_content.md
│
├── diagrams/                      # Architecture diagrams
│
├── requirements.txt               # Python dependencies
└── README.md                      # Project documentation
```

---

## 🚀 Installation Guide

### Prerequisites
- Python 3.13+
- pip

### Steps
```bash
# Clone the repository
git clone https://github.com/YOUR-USERNAME/ecommerce-sales-analysis.git
cd ecommerce-sales-analysis

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

---

## 📖 Usage Guide

### Step 1: Generate Dataset
```bash
python scripts/generate_dataset.py
```

### Step 2: Run Data Preprocessing
```bash
python scripts/01_data_preprocessing.py
```

### Step 3: Run EDA & Visualization
```bash
python scripts/02_eda_visualization.py
```

### Step 4: Train ML Models
```bash
python scripts/03_ml_model.py
```

### Step 5: View Results
- Charts: `outputs/charts/`
- Models: `outputs/models/`

---

## 📊 Results

### Model Performance
| Model | MAE | RMSE | R² Score |
|-------|-----|------|----------|
| Linear Regression | ~2.1 | ~2.8 | ~0.15 |
| **Random Forest** | **~1.8** | **~2.4** | **~0.25** |

### Key Findings
1. **Top Revenue Category:** Electronics
2. **Best Performing Region:** West
3. **Peak Season:** Winter (Nov-Dec)
4. **Best Model:** Random Forest

---

## 💡 Business Insights

### Recommendations
1. **Inventory Management:** Stock up on top-selling products before peak season
2. **Regional Focus:** Increase marketing in high-performing regions
3. **Seasonal Planning:** Prepare for winter holiday surge
4. **Product Mix:** Focus on high-margin categories
5. **Demand Forecasting:** Use ML predictions for procurement

### Future Demand Predictions
- July 2025: ~500 units
- August 2025: ~520 units
- September 2025: ~480 units
- October 2025: ~550 units
- November 2025: ~650 units
- December 2025: ~700 units

---

## 🔮 Future Scope

1. **Advanced Models:** LSTM, XGBoost, Prophet
2. **Real-time Dashboard:** Streamlit or Dash
3. **API Integration:** REST API for predictions
4. **A/B Testing:** Compare recommendation strategies
5. **Customer Segmentation:** RFM analysis
6. **Price Optimization:** Dynamic pricing models

---

## 📄 Documentation

See `docs/` folder for:
- Abstract
- Problem Statement
- Methodology
- Results & Analysis
- PPT Content (10-12 slides)

---

## 📝 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Data Science Mini Project**
- E-Commerce Sales Analysis & Demand Prediction
- Department of Computer Science and Engineering

---

## 🙏 Acknowledgments

- Pandas documentation for data manipulation
- Scikit-learn for ML algorithms
- Matplotlib & Seaborn for visualizations
- The open-source community
