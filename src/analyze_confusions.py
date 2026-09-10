import pandas as pd


PREDICTIONS_FILE = "evaluation/agent_intent_predictions.csv"


def main():
    df = pd.read_csv(PREDICTIONS_FILE)

    mistakes = df[
        df["golden_intent"] != df["predicted_intent"]
    ].copy()

    confusion_counts = (
        mistakes
        .groupby(["golden_intent", "predicted_intent"])
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
    )

    print("=" * 70)
    print("TOP CLASSIFICATION CONFUSIONS")
    print("=" * 70)

    print(f"\nTotal mistakes: {len(mistakes)}")

    print("\nMost common confusion pairs:\n")

    for _, row in confusion_counts.head(15).iterrows():
        print(
            f"{row['golden_intent']}"
            f" -> "
            f"{row['predicted_intent']}"
            f": {row['count']}"
        )

    print("\n" + "=" * 70)
    print("EXAMPLES FROM TOP CONFUSIONS")
    print("=" * 70)

    for _, row in confusion_counts.head(5).iterrows():

        actual = row["golden_intent"]
        predicted = row["predicted_intent"]

        examples = mistakes[
            (mistakes["golden_intent"] == actual)
            & (mistakes["predicted_intent"] == predicted)
        ]

        print(
            f"\n{actual} -> {predicted}"
            f" ({len(examples)} examples)"
        )

        for _, example in examples.head(3).iterrows():
            print(
                f"- {example['customer_message']}"
            )


if __name__ == "__main__":
    main()