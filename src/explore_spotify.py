import pandas as pd
from collections import Counter
import re
import html

INPUT_PATH = "data/processed/spotify_pairs_clean.csv"

df = pd.read_csv(INPUT_PATH)

print("Total interactions:", len(df))


# ---------------------------------------------------------
# Clean customer messages for exploration
# ---------------------------------------------------------

def clean_for_analysis(text):
    if pd.isna(text):
        return ""

    text = html.unescape(text)

    # Remove URLs
    text = re.sub(r"https?://\S+", "", text)

    # Remove @mentions
    text = re.sub(r"@\w+", "", text)

    # Keep only letters, numbers and spaces
    text = re.sub(r"[^a-zA-Z0-9\s']", " ", text)

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)

    return text.lower().strip()


df["analysis_text"] = df["customer_message"].apply(
    clean_for_analysis
)


# ---------------------------------------------------------
# 1. Message length
# ---------------------------------------------------------

df["customer_length"] = df["customer_message"].str.len()

print("\nCustomer message length:")
print(df["customer_length"].describe())


# ---------------------------------------------------------
# 2. Common words
# ---------------------------------------------------------

stop_words = {
    "the", "and", "a", "to", "i", "of", "is", "it",
    "in", "for", "on", "my", "me", "you", "that",
    "this", "with", "but", "have", "are", "be", "was",
    "can", "not", "do", "so", "we", "just", "your",
    "at", "or", "if", "im", "i'm", "its", "from",
    "why", "when", "what", "how", "all", "there",
    "still", "like", "any", "please", "help", "thanks",
    "get", "need", "been", "now"
}

word_counts = Counter()

for message in df["analysis_text"]:
    words = message.split()

    for word in words:
        if word not in stop_words and len(word) > 2:
            word_counts[word] += 1


print("\nTop 30 meaningful customer words:")

for word, count in word_counts.most_common(30):
    print(f"{word}: {count}")


# ---------------------------------------------------------
# 3. Common two-word phrases
# ---------------------------------------------------------

bigram_counts = Counter()

for message in df["analysis_text"]:
    words = [
        word
        for word in message.split()
        if word not in stop_words and len(word) > 2
    ]

    for i in range(len(words) - 1):
        bigram = f"{words[i]} {words[i + 1]}"
        bigram_counts[bigram] += 1


print("\nTop 30 meaningful two-word phrases:")

for phrase, count in bigram_counts.most_common(30):
    print(f"{phrase}: {count}")