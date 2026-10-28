"""
FixMyText AI — Evaluate and compare all trained models.

Usage: python ml/evaluate_models.py

Loads saved metric files from artifacts/ and prints a comparison table.
"""

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "artifacts"


def main():
    files = {
        "Logistic Regression": "baseline_metrics.json",
        "LSTM": "lstm_metrics.json",
        "BiLSTM": "bilstm_metrics.json",
    }

    results = []
    for name, fname in files.items():
        path = ARTIFACTS / fname
        if path.exists():
            m = json.loads(path.read_text(encoding="utf-8"))
            results.append((name, m))
            print(f"[OK] Found {name} metrics")
        else:
            print(f"[--] {name} metrics not found ({fname})")

    if not results:
        print("\nNo trained models found. Run training scripts first:")
        print("  python ml/train_baseline.py")
        print("  python ml/train_lstm.py")
        print("  python ml/train_bilstm.py")
        return

    print("\n" + "=" * 70)
    print(f"{'Model':<25} {'Accuracy':>10} {'Precision':>10} {'Recall':>10} {'F1':>10}")
    print("-" * 70)
    for name, m in results:
        print(f"{name:<25} {m['accuracy']:>10.4f} {m['macro_precision']:>10.4f} "
              f"{m['macro_recall']:>10.4f} {m['macro_f1']:>10.4f}")
    print("=" * 70)

    # Find best by F1
    best_name, best_m = max(results, key=lambda x: x[1]["macro_f1"])
    print(f"\nBest model by Macro-F1: {best_name} ({best_m['macro_f1']:.4f})")
    print("\nNote: All metrics are from a synthetic starter dataset.")
    print("Do not report these as real-world performance figures.")


if __name__ == "__main__":
    main()
