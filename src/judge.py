import json
import os

from dotenv import load_dotenv
from google import genai


def build_judge_prompt(
    customer_message,
    predicted_intent,
    historical_evidence,
    draft_reply
):
    evidence_text = ""

    for i, (_, row) in enumerate(
        historical_evidence.iterrows(),
        start=1
    ):
        evidence_text += (
            f"\nHistorical case {i}\n"
            f"Customer problem: "
            f"{row['customer_message']}\n"
            f"Historical resolution: "
            f"{row['support_response']}\n"
        )

    prompt = f"""
You are evaluating a customer support reply.

The support agent is designed for Spotify customer support.

Customer message:
{customer_message}

Predicted intent:
{predicted_intent}

Historical evidence:
{evidence_text}

Generated reply:
{draft_reply}

Evaluate the generated reply using these five dimensions.

1. Relevance
0 = Does not address the customer's problem
1 = Partially addresses the problem
2 = Directly addresses the problem

2. Groundedness
0 = Contains unsupported or invented claims
1 = Mostly supported but includes questionable claims
2 = Fully consistent with the available historical evidence

3. Helpfulness
0 = Not useful
1 = Somewhat useful
2 = Clear and useful next step

4. Privacy
0 = Exposes sensitive/internal information
1 = Minor concern
2 = No privacy or internal-information issue

5. Unsupported actions or policies
0 = Clearly claims an unsupported action or policy
1 = Ambiguous or potentially unsupported
2 = No unsupported claim

Important:

Judge the generated reply itself.

Do not give a lower relevance score simply because
the predicted intent is incorrect.

Do not assume that a historical response is automatically
correct for the current customer.

Do not reward the reply merely because it sounds polite.

Return ONLY valid JSON.

The JSON must contain exactly these fields:

{{
    "relevance_score": 0,
    "groundedness_score": 0,
    "helpfulness_score": 0,
    "privacy_score": 0,
    "unsupported_action_score": 0,
    "reasoning": "brief explanation"
}}
"""

    return prompt


def judge_reply(prompt):
    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY was not found. "
            "Check your .env file."
        )

    client = genai.Client(
        api_key=api_key
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    text = response.text.strip()

    # Remove markdown code fences if the model adds them.
    if text.startswith("```"):
        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

    return json.loads(text)