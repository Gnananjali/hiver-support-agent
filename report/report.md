# SpotifyCares AI Support Agent

## 1. Problem Framing

The goal of this project is to build a practical AI customer-support agent for SpotifyCares using historical customer-support conversations from Twitter.

The agent receives a new customer message and performs three tasks:

1. Classifies the customer's primary problem into a small, data-derived set of support intents.
2. Retrieves historically similar SpotifyCares conversations to provide evidence about how similar issues were handled.
3. Drafts a customer-facing response and decides whether the case should be auto-handled or escalated to a human.

The project is intentionally scoped around support triage and response drafting rather than attempting to build a fully autonomous customer-service system.

The central evaluation question is:

> Can a lightweight support agent identify the customer's primary issue and produce a useful, historically grounded response while recognizing cases that may require human investigation?

The system is evaluated using a 200-example hand-labelled Golden Set. Evaluation covers both intent classification and generated reply quality.

---

## 2. What Good Looks Like

A good support agent should not be judged only by whether its intent prediction is correct. It should also produce a response that is relevant, grounded in historical evidence, useful to the customer, safe, and free from unsupported claims.

### Intent classification

The classifier should:

- Identify the customer's primary problem rather than simply matching keywords.
- Perform substantially better than the trivial majority-class baseline.
- Maintain useful performance across different intents rather than succeeding only on the most common class.
- Recognize uncertainty when the message is ambiguous.

The main automated metrics are accuracy and macro F1 on the 200-example Golden Set. Macro F1 is important because the Golden Set contains multiple intents with different numbers of examples.

### Reply generation

A good generated reply should:

1. Be relevant to the customer's actual problem.
2. Be grounded in historical SpotifyCares evidence.
3. Provide a clear and appropriate next step.
4. Avoid exposing usernames, tweet IDs, internal identifiers, or other conversation-specific information.
5. Avoid unsupported refunds, policies, features, procedures, or claims that an action has already been completed.

Reply quality is evaluated using a five-dimension rubric. Each dimension is scored from 0 to 2, giving a maximum score of 10.

### Escalation

A good escalation policy should avoid treating every case as safe for automation. Cases with account-specific requirements, weak historical evidence, or low classifier confidence should be considered for human handling.

The current escalation thresholds are engineering assumptions rather than validated policy. Further evaluation would be needed before using them in production.

---

## 3. What We Deliberately Did Not Build

This project deliberately avoids several areas that would increase complexity without providing enough evidence of value within the assignment scope.

### Fully autonomous account resolution

The system does not directly change passwords, subscriptions, payment methods, refunds, or account settings.

Historical Twitter conversations can show how support agents responded, but they do not provide the access or authorization required to safely perform account-specific actions.

### Production-scale LLM support automation

The project does not attempt to build a production-ready autonomous support system with authentication, tool execution, monitoring, rate limiting, or deployment infrastructure.

The objective is to demonstrate the core support-agent workflow and evaluate its behavior.

### Training a large language model

The intent classifier uses TF-IDF and Logistic Regression rather than fine-tuning a large model. This provides a simple and interpretable baseline and keeps experimentation lightweight.

### Full-dataset processing

The assignment explicitly allows subsampling. Instead of repeatedly processing all approximately 3 million tweets, the project reconstructs the selected brand's conversations and uses smaller labelled subsets for development and evaluation.

This makes iteration faster and reduces unnecessary computation.

### Perfect intent classification

The taxonomy is a practical simplification of messy real-world support conversations. Some messages contain multiple problems or insufficient context, so a single-label classifier cannot represent every nuance.

The goal is therefore useful triage rather than perfect categorization.

---

## 4. Dataset and Conversation Reconstruction

The project uses the Kaggle Customer Support on Twitter dataset.

The selected brand is SpotifyCares because it provides a substantial number of support interactions and contains recurring product, account, subscription, payment, and playback problems suitable for a focused support-agent experiment.

SpotifyCares contains approximately 43,000 support interactions in the reconstructed dataset.

Conversation relationships were reconstructed using the dataset's tweet-response identifiers rather than treating individual tweets as independent examples.

The resulting cleaned customer-support dataset contains:

- 43,076 customer-support pairs after cleaning.
- Customer message text.
- Corresponding historical SpotifyCares response.

A separate retrieval-safe corpus was created for evaluation. It removes Golden Set customer messages from the retrieval corpus to reduce direct leakage during evaluation.

The Golden Set contains 200 manually labelled customer messages.

A separate training sample of 550 historical examples was manually labelled for the intent classifier. After removing one message overlapping with the Golden Set, 549 examples remained for fair baseline training.

---

## 5. Intent Taxonomy

The final taxonomy contains 11 intents derived from recurring problems observed in the SpotifyCares data:

