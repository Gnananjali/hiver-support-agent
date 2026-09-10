from classifier import load_classifier


def main():
    vectorizer, model = load_classifier()

    test_messages = [
        "I can't log into my Spotify account",
        "Why was I charged twice?",
        "I can't add someone to my family plan",
        "My downloaded songs won't play offline",
        "I can't get my student discount to work",
    ]

    for message in test_messages:

        message_vector = vectorizer.transform(
            [message]
        )

        probabilities = model.predict_proba(
            message_vector
        )[0]

        ranked_indices = probabilities.argsort()[::-1]

        print()
        print("=" * 70)
        print(f"Message: {message}")
        print("=" * 70)

        print("Top 3 predictions:")

        for index in ranked_indices[:3]:
            intent = model.classes_[index]
            probability = probabilities[index]

            print(
                f"{intent}: {probability:.4f}"
            )


if __name__ == "__main__":
    main()