import pandas as pd


HISTORICAL_FILE = "data/processed/spotify_pairs_clean.csv"
GOLDEN_FILE = "evaluation/golden_set.csv"
TRAINING_FILE = "evaluation/training_candidates.csv"


def normalize_text(text):
    return str(text).strip().lower()


def main():
    historical = pd.read_csv(HISTORICAL_FILE)
    golden = pd.read_csv(GOLDEN_FILE)
    training = pd.read_csv(TRAINING_FILE)

    historical_messages = set(
        historical["customer_message"]
        .dropna()
        .map(normalize_text)
    )

    golden_messages = set(
        golden["customer_message"]
        .dropna()
        .map(normalize_text)
    )

    training_messages = set(
        training["customer_message"]
        .dropna()
        .map(normalize_text)
    )

    golden_in_historical = golden_messages & historical_messages
    golden_in_training = golden_messages & training_messages

    print("=" * 60)
    print("DATA OVERLAP CHECK")
    print("=" * 60)

    print(f"Historical messages: {len(historical_messages)}")
    print(f"Golden Set messages: {len(golden_messages)}")
    print(f"Training messages: {len(training_messages)}")

    print()
    print(
        "Golden Set messages found in historical data:",
        len(golden_in_historical)
    )

    print(
        "Golden Set messages found in training set:",
        len(golden_in_training)
    )

    print()

    if golden_in_training:
        print("WARNING: Golden Set / training overlap detected.")

        for message in list(golden_in_training)[:10]:
            print(f"- {message}")

    else:
        print("Good: no Golden Set / training message overlap detected.")


if __name__ == "__main__":
    main()