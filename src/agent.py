from classifier import load_classifier, predict_intent
from retrieval import (
    load_data,
    build_retriever,
    retrieve_similar_cases
)
from escalation import decide_escalation


def run_agent(customer_message):
    # 1. Classify the customer message
    classifier_vectorizer, classifier_model = load_classifier()

    predicted_intent, confidence = predict_intent(
        customer_message,
        classifier_vectorizer,
        classifier_model
    )

    # 2. Retrieve similar historical cases
    df = load_data()

    retrieval_vectorizer, customer_vectors = build_retriever(df)

    results = retrieve_similar_cases(
        customer_message,
        df,
        retrieval_vectorizer,
        customer_vectors,
        top_k=3
    )

    # 3. Decide whether to auto-handle or escalate
    decision, reason = decide_escalation(
        predicted_intent,
        confidence,
        results
    )

    return (
        predicted_intent,
        confidence,
        results,
        decision,
        reason
    )


def main():
    customer_message = input(
        "Customer message: "
    )

    (
        intent,
        confidence,
        results,
        decision,
        reason
    ) = run_agent(customer_message)

    print("\n" + "=" * 70)
    print("SUPPORT AGENT")
    print("=" * 70)

    print(f"\nPredicted intent: {intent}")
    print(f"Classifier confidence: {confidence:.4f}")

    print(f"\nDecision: {decision}")
    print(f"Reason: {reason}")

    print("\nHistorical evidence:")

    for i, (_, row) in enumerate(
        results.iterrows(),
        start=1
    ):
        print(f"\nEvidence {i}")
        print(f"Similarity: {row['similarity']:.4f}")
        print(f"Customer: {row['customer_message']}")
        print(f"Historical response: {row['support_response']}")


if __name__ == "__main__":
    main()