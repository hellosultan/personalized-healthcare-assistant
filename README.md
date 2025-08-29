# 🏥 Personalized Healthcare Assistant

## 🌟 Project Overview
This project simulates a **Big Data healthcare analytics pipeline** using synthetic asthma patient records.  
It demonstrates how to generate, store, and analyze **millions of patient records** with industry-ready tools like **Parquet, DuckDB, and Python**.  
> **Note:** All results and figures in this project are based on **synthetic data**.  
> They illustrate pipeline design and analysis techniques, not real patient outcomes.

**Key features:**
- Synthetic **5M+ patient records** generated (scalable to 50M+)  
- Data stored as **partitioned Parquet** (year/month)  
- Queried with **DuckDB** (SQL-on-files, industry standard)  
- Analytics in **Python + Pandas + Matplotlib**  
- Exported **KPIs, charts, and model metrics** for business insights  

---

## 🚀 Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/hellosultan/personalized-healthcare-assistant.git
cd personalized-healthcare-assistant
````

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Generate synthetic data

```bash
# 1 million rows (~250MB)
python src/sql/generate_synthetic_asthma.py --rows 1000000 --chunk 100000

# 5 million rows (~1.2GB) for full Big Data demo
python src/sql/generate_synthetic_asthma.py --rows 5000000 --chunk 100000
```

### 4. Run analytics

Launch Jupyter Notebook:

```bash
jupyter notebook notebooks/analysis.ipynb
```

Or run scripts directly:

```bash
python src/sql/duck_kpis.py
python src/sql/duck_age_bins.py
python src/sql/duck_bmi_control.py
python src/sql/derive_features.py
python src/sql/train_baseline.py
```

---

## 📊 Features

### ✅ Data Engineering

* Synthetic generator → **partitioned Parquet files** under `data/synthetic/`
* SQLite pipeline (`data/EHR.db`) for smaller datasets
* Feature builder (`derive_features.py`) → ML-ready dataset (`features.duckdb`)

### ✅ Analytics

* DuckDB SQL queries across **millions of rows**
* Feature engineering: BMI categories, smoker flags, comorbidities
* Pandas + Matplotlib for KPIs & charts

### ✅ Machine Learning

* Baseline logistic regression to predict **Poorly Controlled** patients
* ROC-AUC, classification report, confusion matrix
* Feature importance analysis (logistic regression coefficients)

### ✅ Outputs

All results exported to `reports/figures/`:

* KPI CSVs (`*.csv`)
* Charts (`*.png`)
* Model metrics (`model_metrics.json`)

### 📈 Results
* ROC-AUC (baseline logistic regression): 0.955
* This indicates the model can **reliably distinguish poorly controlled asthma patients** from well/partly controlled ones, even on a large synthetic dataset.
* **Confusion matrix** shows the expected imbalance (more well-controlled than poorly controlled), but recall for high-risk patients remains meaningful.
### Key drivers of poor control:
* ER visits, smoking status, and obesity (BMI) → strongly increase risk.
* Higher FEV1 values → protective against poor control.
>️ **Note:** All results are based on **synthetic data**. They illustrate pipeline design and analysis techniques, not real patient outcomes.

### 🔹 Visualizations & Insights

| ROC Curve                                                                                                                        | Confusion Matrix                                                                                                                               |
| -------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| ![ROC Curve](https://raw.githubusercontent.com/hellosultan/personalized-healthcare-assistant/main/reports/figures/roc_curve.png) ROC Curve: Shows model discrimination ability (AUC=0.955). A curve well above the diagonal means the model separates poorly vs well-controlled patients much better than random. | ![Confusion Matrix](https://raw.githubusercontent.com/hellosultan/personalized-healthcare-assistant/main/reports/figures/confusion_matrix.png) Confusion Matrix: Highlights class imbalance — most patients are well-controlled, but the model still identifies a meaningful share of poorly controlled cases.|

| Control Status by Year & Gender                                                                                                                           | Age Distribution                                                                                                                       |
| --------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| ![Control Status](https://raw.githubusercontent.com/hellosultan/personalized-healthcare-assistant/main/reports/figures/control_status_by_year_gender.png) Control Status by Year & Gender: Tracks asthma control trends across time and demographics. Females and males show similar patterns, with most patients remaining well-controlled.| ![Age Dist](https://raw.githubusercontent.com/hellosultan/personalized-healthcare-assistant/main/reports/figures/age_distribution.png) Age Distribution: Synthetic population skews toward adults; elderly and children are underrepresented, which reflects how the dataset was generated.|

| BMI vs Control Status                                                                                                                      | ER Visits Distribution                                                                                                                        |
| ------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------- |
| ![BMI vs Control](https://raw.githubusercontent.com/hellosultan/personalized-healthcare-assistant/main/reports/figures/bmi_by_control.png) BMI vs Control Status: Overweight and obese groups have a higher proportion of poorly controlled patients, consistent with known asthma risk factors. | ![ER Visits](https://raw.githubusercontent.com/hellosultan/personalized-healthcare-assistant/main/reports/figures/er_visits_distribution.png) ER Visits Distribution: Poorly controlled patients account for most ER visits, showing the model captures clinically meaningful utilization patterns.|
 |
| ![Feature Importance](https://raw.githubusercontent.com/hellosultan/personalized-healthcare-assistant/main/reports/figures/feature_importance.png)|

	•	Feature Importance: Logistic regression coefficients indicate which features drive predictions.
	•	Positive drivers (higher risk): ER visits, smoking, obesity.
	•	Negative drivers (protective): Higher lung function (FEV1), normal BMI.

### 📂 KPI CSVs

* [Control Status by Year & Gender](reports/figures/control_status_by_year_gender.csv)
* [Age Distribution](reports/figures/age_distribution.csv)
* [BMI vs Control](reports/figures/bmi_by_control.csv)
* [ER Visits Distribution](reports/figures/er_visits_distribution.csv)
* [Feature Importance](reports/figures/feature_importance.csv)
* [Model Metrics](reports/figures/model_metrics.json)

---

## 🧰 Tech Stack

* **Python** (pandas, numpy, matplotlib, seaborn)
* **DuckDB** (SQL on Parquet)
* **PyArrow** (Parquet I/O)
* **SQLite** (prototype DB)
* **scikit-learn** (baseline ML)
* Optional: **PySpark** (for >50M rows)

---

## 📌 Business Relevance

* Simulates a **personalized healthcare assistant** pipeline
* Identifies **high-risk patients** (poorly controlled asthma)
* Links **BMI, smoking, and comorbidities** to outcomes
* Demonstrates **scalable, end-to-end Big Data analytics + ML skills**
* Outputs can support **population health monitoring** and **clinical decision support**

---

## 🔮 Future Work

* Integrate **streaming ingestion** (Kafka, real-time IoT data)
* Deploy predictive model as an **API (FastAPI/Flask)**
* Add **dashboard** in Power BI / Tableau / Streamlit\*\*
* Extend dataset with other chronic diseases (diabetes, COPD)

---

## 👨‍💻 Author

**Sultan Muhammad**
[LinkedIn](https://linkedin.com/in/hellosultan) | [GitHub](https://github.com/hellosultan)


