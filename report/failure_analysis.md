# Failure Analysis

## Overview

The current intent classifier achieves 33.50% accuracy and 28.54% macro F1 on the 200-example Golden Set.

It makes 133 classification mistakes out of 200 examples.

The main errors are concentrated in cases where multiple intents share similar vocabulary, where the customer describes multiple problems in one message, or where the distinction depends on the customer's primary problem rather than individual keywords.

## Top 5 Failure Modes

### 1. Billing/payment questions classified as other_unclear

**Example:**

> hello! does spotify still take a visa gift card as a form of payment for premium?

**Observed error:**

`billing_payment → other_unclear`

**Why it likely failed:**

The message contains "Premium", which appears frequently in several intents, while the actual question is about an accepted payment method.

**Hypothesis:**

The TF-IDF classifier relies too heavily on shared words such as "Premium" and does not reliably identify the customer's primary problem.

**Potential improvement:**

Add more diverse billing/payment training examples, particularly payment-method questions, and consider hierarchical classification where payment-related questions are identified before more specific subscription categories.

---

### 2. Download/offline problems classified as app_technical_issue

**Example:**

> why do you try to download over 4g when cellular download is off? please look into this, I need to kill the app as a workaround.

**Observed error:**

`download_offline → app_technical_issue`

**Why it likely failed:**

The message describes both downloading behavior and an app workaround. Words such as "app" may pull the classifier toward the broader technical-issue category.

**Hypothesis:**

The classifier struggles when a specific problem is described using general technical language.

**Potential improvement:**

Add more examples where download/offline problems contain words such as "app", "4G", "cellular", or "storage", and explicitly label the primary problem.

---

### 3. Playback problems classified as content_library

**Example:**

> Why is not playing trivium in spotify?

**Observed error:**

`playback_issue → content_library`

**Why it likely failed:**

The message contains a specific song/artist, making it resemble missing-content or library questions even though the actual problem is that the content will not play.

**Hypothesis:**

The classifier has difficulty distinguishing "content is missing" from "content exists but will not play."

**Potential improvement:**

Add contrastive examples covering:
- song is missing → `content_library`
- song exists but will not play → `playback_issue`

---

### 4. Premium subscription problems classified as other_unclear

**Example:**

> i've been paying for premium and i have spotify free... why?

**Observed error:**

`premium_subscription → other_unclear`

**Why it likely failed:**

The message is short and contains limited context. It describes a Premium/account-state problem but does not contain many distinctive words.

**Hypothesis:**

Short customer messages provide insufficient lexical information for the TF-IDF model.

**Potential improvement:**

Add more short examples describing Premium activation/status problems and use confidence-based escalation for ambiguous cases.

---

### 5. Student plan problems confused with overlapping intents

**Observed errors:**

- `student_plan → other_unclear`: 5
- `student_plan → account_access`: 5
- `student_plan → feature_feedback`: 4

**Why it likely failed:**

Student-plan messages often contain overlapping concepts such as account access, verification, Premium, discounts, or requests about how the product works. These words also appear in several other intent categories.

**Hypothesis:**

The TF-IDF classifier relies heavily on lexical similarity and has difficulty identifying the customer's primary intent when student-plan issues contain vocabulary associated with other categories.

**Potential improvement:**

Increase training coverage for student-plan examples, especially examples involving verification, eligibility, discounts, account access, and existing Premium subscriptions. Contrastive examples could also help distinguish student-plan problems from account-access and feature-feedback cases.