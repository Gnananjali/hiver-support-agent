import pandas as pd


INPUT_FILE = "evaluation/reply_evaluation_sample.csv"
OUTPUT_FILE = "evaluation/reply_scores_sample.csv"


def score_reply(row):
    """
    Temporary manual scoring function.

    We will later replace this with an LLM judge.
    """

    return {
        "relevance_score": None,
        "groundedness_score": None,
        "helpfulness_score": None,
        "privacy_score": None,
        "unsupported_action_score": None,
    }


def main():
    df = pd.read_csv(INPUT_FILE)

    scores = []

    for _, row in df.iterrows():
        result = score_reply(row)

        scores.append({
            "example_id": row["example_id"],
            "customer_message": row["customer_message"],
            "draft_reply": row["draft_reply"],
            **result
        })

    scores_df = pd.DataFrame(scores)

    scores_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("=" * 70)
    print("REPLY EVALUATION STRUCTURE")
    print("=" * 70)

    print(f"\nExamples: {len(scores_df)}")

    print("\nEvaluation dimensions:")
    print("- Relevance")
    print("- Groundedness")
    print("- Helpfulness")
    print("- Privacy")
    print("- Unsupported actions/policies")

    print(f"\nSaved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()