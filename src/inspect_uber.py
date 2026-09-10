import pandas as pd

file_path = "data/raw/twcs/twcs.csv"

columns = [
    "tweet_id",
    "author_id",
    "inbound",
    "text",
    "response_tweet_id",
    "in_response_to_tweet_id",
]

df = pd.read_csv(
    file_path,
    usecols=columns,
    chunksize=100_000
)

uber_rows = []

for chunk in df:
    matches = chunk[
        chunk["author_id"].isin(["Uber_Support"])
    ]

    uber_rows.append(matches)

uber_df = pd.concat(uber_rows, ignore_index=True)

print("Uber support tweets:", len(uber_df))

print("\nSample Uber support messages:\n")

for _, row in uber_df.head(15).iterrows():
    print(f"Tweet ID: {row['tweet_id']}")
    print(f"Text: {row['text']}")
    print(f"Responding to: {row['in_response_to_tweet_id']}")
    print("-" * 70)