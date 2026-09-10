import pandas as pd

INPUT_FILE = "evaluation/training_candidates.csv"

BATCH_SIZE = 20


def main():
    df = pd.read_csv(INPUT_FILE)

    batch_number = int(input("Enter batch number: "))

    start = (batch_number - 1) * BATCH_SIZE
    end = start + BATCH_SIZE

    batch = df.iloc[start:end]

    print()
    print("=" * 80)
    print(f"TRAINING BATCH {batch_number}")
    print("=" * 80)

    for _, row in batch.iterrows():
        print()
        print(f"ID: {row['customer_tweet_id']}")
        print(f"Customer: {row['customer_message']}")
        print(f"Spotify response: {row['support_response']}")
        print("-" * 80)


if __name__ == "__main__":
    main()