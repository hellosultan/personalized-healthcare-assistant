import duckdb, os, pandas as pd

parquet_root = "data/synthetic"
con = duckdb.connect()

q = f"""
SELECT CASE
    WHEN age <= 18 THEN '0-18'
    WHEN age <= 35 THEN '19-35'
    WHEN age <= 50 THEN '36-50'
    WHEN age <= 70 THEN '51-70'
    ELSE '71+'
END AS age_group,
COUNT(*) AS n
FROM read_parquet('{parquet_root}/year=*/month=*/part-*.parquet')
GROUP BY 1 ORDER BY 1
"""
df = con.execute(q).fetch_df()

os.makedirs("reports/figures", exist_ok=True)
df.to_csv("reports/figures/age_distribution.csv", index=False)
print(df)
print("✅ Wrote reports/figures/age_distribution.csv")

con.close()