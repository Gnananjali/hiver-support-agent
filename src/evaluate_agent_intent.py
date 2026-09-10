import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    f1_score,
    classification_report,
    confusion_matrix
)

from classifier import load_classifier, predict_intent


GOLDEN_FILE = "evaluation/golden_set.csv"
PREDICTIONS_FILE = "evaluation/agent_intent_predictions.csv"


def main():
    golden_df = pd.read_csv(GOLDEN_FILE)

    vectorizer, model = load_classifier()

    predictions = []

    for message in golden_df["customer_message"]:
        prediction, confidence = predict_intent(
            message,
            vectorizer,
            model
        )

        predictions.append(prediction)

    golden_df["predicted_intent"] = predictions

    y_true = golden_df["golden_intent"]
    y_pred = golden_df["predicted_intent"]

    accuracy = accuracy_score(
        y_true,
        y_pred
    )

    macro_f1 = f1_score(
        y_true,
        y_pred,
        average="macro",
        zero_division=0
    )

    print("=" * 70)
    print("AGENT INTENT EVALUATION")
    print("=" * 70)

    print(f"\nEvaluation examples: {len(golden_df)}")
    print(f"Number of intents: {y_true.nunique()}")

    print(f"\nAccuracy: {accuracy:.4f}")
    print(f"Macro F1: {macro_f1:.4f}")

    print("\nPer-intent results:")
    print(
        classification_report(
            y_true,
            y_pred,
            zero_division=0
        )
    )

    # Confusion matrix
    labels = sorted(y_true.unique())

    matrix = confusion_matrix(
        y_true,
        y_pred,
        labels=labels
    )

    confusion_df = pd.DataFrame(
        matrix,
        index=labels,
        columns=labels
    )

    print("\nConfusion Matrix:")
    print(confusion_df)

    # Save predictions for later failure analysis
    golden_df.to_csv(
        PREDICTIONS_FILE,
        index=False
    )

    print(
        f"\nPredictions saved to: {PREDICTIONS_FILE}"
    )


if __name__ == "__main__":
    main()