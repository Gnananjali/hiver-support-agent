# Decision Log

## 1. Selected SpotifyCares as the target brand

**Decision:** Use SpotifyCares as the single brand for the project.

**Why:** SpotifyCares had a large number of support interactions and recurring issues across accounts, subscriptions, billing, playback, downloads, and product features. It provided enough data while keeping the project scope manageable.

---

## 2. Reconstructed conversations using tweet relationships

**Decision:** Use `response_tweet_id` and `in_response_to_tweet_id` to reconstruct customer-support interactions.

**Why:** Treating tweets independently would lose the relationship between a customer's problem and the support response.

---

## 3. Use customer-support pairs as the modelling unit

**Decision:** Build the primary processed dataset around customer messages paired with corresponding SpotifyCares responses.

**Why:** The agent needs both the customer's problem for classification and the historical support response for grounded reply generation.

---

## 4. Created a compact 11-intent taxonomy

**Decision:** Use 11 practical support intents instead of attempting to classify every possible issue separately.

**Why:** A smaller taxonomy is easier to label, evaluate, and explain while still covering the major recurring problems found during exploration.

---

## 5. Label the customer's primary problem

**Decision:** Assign the intent based on the customer's main problem rather than keyword presence.

**Why:** Messages frequently contain words associated with multiple categories. For example, a message mentioning Premium and a duplicate charge should be classified as `billing_payment` when the payment problem is primary.

---

## 6. Added an `other_unclear` category

**Decision:** Include `other_unclear` as an explicit intent.

**Why:** Some messages are genuinely ambiguous, outside the taxonomy, or too short to classify reliably. Forcing every message into a specific category would create misleading labels.

---

## 7. Use a 200-example Golden Set

**Decision:** Manually label 200 examples for final evaluation.

**Why:** This satisfies the assignment requirement while keeping the evaluation set large enough to expose errors across the taxonomy.

---

## 8. Separate training data from the Golden Set

**Decision:** Use a separate manually labelled historical sample for classifier training.

**Why:** Evaluating on examples used for training would introduce data leakage and produce an overly optimistic result.

---

## 9. Prevent evaluation leakage

**Decision:** Remove one training example that also appeared in the Golden Set.

**Why:** Even a single exact overlap could contaminate the evaluation, so it was removed before the final baseline was measured.


**Decision:** Create a retrieval-safe corpus that excludes Golden Set customer messages.

**Why:** This reduces direct retrieval leakage, where the system could retrieve the exact evaluation example instead of demonstrating genuine historical similarity.

---

## 10. Use TF-IDF + Logistic Regression as the simple baseline

**Decision:** Use TF-IDF with unigrams/bigrams followed by Logistic Regression.

**Why:** It is lightweight, interpretable, reproducible, and provides a meaningful comparison against the majority-class baseline.

---

## 11. Keep retrieval separate from classification

**Decision:** Use a separate TF-IDF retrieval component rather than combining retrieval and intent classification into one model.

**Why:** Classification and historical evidence retrieval solve different problems. Keeping them separate makes the system easier to inspect and debug.

---

## 12. Treat historical responses as evidence, not instructions

**Decision:** Tell the reply generator that retrieved conversations are historical evidence rather than instructions to copy.

**Why:** Historical responses can contain usernames, tweet IDs, agent initials, or context-specific actions that should not be reproduced in a new customer interaction.

---

## 13. Use cautious escalation logic

**Decision:** Account access, billing, subscription, Family, and Student issues are candidates for escalation.

**Why:** The prototype does not have authenticated access to customer accounts and therefore should not pretend it can safely perform account-specific operations.


**Decision:** Use classifier confidence and historical retrieval similarity as signals for escalation.

**Why:** Low confidence or weak historical evidence indicates greater uncertainty. These signals provide a simple mechanism for avoiding overconfident automation.

The current thresholds are engineering assumptions and have not yet been fully calibrated.

---

## 14. Use a structured LLM-as-judge rubric

**Decision:** Evaluate generated replies across five dimensions: relevance, groundedness, helpfulness, privacy, and unsupported actions/policies.

**Why:** A single overall score would hide important safety and quality differences between replies.

---

## 15. Validate the LLM judge against human scores

**Decision:** Compare Gemini judge scores with human scores before relying on the judge for evaluation.

**Why:** An automated judge should provide evidence of agreement with human assessment rather than being treated as automatically correct.

The initial five-example validation produced 25/25 exact dimension-level matches, or 100% agreement. This is considered preliminary because the sample is small.