# src/sql/load_to_sqlite.py
import os
import sqlite3
import pandas as pd

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_FILE = os.path.join(DATA_DIR, "raw", "synthetic_asthma_dataset.csv")
DB_PATH = os.path.join(DATA_DIR, "EHR.db")

def main():
    print("🔹 Loading synthetic asthma dataset...")
    
    # Load CSV
    df = pd.read_csv(RAW_FILE)
    print(f"✅ Loaded {len(df):,} rows and {len(df.columns)} columns")
    
    # Normalize column names
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    
    # Create data/ if missing
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # Connect to SQLite
    conn = sqlite3.connect(DB_PATH)
    
    # Save table
    df.to_sql("asthma_records", conn, if_exists="replace", index=False)
    print("✅ Saved table: asthma_records")
    
    # Create indexes if common columns exist
    cur = conn.cursor()
    if "patient_id" in df.columns:
        cur.execute("CREATE INDEX IF NOT EXISTS idx_patient_id ON asthma_records(patient_id);")
    if "visit_date" in df.columns:
        cur.execute("CREATE INDEX IF NOT EXISTS idx_visit_date ON asthma_records(visit_date);")
    conn.commit()
    
    # Count rows
    cur.execute("SELECT COUNT(*) FROM asthma_records;")
    count = cur.fetchone()[0]
    print(f"📊 Final row count in DB: {count:,}")
    
    conn.close()
    print(f"✅ Database created at {DB_PATH}")

if __name__ == "__main__":
    main()