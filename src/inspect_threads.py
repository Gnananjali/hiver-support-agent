import pandas as pd

file_path = "data/raw/twcs/twcs.csv"

df = pd.read_csv(file_path, nrows=100_000)

brand = "sprintcare"

brand_tweets = df[df["author_id"] == brand]

print(f"Number of {brand} tweets:", len(brand_tweets))

print("\nSample brand tweets:")
print(brand_tweets[["tweet_id", "text", "response_tweet_id", "in_response_to_tweet_id"]].head(10).to_string(index=False))