import pandas as pd

file_path = "data/raw/twcs/twcs.csv"

candidates = [
    "AmazonHelp",
    "AppleSupport",
    "Uber_Support",
    "SpotifyCares",
]

# Read only the columns we need.
columns = [
    "tweet_id",
    "author_id",
    "inbound",
    "text",
    "in_response_to_tweet_id",
]

# Store support tweets for our candidate brands.
support_tweets = []

for chunk in pd.read_csv(
    file_path,
    usecols=columns,
    chunksize=100_000
):
    matches = chunk[
        chunk["author_id"].isin(candidates)
        & (chunk["inbound"] == False)
    ]

    support_tweets.append(matches)

support_df = pd.concat(support_tweets, ignore_index=True)

# Create a lookup from tweet ID to tweet information.
all_tweets = {}

for chunk in pd.read_csv(
    file_path,
    usecols=columns,
    chunksize=100_000
):
    for _, row in chunk.iterrows():
        all_tweets[row["tweet_id"]] = {
            "author_id": row["author_id"],
            "inbound": row["inbound"],
            "text": row["text"],
        }

print("\nUsable customer → support interactions")
print("-" * 60)

for brand in candidates:
    brand_support = support_df[
        support_df["author_id"] == brand
    ]

    matched_customer_messages = 0

    for _, support in brand_support.iterrows():
        parent_id = support["in_response_to_tweet_id"]

        if pd.isna(parent_id):
            continue

        parent = all_tweets.get(parent_id)

        if parent and parent["inbound"] == True:
            matched_customer_messages += 1

    print(f"\n{brand}")
    print(f"  Support tweets: {len(brand_support)}")
    print(f"  Customer messages with direct support reply: {matched_customer_messages}")