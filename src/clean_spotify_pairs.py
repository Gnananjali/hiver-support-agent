import pandas as pd
import html
import re

INPUT_PATH = "data/processed/spotify_pairs.csv"
OUTPUT_PATH = "data/processed/spotify_pairs_clean.csv"


def clean_text(text):
    if pd.isna(text):
        return ""

    text = html.unescape(text)

    text = re.sub(r"https?://\S+", "", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


df = pd.read_csv(INPUT_PATH)

df["customer_message"] = df["customer_message"].apply(clean_text)
df["support_response"] = df["support_response"].apply(clean_text)

df = df[
    (df["customer_message"].str.len() > 0)
    & (df["support_response"].str.len() > 0)
]

df.to_csv(OUTPUT_PATH, index=False)

print("Rows after cleaning:", len(df))
print("Saved to:", OUTPUT_PATH)

print("\nSample cleaned pairs:")
print(
    df[["customer_message", "support_response"]]
    .head(10)
    .to_string(index=False)
)