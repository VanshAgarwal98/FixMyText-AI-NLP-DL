"""
FixMyText AI — Dataset preparation and analysis.

Usage: python ml/prepare_dataset.py

Validates the CSV, prints statistics, and checks for common issues
like duplicates and class imbalance.
"""

from pathlib import Path
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.preprocessing import normalize_text


def main():
    csv_path = ROOT / "data" / "complaints.csv"
    if not csv_path.exists():
        raise SystemExit(f"Dataset not found at {csv_path}")

    df = pd.read_csv(csv_path)
    print(f"Raw rows: {len(df)}")
    print(f"Columns:  {list(df.columns)}")

    # Clean
    df = df.dropna(subset=["text", "category"])
    df["text_clean"] = df["text"].apply(normalize_text)
    df = df[df["text_clean"].str.len() > 0]

    print(f"\nAfter cleaning: {len(df)} rows")
    print(f"Categories ({df['category'].nunique()}):")
    for cat, count in df["category"].value_counts().items():
        print(f"  {cat:20s}  {count:4d}")

    # Check duplicates
    dups = df.duplicated(subset=["text_clean"], keep=False)
    n_dup = dups.sum()
    if n_dup:
        print(f"\n[WARN] {n_dup} duplicate texts found (after normalisation):")
        for _, row in df[dups].head(10).iterrows():
            print(f"  [{row['category']}] {row['text_clean'][:80]}")
    else:
        print("\n[OK] No duplicate texts found.")

    # Length stats
    df["length"] = df["text_clean"].str.split().str.len()
    print(f"\nText length (words):  min={df['length'].min()}, "
          f"mean={df['length'].mean():.1f}, max={df['length'].max()}")

    # Class balance
    counts = df["category"].value_counts()
    ratio = counts.max() / counts.min()
    if ratio > 3:
        print(f"\n[WARN] Class imbalance ratio {ratio:.1f}:1 - consider adding more examples to smaller classes.")
    else:
        print(f"\n[OK] Class balance ratio {ratio:.1f}:1 - acceptable.")

    print("\nDataset preparation complete.")


if __name__ == "__main__":
    main()
