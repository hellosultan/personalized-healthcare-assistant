import os, sqlite3, pandas as pd

DB_PATH = os.path.join("data", "EHR.db")

with sqlite3.connect(DB_PATH) as conn:
    df = pd.read_sql_query("SELECT * FROM asthma_records LIMIT 5;", conn)

print("✅ Preview of asthma_records:")
print(df.head())