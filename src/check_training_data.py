import pandas as pd

INPUT_FILE = "data/processed/spotify_pairs_clean.csv"


def main():
    df = pd.read_csv(INPUT_FILE)

    print("=" * 60)
    print("TRAINING DATA CHECK")
    print("=" * 60)

    print(f"Total rows: {len(df)}")

    print()
    print("Columns:")
    print(df.columns.tolist())

    print()
    print("First 3 customer messages:")
    for message in df["customer_message"].head(3):
        print("-", message)


if __name__ == "__main__":
    main()