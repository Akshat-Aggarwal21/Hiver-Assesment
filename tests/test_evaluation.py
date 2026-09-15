import pytest
from dataset.build_dataset import load_dataset
from evaluation.metrics import EmailMetricsCalculator
from evaluation.evaluator import HiverEvaluator


def test_metrics_calculator():
    calc = EmailMetricsCalculator()
    tickets = load_dataset()
    ticket = tickets[0]

    # Evaluate ground truth against itself (should score very high)
    scores, matched, violations, addressed, missing = calc.calculate_all(ticket.ground_truth_reply, ticket)
    assert scores.composite_heqi >= 85.0
    assert scores.policy_adherence_score >= 80.0
    assert scores.tone_empathy_score >= 80.0
    assert scores.actionability_score >= 70.0
    assert scores.semantic_similarity >= 95.0
    assert len(violations) == 0


def test_evaluator_single_ticket():
    evaluator = HiverEvaluator()
    tickets = load_dataset()
    res = evaluator.evaluate_ticket(tickets[0])
    
    assert res.ticket_id == tickets[0].ticket_id
    assert res.scores.composite_heqi > 0
    assert len(res.strengths) >= 1
    assert res.reasoning is not None


def test_evaluator_all_benchmark():
    evaluator = HiverEvaluator()
    tickets = load_dataset()[:5]  # Test subset for rapid verification
    results, summary = evaluator.evaluate_all(tickets)
    
    assert len(results) == 5
    assert summary.total_tickets == 5
    assert summary.mean_heqi > 70.0
    assert summary.mean_policy_adherence > 70.0
    assert "cancellation_refund" in summary.category_breakdown or "technical_issue" in summary.category_breakdown
