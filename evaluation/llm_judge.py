"""
LLM-as-a-Judge Evaluation Module for Hiver AI.

Provides qualitative and quantitative grading of email replies
using LLMs when external API keys (OpenAI / Gemini) are supplied.
"""

import os
import json
from typing import Optional, Dict, Any
from dataset.schema import SupportTicket


LLM_JUDGE_PROMPT = """You are an expert Customer Support Quality Assurance auditor at Hiver.
Evaluate the following generated customer support email reply against the provided Customer Context, Internal Policies, Email Thread, and Ground Truth Golden Reference.

### EVALUATION CRITERIA:
1. Policy Adherence (0-100): Does the reply respect all company policies and avoid prohibited promises?
2. Intent Resolution (0-100): Did the reply address every query and pain point raised by the customer?
3. Tone & Empathy (0-100): Is the tone warm, professional, and appropriately de-escalating for frustrated/angry customers?
4. Actionability (0-100): Are next steps, timelines, and instructions explicit and easy to follow?

### OUTPUT FORMAT:
Respond ONLY with a valid JSON object matching this schema:
{
  "policy_score": <number 0-100>,
  "intent_score": <number 0-100>,
  "tone_score": <number 0-100>,
  "actionability_score": <number 0-100>,
  "strengths": ["<string>", ...],
  "improvements": ["<string>", ...],
  "rationale": "<summary explanation>"
}
"""


class LLMJudge:
    """Evaluates support email quality using LLM-as-a-judge."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.client = None
        if self.api_key:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=self.api_key)
            except Exception as e:
                print(f"[LLMJudge] Could not initialize OpenAI client: {e}")

    def judge(self, ticket: SupportTicket, generated_reply: str) -> Optional[Dict[str, Any]]:
        """Judges a generated reply using an LLM auditor."""
        if not self.client:
            return None

        user_content = f"""
### CUSTOMER & TICKET CONTEXT:
- Category: {ticket.category}
- Priority: {ticket.priority}
- Customer Sentiment: {ticket.sentiment}
- Plan Tier: {ticket.customer_context.plan_tier}

### REQUIRED RUBRIC FACTS:
{ticket.rubric.required_facts}

### PROHIBITED CLAIMS:
{ticket.rubric.prohibited_claims}

### GENERATED REPLY TO EVALUATE:
{generated_reply}

### GROUND TRUTH REFERENCE:
{ticket.ground_truth_reply}
"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": LLM_JUDGE_PROMPT},
                    {"role": "user", "content": user_content}
                ],
                response_format={"type": "json_object"},
                temperature=0.1
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"[LLMJudge] Evaluation failed: {e}")
            return None
