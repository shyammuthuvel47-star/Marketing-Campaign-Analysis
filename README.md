# 📊 Marketing Campaign Analysis System

> AI-powered revenue forecasting and profit prediction for Indian beauty brands — built on **166,665 real campaign records** using Random Forest ML, deployed as an interactive Streamlit web app.

---

## 🧠 Project Overview

This end-to-end data science project analyzes marketing campaign performance across three major Indian beauty brands — **Nykaa**, **Purplle**, and **Tira** — to predict campaign revenue and classify campaigns as profitable or loss-making before they run.

The project covers the full pipeline: raw data ingestion → cleaning → EDA → feature engineering → ML modeling → Streamlit deployment.

---

## 🚀 Live App Preview

| Section | Description |
|---|---|
| 🎯 Campaign Setup | Choose brand, type, audience, and customer segment |
| 📡 Channel Mix | Select channels (Email, Facebook, Google, Instagram, WhatsApp, YouTube) |
| 📈 Revenue Predictor | Random Forest Regression — predicts ₹ revenue and estimated ROI |
| 🎯 Profit/Loss Predictor | Random Forest Classification — predicts campaign outcome with confidence % |
| 📋 Campaign Summary | Full parameter table shown after every prediction |
| 🔍 Feature Importance | Visual breakdown of what drives revenue the most |

---

## 📁 Project Structure

```
Marketing-Campaign-Analysis-System/
│
├── Project-3_1.ipynb              # Full analysis notebook (EDA + ML pipeline)
├── Campaign.py                    # Streamlit web app
│
├── nykaa_campaign_data_with_nulls.csv
├── purplle_campaign_data_with_nulls.csv
├── tira_campaign_data_with_nulls.csv
│
├── cleaned_marketing_data.csv     # Generated after preprocessing
│
├── revenue_model.pkl              # Saved Random Forest Regression model
├── profit_model.pkl               # Saved Random Forest Classification model
├── reg_features.pkl               # Feature list for regression
├── clf_features.pkl               # Feature list for classification
├── label_encoder.pkl              # LabelEncoder for categorical columns
│
└── README.md
```

---

## 🗃️ Dataset

| Brand | Records |
|---|---|
| Nykaa | ~55,555 |
| Purplle | ~55,555 |
| Tira | ~55,555 |
| **Total** | **~166,665** |

### Key Columns

| Column | Description |
|---|---|
| `Campaign_Type` | Email / Influencer / Paid Ads / Social Media |
| `Channel_Used` | One or more channels (comma-separated) |
| `Target_Audience` | Audience segment (Youth, Working Women, etc.) |
| `Impressions`, `Clicks`, `Leads`, `Conversions` | Funnel metrics |
| `Acquisition_Cost` | Cost per acquisition (₹) |
| `Revenue` | Revenue generated (₹) — regression target |
| `Engagement_Score` | Campaign engagement index (1–100) |
| `ROI` | Derived: `(Revenue − Acquisition_Cost) / Acquisition_Cost` |
| `Profit_Flag` | Derived: `1` if ROI > 0, else `0` — classification target |

---

## ⚙️ Pipeline Summary

### 1. Data Loading & Merging
- Loaded CSVs for all three brands with `latin-1` encoding
- Added `Brand` column and concatenated into a single 166K-row DataFrame

### 2. Preprocessing
- Numerical columns filled with **median**; `Acquisition_Cost` with **mean**; `Revenue` with **0**
- Categorical columns filled with **mode**; `Date` forward-filled
- `Campaign_ID` dropped (not analytically useful)
- `Date` parsed with `dayfirst=True`; `Duration` cast to `int`

### 3. Feature Engineering
- **ROI** calculated from Revenue and Acquisition_Cost (EDA/display only — excluded from regression features to prevent data leakage)
- **Multi-label channel encoding** via `MultiLabelBinarizer` → 6 binary columns (`C_U_Email`, `C_U_Facebook`, etc.)
- **Profit_Flag** derived from ROI sign (binary target for classification)

### 4. Exploratory Data Analysis
- Average revenue by brand and campaign type
- ROI distribution by campaign type (pie chart)
- Channel performance across 4 metrics: Avg ROI, Avg Revenue, Avg Clicks, Profit Rate

### 5. Machine Learning

#### Regression — Predicting Revenue

