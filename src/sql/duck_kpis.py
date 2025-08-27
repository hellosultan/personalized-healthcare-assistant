import duckdb, os, pandas as pd
parquet_root = "data/synthetic"
con = duckdb.connect()

q = f"""
SELECT year, gender, control_status, COUNT(*) AS n
FROM read_parquet('{parquet_root}/year=*/month=*/part-*.parquet')
GROUP BY 1,2,3
ORDER BY 1,2,3
"""
df = con.execute(q).fetch_df()
print(df.head())

os.makedirs("reports/figures", exist_ok=True)
df.to_csv("reports/figures/control_status_by_year_gender.csv", index=False)
print("✅ Wrote reports/figures/control_status_by_year_gender.csv")
con.close()