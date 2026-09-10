import pandas as pd


HISTORICAL_FILE = "data/processed/spotify_pairs_clean.csv"
GOLDEN_FILE = "evaluation/golden_set.csv"
TRAINING_FILE = "evaluation/training_candidates.csv"

SAFE_TRAINING_FILE = "evaluation/training_clean.csv"
SAFE_RETRIEVAL_FILE = "data/processed/spotify_retrieval_safe.csv"


def normalize_text(text):
    return str(text).strip().lower()


def main():
    historical = pd.read_csv(HISTORICAL_FILE)
    golden = pd.read_csv(GOLDEN_FILE)
    training = pd.read_csv(TRAINING_FILE)

    golden_messages = set(
        golden["customer_message"]
        .dropna()
        .map(normalize_text)
    )

    # ---------------------------------------------------------
    # 1. Remove Golden Set examples from the training set
    # ---------------------------------------------------------

    training_normalized = training["customer_message"].map(
        normalize_text
    )

    safe_training = training[
        ~training_normalized.isin(golden_messages)
    ].copy()

    # ---------------------------------------------------------
    # 2. Remove Golden Set examples from retrieval corpus
    # ---------------------------------------------------------

    historical_normalized = historical["customer_message"].map(
        normalize_text
    )

    safe_retrieval = historical[
        ~historical_normalized.isin(golden_messages)
    ].copy()

    # ---------------------------------------------------------
    # Save the new datasets
    # ---------------------------------------------------------

    safe_training.to_csv(
        SAFE_TRAINING_FILE,
        index=False
    )

    safe_retrieval.to_csv(
        SAFE_RETRIEVAL_FILE,
        index=False
    )

    print("=" * 60)
    print("SAFE DATASETS CREATED")
    print("=" * 60)

    print()
    print(f"Original training examples: {len(training)}")
    print(f"Safe training examples: {len(safe_training)}")
    print(f"Training examples removed: {len(training) - len(safe_training)}")

    print()

    print(f"Original retrieval examples: {len(historical)}")
    print(f"Safe retrieval examples: {len(safe_retrieval)}")
    print(
        f"Retrieval examples removed: "
        f"{len(historical) - len(safe_retrieval)}"
    )

    print()

    print(f"Saved: {SAFE_TRAINING_FILE}")
    print(f"Saved: {SAFE_RETRIEVAL_FILE}")


if __name__ == "__main__":
    main()