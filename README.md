# Hiver SDE Intern Take-Home - AI Customer Support Agent

An end-to-end customer support agent built using historical Twitter support conversations from the Kaggle Customer Support on Twitter dataset.

The project focuses on one support brand, **SpotifyCares**, and explores whether a lightweight intent classifier, historical retrieval, escalation logic, and an LLM-generated response can provide useful and safe support automation.

---

## 1. Problem

The goal is to build an AI support agent that can:

1. Classify an incoming customer message into a small set of support intents.
2. Retrieve historically similar customer-support interactions.
3. Draft a response grounded in how SpotifyCares historically handled similar issues.
4. Decide whether the case can be auto-handled or should be escalated to a human.

The project prioritizes measurable evidence over building a large or complicated system.

---

## 2. Dataset

The project uses the Kaggle **Customer Support on Twitter** dataset:

`thoughtvector/customer-support-on-twitter`

The raw dataset is not committed to the repository because of its size.

Expected local location:

`data/raw/twcs/twcs.csv`

The selected brand is **SpotifyCares**.

---

## 3. Conversation Reconstruction

The raw dataset contains tweets and reply relationships rather than ready-made customer-support pairs.

The project reconstructs customer â†’ support interactions using:

- `in_response_to_tweet_id`
- `response_tweet_id`

The resulting SpotifyCares pairs are stored in:

`data/processed/spotify_pairs.csv`

After text cleaning:

`data/processed/spotify_pairs_clean.csv`

The cleaned dataset contains **43,076 customer-support interactions**.

---

## 4. Intent Taxonomy

Eleven intents were defined from the observed SpotifyCares support data:

- `account_access` - Login, password, hacked account, account access
- `premium_subscription` - Premium activation/status, cancellation, subscription changes
- `billing_payment` - Charges, duplicate charges, refunds, payment failures, payment methods
- `family_plan` - Family plan setup, members, invitations, verification
- `student_plan` - Student discount, verification, eligibility
- `app_technical_issue` - App bugs, crashes, search problems, app malfunction
- `playback_issue` - Songs stopping/not playing, shuffle/repeat problems
- `content_library` - Missing songs/albums, playlists, library and curation
- `download_offline` - Downloaded/offline music problems
- `feature_feedback` - Feature requests and product suggestions
- `other_unclear` - Outside the defined categories or insufficient information

Messages were labeled according to the **primary customer problem**, rather than simply matching keywords.
---

## 5. Evaluation Data

A manually labeled **Golden Set of 200 examples** was created for evaluation.

The Golden Set is stored at:

`evaluation/golden_set.csv`

The examples cover all 11 intents.

A separate manually labeled training sample contains **549 examples** after removing an exact overlap with the Golden Set.

Training data:

`evaluation/training_clean.csv`

The separation between training and evaluation data was used to avoid evaluating the classifier on examples it had already seen during training.

---

## 6. Baseline Results

Two intent-classification baselines were implemented.

### Baseline 1 - Majority Class

The trivial baseline always predicts the most common intent in the Golden Set.

Most common intent:

`feature_feedback`

Results:

| Metric | Score |
|---|---:|
| Accuracy | 13.00% |
| Macro F1 | 2.09% |

This provides a simple lower-bound benchmark.

### Baseline 2 - TF-IDF + Logistic Regression

The simple ML baseline uses:

- TF-IDF features
- unigram and bigram features
- Logistic Regression
- 549 manually labeled training examples
- 200-example Golden Set

Results:

| Metric | Score |
|---|---:|
| Accuracy | 33.50% |
| Macro F1 | 28.54% |

This is substantially better than the majority-class baseline, but performance remains limited on several overlapping intents.

---

## 7. AI Support Agent

The support agent combines four components:

### 7.1 Intent Classification

The same TF-IDF + Logistic Regression classifier predicts the customer's intent.

The classifier also provides its highest class probability, which is used as an engineering signal for escalation.

### 7.2 Historical Retrieval

The system retrieves the top 3 historically similar SpotifyCares customer-support interactions.

Retrieval uses:

- TF-IDF
- unigram and bigram features
- cosine similarity

The retrieved historical responses provide evidence for drafting the new response.

### 7.3 Escalation

The agent considers:

- classifier confidence,
- strength of historical evidence,
- whether the intent may require account-specific investigation.

Account-specific intents such as billing, account access, subscriptions, family plans, and student plans are treated more cautiously.

The current thresholds are engineering assumptions and have not yet been calibrated on a dedicated escalation benchmark.

### 7.4 Grounded Reply Generation

The response generator uses **Gemini 2.5 Flash**.

The prompt provides:

- the customer message,
- predicted intent,
- classifier confidence,
- retrieved historical customer messages,
- retrieved historical support responses.

Historical responses are treated as evidence rather than instructions.

The generator is explicitly instructed not to:

- invent policies,
- invent refunds or procedures,
- claim actions were completed,
- expose internal tweet IDs or usernames,
- reveal internal reasoning.

For account-specific issues, the response can direct the customer toward a private support channel.

---

## 8. Reply Evaluation

A five-dimension rubric was created to evaluate generated replies:

1. Relevance
2. Groundedness
3. Helpfulness
4. Safety / Privacy
5. Unsupported Actions / Policies

