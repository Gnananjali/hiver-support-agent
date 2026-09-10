import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score


TRAIN_FILE = "evaluation/training_clean.csv"
TEST_FILE = "evaluation/golden_set.csv"


def main():
    # Load the labeled training data
    train_df = pd.read_csv(TRAIN_FILE)

    # Load the golden evaluation set
    test_df = pd.read_csv(TEST_FILE)

    # Get customer messages and their labels
    X_train = train_df["customer_message"]
    y_train = train_df["training_intent"]

    # Get the messages and ground-truth labels for evaluation
    X_test = test_df["customer_message"]
    y_test = test_df["golden_intent"]

    # Convert text into TF-IDF numerical features
    vectorizer = TfidfVectorizer(
        lowercase=True,
        ngram_range=(1, 2),
        min_df=2
    )

    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    # Train a simple Logistic Regression classifier
    model = LogisticRegression(
        max_iter=1000,
        random_state=42
    )

    model.fit(X_train_tfidf, y_train)

    # Predict intents for the golden set
    predictions = model.predict(X_test_tfidf)

    # Calculate evaluation metrics
    accuracy = accuracy_score(y_test, predictions)

    macro_f1 = f1_score(
        y_test,
        predictions,
        average="macro",
        zero_division=0
    )

    print("=" * 60)
    print("BASELINE #2 — TF-IDF + LOGISTIC REGRESSION")
    print("=" * 60)

    print(f"Training examples: {len(train_df)}")
    print(f"Evaluation examples: {len(test_df)}")
    print(f"Number of intents: {y_train.nunique()}")
    print(f"Vocabulary size: {len(vectorizer.vocabulary_)}")

    print()
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Macro F1: {macro_f1:.4f}")


if __name__ == "__main__":
    main()