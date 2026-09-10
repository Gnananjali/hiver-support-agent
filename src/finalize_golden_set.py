import pandas as pd


INPUT_FILE = "evaluation/golden_candidates.csv"
OUTPUT_FILE = "evaluation/golden_set.csv"


# Final labels decided during manual review.
FINAL_LABELS = {
    # Batch 1: 1-20
    1: "account_access",
    2: "account_access",
    3: "account_access",
    4: "account_access",
    5: "account_access",
    6: "account_access",
    7: "account_access",
    8: "premium_subscription",
    9: "account_access",
    10: "account_access",
    11: "account_access",
    12: "account_access",
    13: "other_unclear",
    14: "premium_subscription",
    15: "account_access",
    16: "premium_subscription",
    17: "account_access",
    18: "account_access",
    19: "account_access",
    20: "app_technical_issue",

    # Batch 2: 21-40
    21: "other_unclear",
    22: "student_plan",
    23: "premium_subscription",
    24: "premium_subscription",
    25: "billing_payment",
    26: "premium_subscription",
    27: "family_plan",
    28: "premium_subscription",
    29: "premium_subscription",
    30: "download_offline",
    31: "billing_payment",
    32: "student_plan",
    33: "premium_subscription",
    34: "premium_subscription",
    35: "premium_subscription",
    36: "billing_payment",
    37: "student_plan",
    38: "content_library",
    39: "premium_subscription",
    40: "premium_subscription",

    # Batch 3: 41-60
    41: "billing_payment",
    42: "billing_payment",
    43: "billing_payment",
    44: "billing_payment",
    45: "premium_subscription",
    46: "billing_payment",
    47: "premium_subscription",
    48: "billing_payment",
    49: "billing_payment",
    50: "billing_payment",
    51: "student_plan",
    52: "billing_payment",
    53: "billing_payment",
    54: "billing_payment",
    55: "billing_payment",
    56: "billing_payment",
    57: "billing_payment",
    58: "account_access",
    59: "premium_subscription",
    60: "billing_payment",

    # Batch 4: 61-80
    61: "family_plan",
    62: "family_plan",
    63: "family_plan",
    64: "family_plan",
    65: "family_plan",
    66: "family_plan",
    67: "family_plan",
    68: "family_plan",
    69: "family_plan",
    70: "family_plan",
    71: "account_access",
    72: "feature_feedback",
    73: "family_plan",
    74: "family_plan",
    75: "family_plan",
    76: "family_plan",
    77: "family_plan",
    78: "family_plan",
    79: "family_plan",
    80: "family_plan",

    # Batch 5: 81-100
    81: "student_plan",
    82: "student_plan",
    83: "student_plan",
    84: "student_plan",
    85: "student_plan",
    86: "other_unclear",
    87: "student_plan",
    88: "student_plan",
    89: "student_plan",
    90: "student_plan",
    91: "student_plan",
    92: "app_technical_issue",
    93: "student_plan",
    94: "student_plan",
    95: "student_plan",
    96: "other_unclear",
    97: "app_technical_issue",
    98: "billing_payment",
    99: "billing_payment",
    100: "student_plan",

    # Batch 6: 101-120
    101: "app_technical_issue",
    102: "download_offline",
    103: "app_technical_issue",
    104: "app_technical_issue",
    105: "app_technical_issue",
    106: "student_plan",
    107: "billing_payment",
    108: "app_technical_issue",
    109: "app_technical_issue",
    110: "account_access",
    111: "student_plan",
    112: "family_plan",
    113: "playback_issue",
    114: "app_technical_issue",
    115: "content_library",
    116: "app_technical_issue",
    117: "family_plan",
    118: "account_access",
    119: "playback_issue",
    120: "account_access",

    # Batch 7: 121-140
    121: "content_library",
    122: "feature_feedback",
    123: "playback_issue",
    124: "playback_issue",
    125: "app_technical_issue",
    126: "feature_feedback",
    127: "playback_issue",
    128: "playback_issue",
    129: "playback_issue",
    130: "playback_issue",
    131: "playback_issue",
    132: "account_access",
    133: "playback_issue",
    134: "playback_issue",
    135: "feature_feedback",
    136: "playback_issue",
    137: "playback_issue",
    138: "feature_feedback",
    139: "playback_issue",
    140: "playback_issue",

    # Batch 8: 141-160
    141: "feature_feedback",
    142: "download_offline",
    143: "feature_feedback",
    144: "other_unclear",
    145: "feature_feedback",
    146: "playback_issue",
    147: "content_library",
    148: "content_library",
    149: "other_unclear",
    150: "content_library",
    151: "playback_issue",
    152: "feature_feedback",
    153: "content_library",
    154: "content_library",
    155: "download_offline",
    156: "playback_issue",
    157: "feature_feedback",
    158: "content_library",
    159: "content_library",
    160: "app_technical_issue",

    # Batch 9: 161-180
    161: "app_technical_issue",
    162: "download_offline",
    163: "download_offline",
    164: "download_offline",
    165: "download_offline",
    166: "playback_issue",
    167: "download_offline",
    168: "download_offline",
    169: "download_offline",
    170: "download_offline",
    171: "playback_issue",
    172: "app_technical_issue",
    173: "download_offline",
    174: "download_offline",
    175: "download_offline",
    176: "download_offline",
    177: "content_library",
    178: "download_offline",
    179: "download_offline",
    180: "download_offline",

    # Batch 10: 181-200
    181: "content_library",
    182: "feature_feedback",
    183: "other_unclear",
    184: "feature_feedback",
    185: "feature_feedback",
    186: "feature_feedback",
    187: "feature_feedback",
    188: "feature_feedback",
    189: "feature_feedback",
    190: "feature_feedback",
    191: "feature_feedback",
    192: "content_library",
    193: "feature_feedback",
    194: "feature_feedback",
    195: "feature_feedback",
    196: "feature_feedback",
    197: "feature_feedback",
    198: "content_library",
    199: "feature_feedback",
    200: "feature_feedback",
}


def main():
    df = pd.read_csv(INPUT_FILE)

    if len(df) != 200:
        raise ValueError(f"Expected 200 examples, found {len(df)}")

    if set(df["example_id"]) != set(FINAL_LABELS):
        raise ValueError("Example IDs do not match the final label mapping.")

    df["golden_intent"] = df["example_id"].map(FINAL_LABELS)

    df.to_csv(OUTPUT_FILE, index=False)

    print("Golden set finalized.")
    print(f"Total examples: {len(df)}")
    print(f"Saved to: {OUTPUT_FILE}")
    print("\nFinal intent distribution:")
    print(df["golden_intent"].value_counts().sort_index())


if __name__ == "__main__":
    main()