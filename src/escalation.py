ACCOUNT_SPECIFIC_INTENTS = {
    "account_access",
    "billing_payment",
    "premium_subscription",
    "family_plan",
    "student_plan",
}


def decide_escalation(
    intent,
    confidence,
    historical_cases
):
    top_similarity = historical_cases["similarity"].max()

    reasons = []

    if confidence < 0.30:
        reasons.append(
            "Low classifier confidence"
        )

    if top_similarity < 0.35:
        reasons.append(
            "Weak historical evidence"
        )

    if intent in ACCOUNT_SPECIFIC_INTENTS:
        reasons.append(
            "Issue may require account-specific investigation"
        )

    if reasons:
        return "escalate", "; ".join(reasons)

    return "auto_handle", "Strong classification and historical evidence"