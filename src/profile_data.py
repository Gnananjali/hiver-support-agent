import pandas as pd

file_path = "data/raw/twcs/twcs.csv"

brand_counts = {}

for chunk in pd.read_csv(file_path, chunksize=100_000):
    support_tweets = chunk[chunk["inbound"] == False]

    counts = support_tweets["author_id"].value_counts()

    for brand, count in counts.items():
        brand_counts[brand] = brand_counts.get(brand, 0) + count

print("Number of brands:", len(brand_counts))

print("\nTop 20 brands by number of support tweets:")
for brand, count in sorted(
    brand_counts.items(),
    key=lambda x: x[1],
    reverse=True
)[:20]:
    print(f"{brand}: {count}")