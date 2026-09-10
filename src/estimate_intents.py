import pandas as pd

INPUT_PATH = "data/processed/spotify_pairs_clean.csv"

df = pd.read_csv(INPUT_PATH)

df["text"] = df["customer_message"].fillna("").str.lower()


# Candidate intent rules
intents = {
    "account_access": [
        "login",
        "log in",
        "logged out",
        "password",
        "sign in",
        "facebook account",
        "hacked account",
    ],

    "subscription_premium": [
        "premium",
        "subscription",
        "cancel premium",
        "premium stopped",
    ],

    "billing_payment": [
        "payment",
        "credit card",
        "charged",
        "charge",
        "billing",
        "refund",
        "paypal",
    ],

    "family_plan": [
        "family plan",
        "family account",
        "family premium",
    ],

    "student_plan": [
        "student",
        "student discount",
        "student price",
    ],

    "app_technical_issue": [
        "app doesn't work",
        "app doesnt work",
        "app not working",
        "app is not working",
        "crash",
        "error",
        "bug",
    ],

    "playback_issue": [
        "shuffle",
        "repeat",
        "can't play",
        "cant play",
        "won't play",
        "wont play",
        "not playing",
        "playback",
    ],

    "content_library": [
        "playlist",
        "album",
        "songs disappeared",
        "missing songs",
        "discover weekly",
        "library",
    ],

    "download_offline": [
        "download",
        "downloaded",
        "offline",
    ],

    "device_platform": [
        "iphone",
        "ios",
        "android",
        "windows",
        "macbook",
        "macos",
        "web player",
        "apple watch",
    ],

    "feature_feedback": [
        "feature",
        "suggestion",
        "would be nice",
        "please add",
        "can you add",
        "bring back",
        "why did you remove",
    ],
}


# ---------------------------------------------------------
# Count matches
# ---------------------------------------------------------

results = []

for intent, keywords in intents.items():

    mask = False

    for keyword in keywords:
        mask = mask | df["text"].str.contains(
            keyword,
            regex=False,
            na=False
        )

    count = mask.sum()

    results.append({
        "intent": intent,
        "matching_messages": count,
        "percentage": round(count / len(df) * 100, 2),
    })


results_df = pd.DataFrame(results)

results_df = results_df.sort_values(
    "matching_messages",
    ascending=False
)

print("\nCandidate intent distribution:")
print(results_df.to_string(index=False))


# ---------------------------------------------------------
# Show overlaps
# ---------------------------------------------------------

df["matched_intents"] = ""

for intent, keywords in intents.items():

    mask = False

    for keyword in keywords:
        mask = mask | df["text"].str.contains(
            keyword,
            regex=False,
            na=False
        )

    df.loc[mask, "matched_intents"] = (
        df.loc[mask, "matched_intents"]
        + intent
        + "|"
    )


overlap_count = (
    df["matched_intents"]
    .str.count(r"\|")
    > 1
).sum()

print("\nMessages matching more than one candidate intent:", overlap_count)