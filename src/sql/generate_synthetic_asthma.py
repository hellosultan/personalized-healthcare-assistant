import os
import math
import argparse
import numpy as np
import pandas as pd

# Reproducible RNG
RNG = np.random.default_rng(42)

GENDERS = np.array(["Male", "Female"])
SMOKING = np.array(["Never", "Former", "Current"])
TRIGGERS = np.array([None, "Dust", "Pollen", "Multiple"])
ACTIVITY = np.array(["Sedentary", "Moderate", "Active"])
ENV = np.array(["Indoor", "Outdoor"])
CONTROL = np.array([None, "Well Controlled", "Partly Controlled", "Poorly Controlled"])
COMORB = np.array([None, "Diabetes", "Hypertension", "Both"])

def synth_chunk(start_id: int, rows: int) -> pd.DataFrame:
    # Core distributions (lightly realistic)
    age = RNG.integers(5, 90, size=rows)
    gender = RNG.choice(GENDERS, size=rows, p=[0.5, 0.5])
    bmi = np.round(RNG.normal(27.5, 5.0, size=rows).clip(14, 55), 1)
    smoking_status = RNG.choice(SMOKING, size=rows, p=[0.65, 0.25, 0.10])
    pets = RNG.integers(0, 4, size=rows)  # household pets count
    trigger = RNG.choice(TRIGGERS, size=rows, p=[0.25, 0.30, 0.30, 0.15])
    activity_level = RNG.choice(ACTIVITY, size=rows, p=[0.45, 0.40, 0.15])
    lifestyle_env = RNG.choice(ENV, size=rows, p=[0.6, 0.4])
    comorbidity = RNG.choice(COMORB, size=rows, p=[0.65, 0.12, 0.18, 0.05])

    # Pulmonary measures (toy)
    fev1 = np.round(RNG.normal(3.2, 0.8, size=rows).clip(0.5, 6.0), 2)
    eos = np.round(RNG.normal(0.35, 0.15, size=rows).clip(0.05, 2.0), 2)  # eosinophils (x10^9/L)
    er_visits = RNG.poisson(lam=0.4, size=rows).clip(0, 10)

    # Derived “control” status influenced by features (toy heuristic)
    risk_score = (
        (bmi > 30).astype(int) * 0.2 +
        (smoking_status == "Current").astype(int) * 0.25 +
        (eos > 0.5).astype(int) * 0.25 +
        (er_visits >= 2).astype(int) * 0.3
    )
    control_status = np.where(risk_score > 0.6, "Poorly Controlled",
                        np.where(risk_score > 0.35, "Partly Controlled",
                                 "Well Controlled"))
    # Sprinkle Nones
    mask_none = RNG.random(rows) < 0.08
    control_status = np.where(mask_none, None, control_status)

    # Patient IDs & dates (2023–2025 monthly spread)
    start_num = start_id
    pid = np.array([f"ASTH{start_num + i:06d}" for i in range(rows)])
    # monthly partition keys
    years = RNG.choice([2023, 2024, 2025], size=rows, p=[0.25, 0.45, 0.30])
    months = RNG.integers(1, 13, size=rows)

    df = pd.DataFrame({
        "patient_id": pid,
        "age": age,
        "gender": gender,
        "bmi": bmi,
        "smoking_status": smoking_status,
        "pets": pets,
        "trigger": trigger,
        "activity_level": activity_level,
        "environment": lifestyle_env,
        "comorbidity": comorbidity,
        "eosinophils": eos,
        "er_visits": er_visits,
        "fev1": fev1,
        "risk_score": np.round(risk_score, 2),
        "control_status": control_status,
        "year": years,
        "month": months
    })
    return df

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", type=int, default=1_000_000, help="Total rows to generate")
    ap.add_argument("--chunk", type=int, default=100_000, help="Rows per parquet file")
    ap.add_argument("--out", type=str, default="data/synthetic", help="Output root folder for partitioned Parquet")
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    written = 0
    next_id = 0
    total_chunks = math.ceil(args.rows / args.chunk)

    print(f"[GEN] Target rows={args.rows:,}, chunk={args.chunk:,}, chunks≈{total_chunks}")
    while written < args.rows:
        n = min(args.chunk, args.rows - written)
        df = synth_chunk(start_id=next_id, rows=n)

        # Partitioned write: year=YYYY/month=MM
        # (DuckDB/PySpark can glob-read these)
        for (y, m), g in df.groupby(["year", "month"]):
            out_dir = os.path.join(args.out, f"year={y}", f"month={m:02d}")
            os.makedirs(out_dir, exist_ok=True)
            # unique-ish filename
            fname = os.path.join(out_dir, f"part-{next_id:07d}.parquet")
            g.to_parquet(fname, index=False)
        written += n
        next_id += n
        print(f"[GEN] Wrote chunk rows={n:,} | cumulative={written:,}/{args.rows:,}")

    print(f"[DONE] Partitioned Parquet under {args.out}")

if __name__ == "__main__":
    main()