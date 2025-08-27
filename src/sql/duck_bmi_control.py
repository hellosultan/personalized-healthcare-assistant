import duckdb, os, pandas as pd

parquet_root = "data/synthetic"
con = duckdb.connect()

q = f"""
SELECT
  CASE
    WHEN bmi < 18.5 THEN 'Underweight'
    WHEN bmi < 25   THEN 'Normal'
    WHEN bmi < 30   THEN 'Overweight'
    ELSE 'Obese'
  END AS bmi_category,
  control_status,
  COUNT(*) AS n
FROM read_parquet('{parquet_root}/year=*/month=*/part-*.parquet')
GROUP BY 1,2
ORDER BY 1,2
"""
df = con.execute(q).fetch_df()

os.makedirs("reports/figures", exist_ok=True)
df.to_csv("reports/figures/bmi_by_control.csv", index=False)
print(df.head())
print("✅ Wrote reports/figures/bmi_by_control.csv")

con.close()