import pandas as pd

INPUT_PATH = "data/processed/spotify_pairs_clean.csv"
OUTPUT_PATH = "evaluation/golden_candidates.csv"

df = pd.read_csv(INPUT_PATH)


# Candidate keywords for finding examples.
# These are only used for sampling.
intent_keywords = {
    "account_access": [
        "login",
        "log in",
        "logged out",
        "password",
        "sign in",
    ],

    "premium_subscription": [
        "premium",
        "subscription",
        "cancel premium",
    ],

    "billing_payment": [
        "payment",
        "charged",
        "charge",
        "billing",
        "refund",
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
        "missing songs",
        "discover weekly",
        "library",
    ],

    "download_offline": [
        "download",
        "downloaded",
        "offline",
    ],

    "feature_feedback": [
        "feature",
        "suggestion",
        "would be nice",
        "please add",
        "can you add",
        "bring back",
    ],
}


df["text_lower"] = (
    df["customer_message"]
    .fillna("")
    .str.lower()
)


samples = []

for intent, keywords in intent_keywords.items():

    mask = False

    for keyword in keywords:
        mask = mask | df["text_lower"].str.contains(
            keyword,
            regex=False,
            na=False
        )

    matches = df[mask].copy()

    # Random but reproducible sample
    sample_size = min(20, len(matches))

    sampled = matches.sample(
        n=sample_size,
        random_state=42
    )

    sampled["candidate_intent"] = intent

    samples.append(
        sampled[
            [
                "candidate_intent",
                "customer_message",
                "support_response",
            ]
        ]
    )


golden_candidates = pd.concat(
    samples,
    ignore_index=True
)

golden_candidates.insert(
    0,
    "example_id",
    range(1, len(golden_candidates) + 1)
)

# Empty column for our future manual label.
golden_candidates["golden_intent"] = ""

# Empty column for explaining difficult decisions.
golden_candidates["label_notes"] = ""


golden_candidates.to_csv(
    OUTPUT_PATH,
    index=False
)

print("Golden-set candidates created.")
print("Total examples:", len(golden_candidates))
print("Saved to:", OUTPUT_PATH)

print("\nExamples per candidate intent:")
print(
    golden_candidates["candidate_intent"]
    .value_counts()
    .sort_index()
)