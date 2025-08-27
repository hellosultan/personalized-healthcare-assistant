import os, duckdb, pandas as pd

PARQUET = "data/synthetic"
OUT_DB  = "data/features.duckdb"
con = duckdb.connect(OUT_DB)

con.execute(f"""
CREATE OR REPLACE TABLE asthma_features AS
SELECT
  patient_id,
  age,
  gender,
  bmi,
  smoking_status,
  (smoking_status != 'Never')::INT AS smoker_flag,
  activity_level,
  environment,
  comorbidity,
  eosinophils,
  er_visits,
  fev1,
  risk_score,
  control_status,
  CASE
    WHEN bmi < 18.5 THEN 'Underweight'
    WHEN bmi < 25   THEN 'Normal'
    WHEN bmi < 30   THEN 'Overweight'
    ELSE 'Obese'
  END AS bmi_category,
  year, month
FROM read_parquet('{PARQUET}/year=*/month=*/part-*.parquet');
""")

print("✅ features table created")
print(con.execute("SELECT COUNT(*) FROM asthma_features").fetchone())
con.close()