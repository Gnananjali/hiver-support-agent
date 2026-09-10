import pandas as pd

from escalation import decide_escalation


def main():
    cases = pd.DataFrame({
        "similarity": [
            0.8816,
            0.5728,
            0.5267
        ]
    })

    decision, reason = decide_escalation(
        intent="account_access",
        confidence=0.4481,
        historical_cases=cases
    )

    print("Decision:", decision)
    print("Reason:", reason)


if __name__ == "__main__":
    main()