1. `account_access` — login, password, hacked account, or account-access problems.
2. `premium_subscription` — Premium activation, status, cancellation, or subscription changes.
3. `billing_payment` — charges, duplicate charges, refunds, payment failures, and payment methods.
4. `family_plan` — Family plan setup, members, invitations, and verification.
5. `student_plan` — student discounts, verification, and eligibility.
6. `app_technical_issue` — app bugs, crashes, search problems, and general app malfunction.
7. `playback_issue` — songs stopping, not playing, shuffle, and repeat problems.
8. `content_library` — missing songs or albums, playlists, library, and content-related problems.
9. `download_offline` — downloaded or offline music problems.
10. `feature_feedback` — feature requests and product suggestions.
11. `other_unclear` — cases genuinely outside the categories or lacking sufficient information.

The primary-label principle is based on the customer's main problem rather than individual keyword presence.

For example, a message containing both "Premium" and "charged twice" is labelled `billing_payment` because the payment problem is the primary issue.

---

## 6. Evaluation Setup

### Golden Set

A 200-example Golden Set was manually labelled.

The examples were sampled from the selected SpotifyCares data and then reviewed individually using the final taxonomy.

The final distribution was:

| Intent | Examples |
|---|---:|
| account_access | 21 |
| app_technical_issue | 15 |
| billing_payment | 21 |
| content_library | 14 |
| download_offline | 19 |
| family_plan | 21 |
| feature_feedback | 26 |
| other_unclear | 7 |
| playback_issue | 20 |
| premium_subscription | 16 |
| student_plan | 20 |
| **Total** | **200** |

### Baselines

Two baselines were evaluated:

**Baseline 1 — Majority class**

Always predicts the most common Golden Set intent.

**Baseline 2 — TF-IDF + Logistic Regression**

Uses word and bigram TF-IDF features followed by Logistic Regression. It was trained on 549 labelled historical examples and evaluated on the 200-example Golden Set.

### Reply evaluation

Generated replies are evaluated using five dimensions:

- Relevance
- Groundedness
- Helpfulness
- Privacy
- Unsupported actions or policies

Each receives a score from 0–2.

### LLM-as-judge validation

A Gemini-based judge was tested against human scoring on an initial five-example sample.

The human scores matched the LLM judge exactly on all 25 individual dimension scores.

This is preliminary validation only because the sample size is small.

---

## 7. Results

### Intent classification

| System | Accuracy | Macro F1 | Training examples |
|---|---:|---:|---:|
| Majority baseline | 13.00% | 2.09% | 0 |
| TF-IDF + Logistic Regression | 33.50% | 28.54% | 549 |
| Current agent intent classifier | 33.50% | 28.54% | 549 |

The simple classifier substantially improves over the majority baseline:

- Accuracy increases from 13.00% to 33.50%.
- Macro F1 increases from 2.09% to 28.54%.

The current agent uses the same intent classifier, so its intent-classification performance is currently identical to the simple ML baseline.

This is an important result: the retrieval and generation components add support-agent functionality, but they have not yet improved the underlying intent classifier.

### Reply evaluation

On the initial five-example smoke-test sample, the LLM judge gave:

- Average total score: 10/10.
- Relevance: 2/2.
- Groundedness: 2/2.
- Helpfulness: 2/2.
- Privacy: 2/2.
- Unsupported actions/policies: 2/2.

Human scoring matched the LLM judge on all 25 individual dimension scores.

These results should be interpreted as a preliminary qualitative check rather than a final reply-quality benchmark because only five replies were evaluated.

---

## 8. Failure Analysis

The classifier made 133 mistakes out of 200 Golden Set examples.

The largest observed failure patterns are:

### 1. Billing/payment → other_unclear

**Frequency:** 11 cases

Example:

> hello! does spotify still take a visa gift card as a form of payment for premium?

The message contains "Premium", but the actual problem concerns payment methods. Shared vocabulary makes it difficult for the classifier to distinguish payment questions from subscription-related questions.

**Hypothesis:** TF-IDF relies heavily on lexical overlap and does not reliably identify the customer's primary intent.

**Potential improvement:** Add more diverse billing examples, especially payment-method questions, and consider hierarchical classification.

### 2. Download/offline → app_technical_issue

**Frequency:** 8 cases

Example:

> why do you try to download over 4g when cellular download is off? please look into this, I need to kill the app as a workaround.

The message contains general technical language such as "app" and describes an app workaround, while the primary problem is download behavior.

**Hypothesis:** The classifier struggles when a specific problem is expressed using broad technical vocabulary.

**Potential improvement:** Add more download/offline examples containing terms such as app, cellular, storage, and 4G.

### 3. Playback → content_library

**Frequency:** 7 cases

Example:

> Why is not playing trivium in spotify?

A named artist or song can make the message resemble a content-availability problem, even when the actual issue is playback.

**Hypothesis:** The classifier has difficulty distinguishing "content is missing" from "content exists but will not play."

**Potential improvement:** Add contrastive examples explicitly distinguishing missing content from playable-but-failing content.

### 4. Premium subscription → other_unclear

**Frequency:** 6 cases

Example:

