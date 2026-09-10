import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


DATA_FILE = "data/processed/spotify_retrieval_safe.csv"


def load_data():
    df = pd.read_csv(DATA_FILE)

    df = df.dropna(subset=["customer_message", "support_response"])

    return df


def build_retriever(df):
    vectorizer = TfidfVectorizer(
        lowercase=True,
        ngram_range=(1, 2),
        min_df=2
    )

    customer_vectors = vectorizer.fit_transform(
        df["customer_message"]
    )

    return vectorizer, customer_vectors


def retrieve_similar_cases(
    query,
    df,
    vectorizer,
    customer_vectors,
    top_k=5
):
    query_vector = vectorizer.transform([query])

    similarities = cosine_similarity(
        query_vector,
        customer_vectors
    )[0]

    top_indices = similarities.argsort()[::-1][:top_k]

    results = df.iloc[top_indices].copy()
    results["similarity"] = similarities[top_indices]

    return results


def main():
    df = load_data()

    print(f"Historical interactions: {len(df)}")

    vectorizer, customer_vectors = build_retriever(df)

    query = input("\nEnter a customer message: ")

    results = retrieve_similar_cases(
        query,
        df,
        vectorizer,
        customer_vectors,
        top_k=5
    )

    print("\n" + "=" * 70)
    print("TOP HISTORICAL MATCHES")
    print("=" * 70)

    for i, (_, row) in enumerate(results.iterrows(), start=1):
        print(f"\nMATCH {i}")
        print(f"Similarity: {row['similarity']:.4f}")
        print(f"Customer: {row['customer_message']}")
        print(f"SpotifyCares: {row['support_response']}")


if __name__ == "__main__":
    main()