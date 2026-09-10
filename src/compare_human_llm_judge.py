import pandas as pd

HUMAN_FILE = "evaluation/human_judge_validation.csv"
LLM_FILE = "evaluation/llm_judge_sample.csv"


def main():
    human_df = pd.read_csv(HUMAN_FILE)
    llm_df = pd.read_csv(LLM_FILE)

    merged = human_df.merge(
        llm_df,
        on="example_id",
        how="inner"
    )

    dimensions = [
        ("relevance", "relevance_human", "relevance_score"),
        ("groundedness", "groundedness_human", "groundedness_score"),
        ("helpfulness", "helpfulness_human", "helpfulness_score"),
        ("privacy", "privacy_human", "privacy_score"),
        (
            "unsupported_action",
            "unsupported_action_human",
            "unsupported_action_score"
        ),
    ]

    print("Human vs LLM Judge Agreement")
    print("-" * 40)

    total_matches = 0
    total_scores = 0

    for name, human_col, llm_col in dimensions:
        matches = (
            merged[human_col] == merged[llm_col]
        ).sum()

        total = len(merged)
        agreement = matches / total

        total_matches += matches
        total_scores += total

        print(
            f"{name}: "
            f"{matches}/{total} "
            f"({agreement:.1%})"
        )

    overall_agreement = total_matches / total_scores

    print("-" * 40)
    print(
        f"Overall exact agreement: "
        f"{total_matches}/{total_scores} "
        f"({overall_agreement:.1%})"
    )


if __name__ == "__main__":
    main()