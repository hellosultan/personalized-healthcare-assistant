import sqlite3

DB_PATH = "data/EHR.db"

def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # List tables
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print("Tables:", cur.fetchall())

    # Preview sample rows
    cur.execute("SELECT * FROM asthma_records LIMIT 5;")
    rows = cur.fetchall()
    print("\nSample rows from asthma_records:")
    for r in rows:
        print(r)

    conn.close()

if __name__ == "__main__":
    main()
