import pytest
from pathlib import Path
from dataset.build_dataset import load_dataset, get_dataset_statistics, export_to_csv
from dataset.schema import SupportTicket


def test_dataset_loading():
    tickets = load_dataset()
    assert len(tickets) >= 20
    assert all(isinstance(t, SupportTicket) for t in tickets)


def test_ticket_schema_attributes():
    tickets = load_dataset()
    for t in tickets:
        assert t.ticket_id.startswith("TICK-")
        assert t.category in [
            "billing", "technical_issue", "account_access",
            "cancellation_refund", "feature_request", "sla_escalation", "onboarding"
        ]
        assert t.sentiment in ["frustrated", "angry", "urgent", "neutral", "confused", "satisfied"]
        assert t.customer_context.plan_tier in ["Free", "Starter", "Pro", "Enterprise"]
        assert len(t.thread) >= 1
        assert len(t.ground_truth_reply) > 20
        assert len(t.rubric.required_facts) >= 1


def test_dataset_statistics():
    tickets = load_dataset()
    stats = get_dataset_statistics(tickets)
    assert stats["total_tickets"] == len(tickets)
    assert "technical_issue" in stats["categories"]
    assert "billing" in stats["categories"]
    assert "frustrated" in stats["sentiments"]


def test_csv_export(tmp_path):
    tickets = load_dataset()
    csv_file = tmp_path / "test_export.csv"
    export_to_csv(tickets, csv_path=csv_file)
    assert csv_file.exists()
    assert csv_file.stat().st_size > 500
