import pandas as pd

file_path = "data/raw/twcs/twcs.csv"

candidates = [
    "AmazonHelp",
    "AppleSupport",
    "Uber_Support",
    "SpotifyCares",
]

columns = [
    "tweet_id",
    "author_id",
    "inbound",
    "text",
]

# Find customer tweets that are directly replying to each brand.
brand_customer_messages = {
    brand: [] for brand in candidates
}

for chunk in pd.read_csv(
    file_path,
    usecols=columns,
    chunksize=100_000
):
    for brand in candidates:
        brand_messages = chunk[
            (chunk["inbound"] == True)
            & (chunk["text"].str.contains(
                f"@{brand}",
                case=False,
                na=False
            ))
        ]

        for _, row in brand_messages.iterrows():
            if len(brand_customer_messages[brand]) < 10:
                brand_customer_messages[brand].append(row["text"])

print("\nSample customer messages")
print("=" * 70)

for brand in candidates:
    print(f"\n### {brand}")
    
    for i, message in enumerate(
        brand_customer_messages[brand],
        start=1
    ):
        print(f"{i}. {message}")