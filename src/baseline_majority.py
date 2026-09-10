import pandas as pd
from sklearn.metrics import accuracy_score, f1_score


INPUT_FILE = "evaluation/golden_set.csv"


def main():
    # Load the finalized Golden Set
    df = pd.read_csv(INPUT_FILE)

    # Find the most common intent
    majority_intent = df["golden_intent"].mode()[0]

    # Predict the same intent for every example
    predictions = [majority_intent] * len(df)

    # Calculate metrics
    accuracy = accuracy_score(
        df["golden_intent"],
        predictions
    )

    macro_f1 = f1_score(
        df["golden_intent"],
        predictions,
        average="macro",
        zero_division=0
    )

    print("=" * 60)
    print("BASELINE #1 — MAJORITY CLASS")
    print("=" * 60)

    print(f"Total examples: {len(df)}")
    print(f"Majority intent: {majority_intent}")
    print(f"Majority examples: {(df['golden_intent'] == majority_intent).sum()}")

    print()
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Macro F1: {macro_f1:.4f}")


if __name__ == "__main__":
    main()