Each dimension receives a score from 0 to 2, for a maximum total of 10.

The rubric is stored in:

`evaluation/reply_rubric.md`

A preliminary LLM-as-judge smoke test was run on 5 generated replies.

The 5-example sample received:

- Average total score: **10/10**
- All five dimensions: **2.00/2.00**

A human validation of the same 5 examples also produced:

- **25/25 exact dimension-level agreement**

This is only a preliminary judge validation on 5 examples, not a claim of general judge reliability.

---

## 9. Current Results

The current headline intent-classification results are:

| System | Accuracy | Macro F1 |
|---|---:|---:|
| Majority baseline | 13.00% | 2.09% |
| TF-IDF + Logistic Regression | 33.50% | 28.54% |
| Current agent classifier | 33.50% | 28.54% |

The current agent uses the same classifier as the simple ML baseline, so the agent should **not** be presented as having better intent-classification performance.

Its additional value comes from combining classification with historical retrieval, grounded reply generation, and escalation logic.

---

## 10. Failure Analysis

The main observed classification failures were:

1. `billing_payment` â†’ `other_unclear`
2. `download_offline` â†’ `app_technical_issue`
3. `playback_issue` â†’ `content_library`
4. `premium_subscription` â†’ `other_unclear`
5. `student_plan` â†’ several overlapping intents

The failures show that many SpotifyCares issues share vocabulary.

For example, messages about Premium may also involve billing, account access, or technical problems. Download and playback issues can also look like general app problems.

Multi-issue customer messages are particularly difficult because the current taxonomy requires one primary intent.

Detailed examples and hypotheses are documented in:

`report/failure_analysis.md`

---

## 11. What Is Misleading About My Headline Number?

The **33.50% accuracy** result is useful, but it should not be interpreted as saying that the complete support agent successfully handles only 33.5% of customers.

The number measures **intent classification accuracy on a 200-example manually labeled Golden Set**.

It does not directly measure:

- whether a retrieved historical case is useful,
- whether a generated reply solves the customer's problem,
- whether escalation decisions are correct,
- customer satisfaction,
- production performance.

The reply evaluation is also currently only a small smoke test of 5 examples.

Therefore, the headline number is best interpreted as evidence about the current classifier, not the complete quality of the support agent.

---

## 12. What I Would Do With One More Week

With another week, I would prioritize:

### 1. Improve intent classification

Compare the current TF-IDF baseline with stronger lightweight approaches and investigate class-specific errors.

### 2. Calibrate confidence

The current classifier probability is used only as an escalation signal. I would calibrate it and select thresholds using a dedicated validation set.

### 3. Evaluate retrieval quantitatively

Instead of only qualitative smoke tests, create labeled retrieval cases and measure whether relevant historical resolutions appear in the top-k results.

### 4. Expand reply evaluation

Evaluate a substantially larger sample of generated replies using both the LLM judge and human validation.

### 5. Handle multi-intent messages

Allow multiple intents or explicitly detect multi-issue messages before selecting the primary support path.

---

## 13. Repository Structure

```text
hiver-support-agent/
â”œâ”€â”€ data/
â”‚   â”œâ”€â”€ raw/
â”‚   â””â”€â”€ processed/
â”œâ”€â”€ evaluation/
â”‚   â”œâ”€â”€ results/
â”‚   â”œâ”€â”€ golden_set.csv
â”‚   â”œâ”€â”€ training_clean.csv
â”‚   â””â”€â”€ reply_rubric.md
â”œâ”€â”€ report/
â”‚   â”œâ”€â”€ failure_analysis.md
â”‚   â””â”€â”€ report.md
â”œâ”€â”€ src/
â”‚   â”œâ”€â”€ agent.py
â”‚   â”œâ”€â”€ classifier.py
â”‚   â”œâ”€â”€ retrieval.py
â”‚   â”œâ”€â”€ escalation.py
â”‚   â”œâ”€â”€ reply.py
â”‚   â””â”€â”€ evaluation / analysis scripts
â”œâ”€â”€ decision_log.md
â”œâ”€â”€ requirements.txt
â”œâ”€â”€ .env.example
â””â”€â”€ README.md

## 14. Reproducibility

Create and activate a virtual environment:

    python -m venv .venv
    .venv\Scripts\Activate.ps1

Install dependencies:

    pip install -r requirements.txt

### Reproduce the intent-classification results

    python src/baseline_majority.py
    python src/evaluate_baseline_ml.py

### Run the support agent

Set the Gemini API key in `.env`:

    GEMINI_API_KEY=your_api_key_here

Then run:

    python src/agent.py

### Run reply evaluation

    python src/evaluate_replies.py
    python src/evaluate_reply_scores.py

### Run the LLM judge

    python src/run_llm_judge.py
    python src/compare_human_llm_judge.py

The headline intent results can be reproduced from the included processed evaluation data without rerunning the full raw Twitter dataset.

---

## 15. Design Philosophy

The project follows a simple principle:

**Build â†’ Measure â†’ Explain**

Rather than optimizing for system complexity, the implementation focuses on:

- a clearly defined problem,
- reproducible data preparation,
- manually labeled evaluation data,
- meaningful baselines,
- grounded historical evidence,
- explicit escalation logic,
- measurable failure analysis,
- honest reporting of limitations.

