import pandas as pd

from agent import run_agent
from judge import build_judge_prompt, judge_reply


INPUT_FILE = "evaluation/reply_evaluation_sample.csv"
OUTPUT_FILE = "evaluation/llm_judge_sample.csv"


def main():
    df = pd.read_csv(INPUT_FILE)

    results = []

    print("=" * 70)
    print("LLM-AS-JUDGE EVALUATION")
    print("=" * 70)

    for index, row in df.iterrows():

        print(
            f"\nJudging example "
            f"{index + 1}/{len(df)}..."
        )

        customer_message = row["customer_message"]

        # Retrieve the same type of historical evidence
        # used by the support agent.
        _, _, historical_cases, _, _ = run_agent(
            customer_message
        )

        prompt = build_judge_prompt(
            customer_message,
            row["predicted_intent"],
            historical_cases,
            row["draft_reply"]
        )

        judgment = judge_reply(prompt)

        results.append({
            "example_id": row["example_id"],
            "customer_message": customer_message,
            "golden_intent": row["golden_intent"],
            "predicted_intent": row["predicted_intent"],
            "classifier_confidence": row["classifier_confidence"],
            "decision": row["decision"],
            "draft_reply": row["draft_reply"],
            "relevance_score": judgment["relevance_score"],
            "groundedness_score": judgment["groundedness_score"],
            "helpfulness_score": judgment["helpfulness_score"],
            "privacy_score": judgment["privacy_score"],
            "unsupported_action_score": judgment[
                "unsupported_action_score"
            ],
            "reasoning": judgment["reasoning"]
        })

    results_df = pd.DataFrame(results)

    score_columns = [
        "relevance_score",
        "groundedness_score",
        "helpfulness_score",
        "privacy_score",
        "unsupported_action_score"
    ]

    results_df["total_score"] = results_df[
        score_columns
    ].sum(axis=1)

    results_df["max_score"] = 10

    results_df["quality_percentage"] = (
        results_df["total_score"] / 10 * 100
    )

    results_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    print(
        f"\nAverage total score: "
        f"{results_df['total_score'].mean():.2f}/10"
    )

    print(
        f"Average quality: "
        f"{results_df['quality_percentage'].mean():.1f}%"
    )

    for column in score_columns:
        print(
            f"{column}: "
            f"{results_df[column].mean():.2f}/2"
        )

    print(
        f"\nSaved to: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()