import pandas as pd

from agent import run_agent
from reply import build_reply_prompt, generate_reply


GOLDEN_FILE = "evaluation/golden_set.csv"
OUTPUT_FILE = "evaluation/reply_evaluation_sample.csv"


def main():
    golden_df = pd.read_csv(GOLDEN_FILE)

    # Start with only 5 examples.
    sample_df = golden_df.head(5).copy()

    results = []

    print("=" * 70)
    print("REPLY GENERATION EVALUATION — SMALL SAMPLE")
    print("=" * 70)

    for index, row in sample_df.iterrows():

        customer_message = row["customer_message"]

        print(
            f"\nProcessing example "
            f"{index + 1}/{len(sample_df)}..."
        )

        intent, confidence, historical_cases, decision, reason = (
            run_agent(customer_message)
        )

        prompt = build_reply_prompt(
            customer_message,
            intent,
            confidence,
            historical_cases
        )

        reply = generate_reply(prompt)

        results.append({
            "example_id": row["example_id"],
            "customer_message": customer_message,
            "golden_intent": row["golden_intent"],
            "predicted_intent": intent,
            "classifier_confidence": confidence,
            "decision": decision,
            "escalation_reason": reason,
            "draft_reply": reply
        })

    results_df = pd.DataFrame(results)

    results_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("\n" + "=" * 70)
    print("RESULTS")
    print("=" * 70)

    for _, row in results_df.iterrows():

        print("\n" + "-" * 70)
        print(f"Example: {row['example_id']}")
        print(f"Customer: {row['customer_message']}")
        print(f"Intent: {row['predicted_intent']}")
        print(f"Decision: {row['decision']}")
        print(f"\nDraft reply:\n{row['draft_reply']}")

    print("\n" + "=" * 70)
    print(f"Saved to: {OUTPUT_FILE}")
    print("=" * 70)


if __name__ == "__main__":
    main()