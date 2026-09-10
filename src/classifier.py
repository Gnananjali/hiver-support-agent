import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


TRAIN_FILE = "evaluation/training_clean.csv"


def load_classifier():
    df = pd.read_csv(TRAIN_FILE)

    X_train = df["customer_message"]
    y_train = df["training_intent"]

    vectorizer = TfidfVectorizer(
        lowercase=True,
        ngram_range=(1, 2),
        min_df=2
    )

    X_train_tfidf = vectorizer.fit_transform(X_train)

    model = LogisticRegression(
        max_iter=1000,
        random_state=42
    )

    model.fit(X_train_tfidf, y_train)

    return vectorizer, model


def predict_intent(
    customer_message,
    vectorizer,
    model
):
    message_vector = vectorizer.transform(
        [customer_message]
    )

    prediction = model.predict(message_vector)[0]

    probabilities = model.predict_proba(
        message_vector
    )[0]

    confidence = probabilities.max()

    return prediction, confidence