import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    classification_report,
    confusion_matrix,
)


TRAIN_FILE = "evaluation/training_clean.csv"
TEST_FILE = "evaluation/golden_set.csv"


def main():
    train_df = pd.read_csv(TRAIN_FILE)
    test_df = pd.read_csv(TEST_FILE)

    X_train = train_df["customer_message"]
    y_train = train_df["training_intent"]

    X_test = test_df["customer_message"]
    y_test = test_df["golden_intent"]

    vectorizer = TfidfVectorizer(
        lowercase=True,
        ngram_range=(1, 2),
        min_df=2
    )

    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    model = LogisticRegression(
        max_iter=1000,
        random_state=42
    )

    model.fit(X_train_tfidf, y_train)

    predictions = model.predict(X_test_tfidf)

    accuracy = accuracy_score(y_test, predictions)

    macro_f1 = f1_score(
        y_test,
        predictions,
        average="macro",
        zero_division=0
    )

    print("=" * 70)
    print("BASELINE #2 — DETAILED EVALUATION")
    print("=" * 70)

    print(f"Accuracy: {accuracy:.4f}")
    print(f"Macro F1: {macro_f1:.4f}")

    print()
    print("=" * 70)
    print("PER-INTENT PERFORMANCE")
    print("=" * 70)

    print(
        classification_report(
            y_test,
            predictions,
            zero_division=0
        )
    )

    print()
    print("=" * 70)
    print("CONFUSION MATRIX")
    print("=" * 70)

    labels = sorted(y_test.unique())

    matrix = confusion_matrix(
        y_test,
        predictions,
        labels=labels
    )

    confusion_df = pd.DataFrame(
        matrix,
        index=labels,
        columns=labels
    )

    print(confusion_df.to_string())


if __name__ == "__main__":
    main()
