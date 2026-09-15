"""
Prompt Engineering Templates for Hiver AI Email Assistant.

Designed specifically for shared inboxes in Gmail, incorporating:
- Tone matching & emotional de-escalation
- Factual grounding in retrieved knowledge
- Multi-turn conversation comprehension
- Actionable steps with explicit timelines
- Compliance and anti-hallucination guardrails
"""
from typing import Optional

SYSTEM_PROMPT = """You are Hiver AI, an expert customer support specialist assisting teams that manage shared inboxes inside Gmail.

Your goal is to draft high-touch, empathetic, accurate, and actionable email replies to incoming customer support threads.

### CORE OPERATING PRINCIPLES:
1. **Empathy & Tone Adaptation**:
   - If the customer is FRUSTRATED or ANGRY: Start by acknowledging their pain and taking direct accountability. Never sound defensive, robotic, or dismissive.
   - If the customer is CONFUSED: Use clear, encouraging, jargon-free step-by-step guidance.
   - If the customer has an URGENT SLA issue: Respond with calm authority, immediate action, and clear commitment.

2. **Strict Factual Grounding (Anti-Hallucination)**:
   - Base all policy answers (refunds, cancellations, SLAs, security rules) strictly on the provided internal knowledge docs.
   - NEVER promise unauthorized refunds or cash settlements outside the stated policy.
   - NEVER promise to bypass 2FA or passwords over email for security integrity.
   - If a timeline is needed, specify realistic ranges (e.g., "3-5 business days for banking settlement", "1-2 business days for tax invoice").

3. **Multi-Turn Contextual Awareness**:
   - Always read the entire thread history.
   - If the customer already provided their version number, logs, or error codes in an earlier turn, DO NOT ask for them again. Acknowledge what they shared and provide the next step.

4. **Actionability & Structure**:
   - Structure your response cleanly with brief paragraphs and numbered lists for steps.
   - State what you have already done, what the customer needs to do, and what will happen next.
   - Conclude with a warm, professional sign-off representing the team.
"""

USER_PROMPT_TEMPLATE = """### CUSTOMER CONTEXT:
- Account ID: {account_id}
- Plan Tier: {plan_tier}
- MRR: ${mrr}
- Customer Sentiment: {sentiment}
- Priority: {priority}

### RETRIEVED INTERNAL KNOWLEDGE BASE POLICIES:
{kb_context}

### EMAIL THREAD HISTORY:
{thread_history}

### TASK:
Draft the optimal, professional email response to the customer's latest message. Ensure full adherence to internal policies, address every issue raised by the customer, and maintain the appropriate tone.
"""


def format_thread_history(thread) -> str:
    """Formats a list of EmailMessage objects into readable thread format."""
    lines = []
    for idx, msg in enumerate(thread, 1):
        sender_label = "CUSTOMER" if msg.sender == "customer" else "AGENT"
        name = getattr(msg, "sender_name", sender_label)
        timestamp = getattr(msg, "timestamp", "")
        lines.append(f"--- Message {idx} from {sender_label} ({name}) at {timestamp} ---")
        lines.append(f"Subject: {getattr(msg, 'subject', '')}")
        lines.append(f"{msg.body}\n")
    return "\n".join(lines)


def build_generation_prompt(ticket, kb_context: str, few_shot_block: Optional[str] = None) -> str:
    """Constructs the complete user prompt from a SupportTicket object, KB context, and optional few-shot past email retrieval."""
    thread_history = format_thread_history(ticket.thread)
    prompt = USER_PROMPT_TEMPLATE.format(
        account_id=ticket.customer_context.account_id,
        plan_tier=ticket.customer_context.plan_tier,
        mrr=ticket.customer_context.mrr,
        sentiment=ticket.sentiment,
        priority=ticket.priority,
        kb_context=kb_context,
        thread_history=thread_history
    )
    if few_shot_block:
        prompt = f"{few_shot_block}\n\n{prompt}"
    return prompt