| Model | MSE | RMSE | MAE | R² |
|---|---|---|---|---|
| Linear Regression | — | — | — | 0.79 |
| Decision Tree | — | — | — | 0.9979 |
| **Random Forest** ✅ | — | — | — | **0.9993** |

Features used: campaign encodings, funnel metrics, channel flags, Profit_Flag, ROI

#### Classification — Predicting Profit/Loss

| Model | Accuracy | Precision | Recall | F1 |
|---|---|---|---|---|
| Logistic Regression | — | — | — | — |
| Decision Tree | — | — | — | — |
| **Random Forest** ✅ | **Best** | **Best** | **Best** | **Best** |

Features used: campaign encodings, funnel metrics, channel flags (Revenue and ROI excluded to prevent leakage)

### 6. Model Persistence
All models and encoders saved using `pickle` for use in the Streamlit app.

---

## 💻 Streamlit App — `Campaign.py`

### UI Highlights
- Dark theme with custom CSS (`#0d0f14` background, glassmorphism cards)
- Google Fonts: **Inter** + **Space Grotesk**
- Interactive sidebar for all campaign inputs
- Plotly donut chart for channel mix, gauge chart for confidence score, horizontal bar chart for feature importance

### Prediction Flow

**Revenue Prediction (Regression)**
1. User fills sidebar inputs
2. Clicks **📈 Predict Revenue**
3. App displays predicted ₹ revenue + estimated ROI
4. Channel mix donut chart rendered

**Profit/Loss Prediction (Classification)**
1. User fills sidebar inputs
2. Clicks **🎯 Predict Profit/Loss**
3. App shows PROFIT ✓ or LOSS ✗ outcome
4. Confidence gauge + class probability bar chart rendered

---

## 🛠️ Tech Stack

| Category | Tools |
|---|---|
| Data Processing | `pandas`, `numpy` |
| Visualization | `matplotlib`, `seaborn`, `plotly` |
| Machine Learning | `scikit-learn` (LinearRegression, DecisionTree, RandomForest, LogisticRegression, LabelEncoder, MultiLabelBinarizer) |
| Model Saving | `pickle` |
| App Deployment | `streamlit` |
| Fonts | Google Fonts (Inter, Space Grotesk) |

---

## 📦 Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/your-username/marketing-campaign-analysis.git
cd marketing-campaign-analysis
```

### 2. Install dependencies
```bash
pip install pandas numpy matplotlib seaborn scikit-learn streamlit plotly
```

### 3. Run the notebook
Open `Project-3_1.ipynb` in Jupyter or VS Code and run all cells. This will:
- Clean and preprocess the data
- Train all 6 models
- Save `revenue_model.pkl`, `profit_model.pkl`, `reg_features.pkl`, `clf_features.pkl`, and `label_encoder.pkl`

### 4. Launch the Streamlit app
```bash
streamlit run Campaign.py
```

> ⚠️ Make sure all `.pkl` files are in the **same directory** as `Campaign.py` before launching.

---

## 📌 Key Design Decisions

- **ROI excluded from regression features** — ROI is derived from Revenue (the target), so including it would cause data leakage and artificially inflate R².
- **Revenue and ROI excluded from classification features** — Profit_Flag is derived from ROI which is derived from Revenue; including either would cause direct leakage into the classification target.
- **MultiLabelBinarizer for channels** — Campaigns can use multiple channels simultaneously; one-hot encoding a single column would lose this multi-label structure.
- **Static encoding maps in Streamlit** — LabelEncoder order is replicated via sorted dictionaries to ensure consistent predictions without needing to re-fit on the full dataset at inference time.

---

## 🎯 Target Brands

| Brand | Parent | Focus |
|---|---|---|
| **Nykaa** | FSN E-Commerce Ventures | Beauty & wellness e-commerce |
| **Purplle** | Good Glamm Group | Online beauty retail |
| **Tira** | Reliance Retail | Omnichannel beauty retail |

---

## 👤 Author

**Shyam** — Data Analyst | MBA Finance (Pondicherry University) | HCL Technologies  
📍 Chennai, India  
🔗 [LinkedIn](https://linkedin.com/in/your-profile) · [GitHub](https://github.com/your-username)

---

## 📄 License

This project is for academic and portfolio purposes. Dataset is synthetic/educational.