> i've been paying for premium and i have spotify free... why?

Short messages provide limited lexical information even though the intended problem is understandable to a human.

**Hypothesis:** TF-IDF performs poorly when there is insufficient textual context.

**Potential improvement:** Add more short Premium-status examples and use uncertainty-aware escalation.

### 5. Student plan → overlapping intents

Student-plan errors are distributed across several categories:

- `student_plan → other_unclear`: 5
- `student_plan → account_access`: 5
- `student_plan → feature_feedback`: 4

Student-plan messages often mention accounts, verification, Premium, discounts, or product behavior, creating overlap with several categories.

**Hypothesis:** Lexical similarity makes it difficult to identify student-plan issues when the message contains vocabulary associated with other intents.

**Potential improvement:** Increase training coverage for student-plan examples and add contrastive examples separating student verification, account access, and feature requests.

### Overall failure pattern

The errors suggest three recurring weaknesses:

1. **Overlapping vocabulary** between intents.
2. **Short or ambiguous customer messages.**
3. **Multi-intent messages** where a customer describes several problems in one interaction.

These are important limitations of a lightweight single-label TF-IDF classifier.

---

## 9. What Is Misleading About My Headline Number?

The headline intent-classification accuracy is **33.50%**, but this number can be misleading if interpreted without context.

First, the number measures only **intent classification on a 200-example Golden Set**. It does not mean that only 33.5% of the complete support agent is useful.

Second, the agent contains additional components that the accuracy number does not measure:

- Historical retrieval.
- Evidence-based reply generation.
- Escalation decisions.
- Privacy and unsupported-action safeguards.

Third, accuracy alone hides uneven performance between intents. The macro F1 of **28.54%** shows that performance is not uniformly strong across the taxonomy.

Finally, the current agent's classifier is the same TF-IDF + Logistic Regression model used in the simple baseline. Therefore, the current 33.50% result should not be presented as evidence that the complete agent improves classification over the baseline.

The honest headline is:

> The lightweight classifier improves substantially over a trivial baseline, but intent classification remains the main weakness of the current system.

---

## 10. What I Would Do With One More Week

If given another week, I would prioritize improving reliability rather than adding more features.

### 1. Improve intent classification

Expand and rebalance the labelled training set, focusing on the failure modes identified above.

In particular, I would add contrastive examples for:

- Billing vs Premium.
- Playback vs content library.
- Download vs general app issues.
- Student plan vs account access.
- Feature requests vs technical problems.

### 2. Evaluate confidence calibration

The current classifier's maximum class probability is used as a rough confidence signal, but it is not calibrated probability.

I would evaluate calibration and tune the escalation threshold on a held-out validation set.

### 3. Improve retrieval evaluation

Instead of manually inspecting a few retrieval examples, I would create a small retrieval benchmark and measure whether the top-k historical cases are actually relevant to the customer's intent.

### 4. Expand reply evaluation

Evaluate a larger sample of generated replies using the rubric and compare LLM-judge scores against independent human scores.

### 5. Improve multi-intent handling

Introduce either multi-label classification or a primary-intent-plus-secondary-context representation for messages containing several problems.

### 6. Compare alternative classifiers

Test lightweight alternatives such as linear SVM or a sentence-embedding classifier before considering more expensive approaches.

The goal would be to determine whether better representations improve the difficult intent boundaries without unnecessarily increasing system complexity.

---

## 11. Decision Log Summary

Key non-obvious decisions made during the project include:

1. **Selected SpotifyCares** because it offered recurring support problems with sufficient data and a manageable scope.
2. **Reconstructed conversations using tweet IDs** rather than treating tweets independently.
3. **Used customer-support pairs** as the primary modelling unit.
4. **Derived a compact 11-intent taxonomy** rather than attempting to reproduce every possible issue.
5. **Used the customer's primary problem** as the labelling rule when messages contained multiple keywords.
6. **Included `other_unclear`** for genuinely ambiguous or out-of-scope messages.
7. **Created a 200-example Golden Set** to satisfy the assignment while keeping manual labelling manageable.
8. **Used a separate historical training sample** so the baseline would not train directly on Golden Set examples.
9. **Removed one overlapping training example** from the Golden Set to avoid evaluation leakage.
10. **Removed Golden Set messages from the retrieval corpus** to reduce direct retrieval leakage.
11. **Used TF-IDF + Logistic Regression** as an interpretable and lightweight baseline.
12. **Kept retrieval separate from classification** so evidence retrieval could be evaluated independently.
13. **Used historical responses as evidence rather than instructions** to reduce the risk of copying conversation-specific details.
14. **Escalated account-specific issues** because the system does not have authenticated access to customer accounts.
15. **Used an LLM judge with a structured five-dimension rubric** rather than relying only on a single qualitative score.
16. **Validated the judge against human scores** before treating its outputs as evaluation evidence.
17. **Did not treat the initial 5-example 100% judge score as final performance**, because the sample is too small.