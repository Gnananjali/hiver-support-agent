import pandas as pd

INPUT_FILE = "data/processed/spotify_pairs_clean.csv"
OUTPUT_FILE = "evaluation/training_candidates.csv"

SAMPLES_PER_INTENT = 50


def main():
    df = pd.read_csv(INPUT_FILE)

    print("=" * 60)
    print("CREATING TRAINING SET CANDIDATES")
    print("=" * 60)

    # Take a random sample from the historical data.
    training_candidates = df.sample(
        n=SAMPLES_PER_INTENT * 11,
        random_state=42
    ).copy()

    # Keep only the columns we need for manual labeling.
    training_candidates = training_candidates[
        ["customer_tweet_id", "customer_message", "support_response"]
    ]

    # Add an empty column for our human label.
    training_candidates["training_intent"] = ""

    training_candidates.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(f"Total candidates: {len(training_candidates)}")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()