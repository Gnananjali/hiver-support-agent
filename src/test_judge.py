import pandas as pd

from agent import run_agent
from judge import build_judge_prompt, judge_reply


INPUT_FILE = "evaluation/reply_evaluation_sample.csv"


def main():
    df = pd.read_csv(INPUT_FILE)

    # Test only ONE example.
    row = df.iloc[0]

    customer_message = row["customer_message"]
    predicted_intent = row["predicted_intent"]
    draft_reply = row["draft_reply"]

    # Retrieve the historical evidence again.
    _, _, historical_cases, _, _ = run_agent(
        customer_message
    )

    prompt = build_judge_prompt(
        customer_message,
        predicted_intent,
        historical_cases,
        draft_reply
    )

    result = judge_reply(prompt)

    print("=" * 70)
    print("LLM JUDGE TEST")
    print("=" * 70)

    print("\nCustomer:")
    print(customer_message)

    print("\nGenerated reply:")
    print(draft_reply)

    print("\nJudge result:")

    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()