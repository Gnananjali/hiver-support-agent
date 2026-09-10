import pandas as pd

FILE_PATH = "data/raw/twcs/twcs.csv"
OUTPUT_PATH = "data/processed/spotify_pairs.csv"
CHUNK_SIZE = 100_000

# ---------------------------------------------------------
# Pass 1: Find Spotify support tweets and their parent IDs
# ---------------------------------------------------------

support_rows = []

for chunk in pd.read_csv(
    FILE_PATH,
    usecols=["tweet_id", "author_id", "inbound", "text", "in_response_to_tweet_id"],
    chunksize=CHUNK_SIZE,
):
    spotify_support = chunk[
        (chunk["author_id"] == "SpotifyCares")
        & (chunk["inbound"] == False)
        & (chunk["in_response_to_tweet_id"].notna())
    ]

    support_rows.append(
        spotify_support[
            ["tweet_id", "text", "in_response_to_tweet_id"]
        ]
    )

support_df = pd.concat(support_rows, ignore_index=True)

print("Spotify support replies found:", len(support_df))


# ---------------------------------------------------------
# Pass 2: Find the customer tweets those replies answered
# ---------------------------------------------------------

parent_ids = set(support_df["in_response_to_tweet_id"])

customer_rows = []

for chunk in pd.read_csv(
    FILE_PATH,
    usecols=["tweet_id", "author_id", "inbound", "text"],
    chunksize=CHUNK_SIZE,
):
    customers = chunk[
        (chunk["inbound"] == True)
        & (chunk["tweet_id"].isin(parent_ids))
    ]

    customer_rows.append(customers)

customer_df = pd.concat(customer_rows, ignore_index=True)

print("Matching customer messages found:", len(customer_df))


# ---------------------------------------------------------
# Join customer messages with Spotify's responses
# ---------------------------------------------------------

pairs = support_df.merge(
    customer_df[["tweet_id", "author_id", "text"]],
    left_on="in_response_to_tweet_id",
    right_on="tweet_id",
    suffixes=("_support", "_customer"),
)

pairs = pairs.rename(
    columns={
        "tweet_id_customer": "customer_tweet_id",
        "tweet_id_support": "support_tweet_id",
        "author_id": "customer_author_id",
        "text_customer": "customer_message",
        "text_support": "support_response",
    }
)

pairs = pairs[
    [
        "customer_tweet_id",
        "support_tweet_id",
        "customer_author_id",
        "customer_message",
        "support_response",
    ]
]

# Remove rows with missing text
pairs = pairs.dropna(
    subset=["customer_message", "support_response"]
)

# Remove duplicate support replies
pairs = pairs.drop_duplicates(
    subset=["support_tweet_id"]
)

pairs.to_csv(OUTPUT_PATH, index=False)

print("Final customer-support pairs:", len(pairs))
print("Saved to:", OUTPUT_PATH)

print("\nSample pairs:")
print(pairs[["customer_message", "support_response"]].head(10).to_string(index=False))