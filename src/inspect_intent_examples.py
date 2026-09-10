import pandas as pd

INPUT_PATH = "data/processed/spotify_pairs_clean.csv"

df = pd.read_csv(INPUT_PATH)

df["text"] = df["customer_message"].fillna("").str.lower()

categories = {
    "account_login": [
        "login",
        "log in",
        "logged out",
        "password",
        "sign in",
    ],
    "premium": [
        "premium",
        "subscription",
    ],
    "family": [
        "family plan",
        "family account",
        "family premium",
    ],
    "student": [
        "student",
        "student discount",
    ],
    "payment_billing": [
        "payment",
        "credit card",
        "charged",
        "charge",
        "billing",
        "refund",
    ],
    "app_technical": [
        "app",
        "crash",
        "error",
        "not working",
    ],
    "playback": [
        "play",
        "playing",
        "pause",
        "shuffle",
        "repeat",
    ],
    "playlist_library": [
        "playlist",
        "album",
        "library",
        "saved",
    ],
    "download_offline": [
        "download",
        "offline",
    ],
    "device_platform": [
        "iphone",
        "android",
        "windows",
        "mac",
        "apple watch",
        "web player",
    ],
}

for category, keywords in categories.items():

    mask = False

    for keyword in keywords:
        mask = mask | df["text"].str.contains(
            keyword,
            regex=False,
            na=False
        )

    examples = df[mask].drop_duplicates(
        subset=["customer_message"]
    ).head(10)

    print("\n" + "=" * 70)
    print(category.upper())
    print("=" * 70)

    for i, row in examples.iterrows():
        print("\nCUSTOMER:")
        print(row["customer_message"])

        print("SPOTIFY:")
        print(row["support_response"])