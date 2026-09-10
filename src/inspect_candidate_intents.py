import pandas as pd

INPUT_PATH = "data/processed/spotify_pairs_clean.csv"

df = pd.read_csv(INPUT_PATH)

df["text"] = df["customer_message"].fillna("").str.lower()


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

    "premium_subscription": [
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


for intent, keywords in intents.items():

    mask = False

    for keyword in keywords:
        mask = mask | df["text"].str.contains(
            keyword,
            regex=False,
            na=False
        )

    matches = df[mask]

    print("\n" + "=" * 70)
    print(intent.upper())
    print("Matching messages:", len(matches))
    print("=" * 70)

    if len(matches) == 0:
        print("No examples found.")
        continue

    examples = matches.sample(
        n=min(5, len(matches)),
        random_state=42
    )

    for i, (_, row) in enumerate(examples.iterrows(), start=1):

        print(f"\nExample {i}:")
        print("Customer:", row["customer_message"])
        print("Support :", row["support_response"])