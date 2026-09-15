import pytest
from dataset.build_dataset import load_dataset
from generator.knowledge_base import KnowledgeBase
from generator.prompts import build_generation_prompt, format_thread_history
from generator.engine import OfflineDeterministicEngine, get_generator


def test_knowledge_base_retrieval():
    kb = KnowledgeBase()
    assert len(kb.documents) >= 7

    # Retrieve refund policy
    docs = kb.retrieve("need a refund for annual plan", category="cancellation_refund")
    assert len(docs) > 0
    assert any("refund" in d["content"].lower() for d in docs)

    # Retrieve 2FA policy
    docs_sec = kb.retrieve("lost 2FA authenticator phone", category="account_access")
    assert len(docs_sec) > 0
    assert any("2fa" in d["content"].lower() for d in docs_sec)


def test_prompt_formatting():
    tickets = load_dataset()
    ticket = tickets[0]
    kb = KnowledgeBase()
    kb_context = kb.get_context_for_prompt("refund request", category=ticket.category)
    prompt = build_generation_prompt(ticket, kb_context)
    
    assert ticket.ticket_id in prompt or ticket.customer_context.account_id in prompt
    assert ticket.customer_context.plan_tier in prompt
    assert "Policy Doc" in prompt


def test_offline_generator_reply_quality():
    tickets = load_dataset()
    gen = get_generator(provider="mock")

    for t in tickets[:5]:
        reply = gen.generate(t)
        assert len(reply) > 50
        # Check that customer's first name or greeting is present
        assert any(greeting in reply.lower() for greeting in ["hi", "hello", "dear"])
        # Check sign-off
        assert any(signoff in reply.lower() for signoff in ["regards", "sincerely", "support team"])
