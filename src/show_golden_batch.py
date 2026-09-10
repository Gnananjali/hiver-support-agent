import pandas as pd

INPUT_PATH = "evaluation/golden_candidates.csv"

df = pd.read_csv(INPUT_PATH)

# Change this number to see another batch later.
batch_number = 10

batch_size = 20

start = (batch_number - 1) * batch_size
end = start + batch_size

batch = df.iloc[start:end]

print("\n" + "=" * 80)
print(f"GOLDEN SET BATCH {batch_number}")
print("=" * 80)

for _, row in batch.iterrows():

    print(f"\nExample ID: {row['example_id']}")
    print(f"Candidate intent: {row['candidate_intent']}")
    print(f"Customer: {row['customer_message']}")
    print(f"Historical support response: {row['support_response']}")
    print("-" * 80)