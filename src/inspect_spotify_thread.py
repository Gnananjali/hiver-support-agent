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

spotify_tweets = []

for chunk in pd.read_csv(
    file_path,
    usecols=columns,
    chunksize=100_000
):
    matches = chunk[
        chunk["author_id"] == "SpotifyCares"
    ]

    spotify_tweets.append(matches)

spotify_df = pd.concat(
    spotify_tweets,
    ignore_index=True
)

# Pick the first Spotify support tweet that has a parent tweet.
support_tweet = spotify_df[
    spotify_df["in_response_to_tweet_id"].notna()
].iloc[0]

parent_id = int(support_tweet["in_response_to_tweet_id"])

print("Spotify support tweet:")
print(support_tweet["text"])

print("\nIt responds to tweet ID:")
print(parent_id)

# Find that parent tweet in the original CSV.
for chunk in pd.read_csv(
    file_path,
    usecols=columns,
    chunksize=100_000
):
    parent = chunk[
        chunk["tweet_id"] == parent_id
    ]

    if not parent.empty:
        print("\nParent tweet:")
        print(parent.iloc[0]["text"])
        print("\nParent author:")
        print(parent.iloc[0]["author_id"])
        print("\nParent inbound:")
        print(parent.iloc[0]["inbound"])
        break