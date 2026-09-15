# Hiver AI — Shared Inbox Email Copilot & Evaluation Suite

> **100-Minute Open Challenge Submission for Hiver**  
> An end-to-end Gen-AI system designed for teams running customer email at scale inside Gmail shared inboxes. Features a realistic multi-turn dataset, policy-grounded response generation, a multi-dimensional accuracy evaluation framework (HEQI), a rich CLI, and an interactive Web Dashboard.

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![Tests Passing](https://img.shields.io/badge/tests-16%20passed-success.svg)](file:///e:/Hiver%20Assesment%201/tests)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 1. System Architecture

```
                                  +---------------------------------------+
                                  |     Hiver Shared Inbox Dataset        |
                                  | (20 Multi-turn tickets, Sentiment,    |
                                  |  SLA Tiers, Context, Golden Truth)    |
                                  +-------------------+-------------------+
                                                      |
                                                      v
  +--------------------------+          +---------------------------------+
  | Internal Knowledge Base  | -------> |  Gen-AI Response Engine         |
  | (Refund Rules, SLAs,     |   (RAG)  |  - Tone & Empathy Adaptation    |
  |  Troubleshooting, Runbook)          |  - Multi-Turn Context Memory    |
  +--------------------------+          |  - Anti-Hallucination Grounding |
                                        +----------------+----------------+
                                                         |
                                                         | Generated Email Reply
                                                         v
                                        +---------------------------------+
                                        |   Multi-Dimensional Evaluator   |
                                        |       (HEQI Metric Suite)       |
                                        |  * Policy Adherence (30%)       |
                                        |  * Intent Resolution (25%)      |
                                        |  * Tone & Empathy (20%)         |
                                        |  * Actionability (15%)          |
                                        |  * Semantic Similarity (10%)    |
                                        +----------------+----------------+
                                                         |
                         +-------------------------------+-------------------------------+
                         |                                                               |
                         v                                                               v
           +---------------------------+                                   +---------------------------+
           |  Interactive Web App UI   |                                   |       Automated CLI       |
           |  (Live Generation, Gmail  |                                   | (Batch Benchmarks, JSON   |
           |  Composer & Scorecards)   |                                   |  & Markdown Reports)      |
           +---------------------------+                                   +---------------------------+
```

---

## 2. The Dataset & Construction Methodology

### Why Real Support Requires Multi-Turn Context
Naive support datasets evaluate single prompts in isolation. In reality, shared inboxes in Gmail (like `support@company.com`) handle complex customer dialogues:
* **Multi-turn back-and-forth**: Customers reply with error codes, Chrome extension versions, or attachments. The AI must acknowledge previously shared information rather than asking redundant questions.
* **Customer Sentiment & SLA Urgency**: An Enterprise customer experiencing a sync outage during a flash sale requires an authoritative live bridge; a confused starter customer needs warm step-by-step guidance.
* **Account Metadata**: Context like Account ID, ARR/MRR, renewal dates, and payment history dictate what actions are legally or operationally allowed.

### Dataset Composition (`data/support_tickets.json` & `.csv`)
The dataset contains **20 realistic shared inbox support tickets** across 7 core categories:

| Category | Count | Scenarios Covered |
| :--- | :---: | :--- |
| `technical_issue` | 5 | Gmail sync lag, OAuth refresh, collision detection drop, 504 extension crashes, CSV export timeouts |
| `cancellation_refund`| 3 | 14-day money-back guarantee, 6-month non-usage goodwill compromise, trial auto-conversion refund |
| `account_access` | 3 | Lost 2FA phone protocol, Okta SAML Audience URI mismatch, former employee ownership transfer |
| `billing` | 3 | German VAT tax invoice update, mid-cycle seat proration calculation, 501(c)(3) tax exemption |
| `sla_escalation` | 2 | 1-hour Enterprise SLA breach with PIR credit, 45-minute countdown flash sale outage |
| `feature_request` | 2 | HubSpot bi-directional sync (roadmap Q4), native iOS & Android mobile apps |
| `onboarding` | 2 | Setting up round-robin auto-assignment, newly invited agents missing shared inbox |

### Dataset Builder & Exporter (`dataset/build_dataset.py`)
Run the dataset builder script to inspect, validate, and export flattened CSV data:
```bash
python -m dataset.build_dataset
```
Output:
* Validates every ticket against Pydantic schema (`dataset/schema.py`).
* Generates flattened `data/support_tickets.csv` for data exploration.
* Prints distribution statistics across sentiment, categories, and account tiers.

---

## 3. The Gen-AI Response Generator

The generator (`generator/`) is built specifically for shared inboxes in Gmail:
1. **RAG Knowledge Retrieval (`generator/knowledge_base.py`)**:
   - Matches incoming queries against internal company policies (`knowledge/kb_documents.json`) with keyword and category boosting.
   - Injects verified policy text directly into the system prompt to eliminate hallucinations.
2. **Context-Aware Prompt Engineering (`generator/prompts.py`)**:
   - Enforces empathy openers for angry/frustrated clients.
   - Enforces strict compliance (e.g. agents cannot disable 2FA over email; refunds beyond 30 days are account credits).
   - Generates numbered, actionable checklists and concrete timelines (e.g., "3-5 business days").
3. **Multi-Backend Architecture (`generator/engine.py`)**:
   - **`OfflineDeterministicEngine`**: Built-in intelligent engine with rule-based heuristics and RAG synthesis. **Runs 100% out of the box with zero API keys or external dependencies!**
   - **`OpenAIEngine`**: Integrates `gpt-4o-mini` / `gpt-4o` when `OPENAI_API_KEY` is present.
   - **`GeminiEngine`**: Integrates Google Gemini 1.5 when `GEMINI_API_KEY` is present.

---

## 4. The Accuracy & Evaluation System

### Why Naive Metrics (BLEU, ROUGE) Fail for Customer Support
Standard NLP benchmarks rely on surface n-gram overlap against a reference text:
1. **Multiple Valid Formulations**: A support reply can say: *"I have issued a full refund of $1,440 back to your card and cancelled your plan."* Another valid reply can say: *"Your account has been terminated and $1,440 was reimbursed to your Amex."* These have almost zero n-gram overlap (scoring low BLEU/ROUGE), yet both are 100% correct!
2. **Dangerous Hallucination Blindness**: A model can copy 80% of words from the customer prompt, earning a high ROUGE score, while inserting a catastrophic error (e.g. *"I have bypassed 2FA and reset your password over email"* or *"We cannot refund your money"*).

### The Hiver Email Quality Index (HEQI)
To solve this, we engineered **HEQI (0 to 100)**, a multi-dimensional rubric that measures what customer support leaders actually care about:

$$\text{HEQI} = \max\Big(0,\; 0.30 \times \text{Policy} + 0.25 \times \text{Intent} + 0.20 \times \text{Tone} + 0.15 \times \text{Actionability} + 0.10 \times \text{Semantic} - \text{Penalties}\Big)$$

1. **Policy & Factual Adherence (30% Weight)**:
   - Validates that required company policies (14-day refund rule, OAuth re-authorization, 2FA security protocols, SLA credit commitments) are satisfied.
   - Applies **severe 35-point penalties** for prohibited claims (e.g., promising manual 2FA bypass over unverified email, or falsely denying valid refunds).
2. **Intent Resolution & Completeness (25% Weight)**:
   - Verifies that all questions, error codes (e.g. 504, Audience URI mismatch), and customer pain points are addressed.
   - Preserves critical prompt entities (invoice IDs, account numbers, dollar amounts).
3. **Tone, Empathy & De-escalation (20% Weight)**:
   - Detects customer sentiment (`angry`, `frustrated`, `confused`, `urgent`).
   - Requires explicit de-escalation ("I sincerely apologize for this disruption", taking personal ownership) for upset customers.
4. **Actionability & Clarity (15% Weight)**:
   - Checks for structured step-by-step numbered instructions, clear navigation paths (`Settings > ...`), and concrete timelines (`3-5 business days`).
5. **Semantic Similarity (10% Weight)**:
   - Measures cosine similarity against the senior support golden reference reply.

### Confidence Grades
* **Score ≥ 85.0 (Exceptional)**: High confidence — ready for automated draft suggestion or 1-click agent sending.
* **Score 70.0 - 84.9 (Good Draft)**: Solid foundation — recommended for agent review.
* **Score < 70.0 (Needs Review)**: Flagged for missing policy facts or insufficient de-escalation.

---

## 5. Benchmark Results

Running the automated benchmark across all 20 dataset tickets yields:

```text
========================================================
   HIVER AI EMAIL QUALITY BENCHMARK (HEQI EVALUATION)   
========================================================
Metric                           | Score     
----------------------------------------------
Overall Mean HEQI                | 83.18 / 100
Mean Policy Adherence            | 84.92%
Mean Intent Resolution           | 72.06%
Mean Tone & Empathy              | 95.75%
Mean Actionability               | 86.0%
Mean Semantic Similarity         | 76.37%
Mean ROUGE-L F1                  | 0.5591
High Performers (HEQI >= 85)     | 8 / 20
Low Performers  (HEQI < 70)      | 1 / 20
```

### Performance by Category
| Category | Ticket Count | Mean HEQI Score |
| :--- | :---: | :---: |
| `cancellation_refund` | 3 | **88.35** |
| `billing` | 3 | **86.87** |
| `feature_request` | 2 | **83.59** |
| `onboarding` | 2 | **82.97** |
| `technical_issue` | 5 | **81.04** |
| `account_access` | 3 | **80.70** |
| `sla_escalation` | 2 | **78.72** |

### Performance by Customer Sentiment
| Customer Sentiment | Ticket Count | Mean HEQI Score |
| :--- | :---: | :---: |
| `neutral` | 4 | **85.44** |
| `angry` | 3 | **84.84** |
| `frustrated` | 5 | **84.81** |
| `urgent` | 4 | **80.61** |
| `confused` | 4 | **80.19** |

---

## 6. Quickstart Guide (How to Run)

### Prerequisites
* Python 3.10 or higher.
* All core dependencies install in under 30 seconds.

```bash
# Clone the repository
git clone <YOUR_REPO_URL>
cd "Hiver Assesment 1"

# Install dependencies
pip install -r requirements.txt
```

### Option A: Interactive Web Dashboard (Recommended)
Launch the web app on `http://127.0.0.1:8000`:
```bash
python run_app.py
```
* **Browse Tickets**: Filter by category or search shared inbox messages.
* **Inspect RAG**: See which internal policies grounded each reply.
* **Live AI Generation**: Generate replies with customized instructions.
* **Live Scorecard**: Edit any draft and see HEQI scores recalculate in real-time.
* **1-Click Benchmark**: Run the benchmark suite across all tickets and export reports.

### Option B: Command Line Interface (CLI)

```bash
# 1. Run full benchmark evaluation across the dataset
python -m hiver_ai.cli evaluate

# 2. Evaluate a specific ticket with detailed scorecard
python -m hiver_ai.cli evaluate --ticket-id TICK-101

# 3. Generate an AI reply for any ticket
python -m hiver_ai.cli generate --ticket-id TICK-102

# 4. View dataset distribution statistics
python -m hiver_ai.cli dataset-stats

# 5. Inspect multi-turn thread history and ground truth
python -m hiver_ai.cli inspect-ticket --ticket-id TICK-105
```

### Option C: Run Automated Tests
```bash
python -m pytest -v
```
All 16 unit tests covering dataset schemas, RAG retrieval, generators, evaluation metrics, and FastAPI endpoints pass with 100%.

---

## 7. Project Structure

```
├── data/
│   ├── support_tickets.json       # 20 curated shared inbox support tickets
│   └── support_tickets.csv        # Flattened tabular export for analysis
├── dataset/
│   ├── __init__.py
│   ├── schema.py                  # Pydantic models for tickets, threads & rubrics
│   └── build_dataset.py           # Dataset builder, validator & stats calculator
├── knowledge/
│   └── kb_documents.json          # Internal knowledge base policies & SLAs
├── generator/
│   ├── __init__.py
│   ├── knowledge_base.py          # RAG retrieval with keyword & category boosting
│   ├── prompts.py                 # System & user prompt templates
│   └── engine.py                  # Multi-provider generator (Offline/OpenAI/Gemini)
├── evaluation/
│   ├── __init__.py
│   ├── metrics.py                 # HEQI composite & granular sub-score calculations
│   ├── evaluator.py               # Batch benchmark runner & report exporter
│   └── llm_judge.py               # Optional LLM-as-a-judge auditor module
├── hiver_ai/
│   ├── __init__.py
│   └── cli.py                     # Rich command-line interface
├── web/
│   ├── __init__.py
│   ├── server.py                  # FastAPI server with REST endpoints
│   └── static/
│       ├── index.html             # Glassmorphic shared inbox dashboard
│       ├── style.css              # Custom modern dark UI stylesheet
│       └── app.js                 # Interactive frontend logic & charts
├── reports/
│   ├── evaluation_report.json     # Machine-readable benchmark results
│   └── evaluation_report.md       # Human-readable benchmark report
├── tests/
│   ├── test_dataset.py            # Schema & data validation tests
│   ├── test_generator.py          # RAG & reply generation tests
│   ├── test_evaluation.py         # HEQI scoring & rubric tests
│   └── test_api.py                # FastAPI endpoint integration tests
├── conftest.py                    # Pytest configuration
├── run_app.py                     # 1-click application runner
├── requirements.txt               # Dependencies
├── .env.example                   # Environment configuration template
└── README.md                      # Documentation
```

---

## 8. License

This repository is submitted as part of the Hiver Open Challenge and is released under the [MIT License](LICENSE).
