"""
Core Evaluation Engine for Hiver AI.

Coordinates:
- Single-ticket evaluation with detailed scorecard
- Batch dataset evaluation and benchmarking
- Aggregation across ticket categories and customer sentiment
- Exporting evaluation reports to JSON and Markdown
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

from dataset.schema import (
    SupportTicket,
    TicketEvaluationResult,
    BenchmarkSummary,
    EvaluationScores
)
from dataset.build_dataset import load_dataset
from generator.engine import BaseResponseGenerator, get_generator
from evaluation.metrics import EmailMetricsCalculator


class HiverEvaluator:
    """Evaluates AI email replies against human gold standard and rubric."""

    def __init__(self, generator: Optional[BaseResponseGenerator] = None):
        self.generator = generator or get_generator()
        self.metrics_calculator = EmailMetricsCalculator()

    def evaluate_ticket(
        self,
        ticket: SupportTicket,
        generated_reply: Optional[str] = None
    ) -> TicketEvaluationResult:
        """Evaluates a single ticket. Generates reply if not provided."""
        if not generated_reply:
            generated_reply = self.generator.generate(ticket)

        scores, matched_facts, violations, addressed_pts, missing_pts = (
            self.metrics_calculator.calculate_all(generated_reply, ticket)
        )

        strengths = []
        improvements = []

        if scores.policy_adherence_score >= 80:
            strengths.append(f"Strong policy adherence ({len(matched_facts)} required facts covered)")
        else:
            improvements.append("Ensure all required policy terms and timelines are explicitly mentioned")

        if scores.intent_resolution_score >= 80:
            strengths.append("Comprehensive intent coverage addressing customer questions")
        else:
            if missing_pts:
                improvements.append(f"Did not fully address: {', '.join(missing_pts[:2])}")

        if scores.tone_empathy_score >= 85:
            strengths.append("Excellent empathetic tone and de-escalation demeanor")
        elif scores.tone_empathy_score < 70:
            improvements.append("Tone lacks required warmth or emotional de-escalation for frustrated customer")

        if scores.actionability_score >= 80:
            strengths.append("Clear actionable steps and diagnostic instructions provided")
        else:
            improvements.append("Add numbered steps or explicit next actions to improve clarity")

        if violations:
            improvements.append(f"Policy violation detected: {', '.join(violations)}")

        reasoning = (
            f"Overall HEQI Score: {scores.composite_heqi}/100. "
            f"Policy adherence scored {scores.policy_adherence_score}%, intent resolution {scores.intent_resolution_score}%, "
            f"tone/empathy {scores.tone_empathy_score}%, actionability {scores.actionability_score}%, "
            f"and semantic similarity to ground truth is {scores.semantic_similarity}%."
        )

        return TicketEvaluationResult(
            ticket_id=ticket.ticket_id,
            category=ticket.category,
            generated_reply=generated_reply,
            ground_truth_reply=ticket.ground_truth_reply,
            scores=scores,
            strengths=strengths,
            areas_for_improvement=improvements,
            policy_violations_detected=violations,
            unaddressed_customer_points=missing_pts,
            reasoning=reasoning
        )

    def evaluate_all(
        self,
        tickets: Optional[List[SupportTicket]] = None
    ) -> Tuple[List[TicketEvaluationResult], BenchmarkSummary]:
        """Evaluates all tickets in dataset and calculates aggregate benchmark metrics."""
        if tickets is None:
            tickets = load_dataset()

        results: List[TicketEvaluationResult] = []
        for t in tickets:
            res = self.evaluate_ticket(t)
            results.append(res)

        # Aggregate statistics
        total = len(results)
        mean_heqi = sum(r.scores.composite_heqi for r in results) / total
        mean_policy = sum(r.scores.policy_adherence_score for r in results) / total
        mean_intent = sum(r.scores.intent_resolution_score for r in results) / total
        mean_tone = sum(r.scores.tone_empathy_score for r in results) / total
        mean_action = sum(r.scores.actionability_score for r in results) / total
        mean_semantic = sum(r.scores.semantic_similarity for r in results) / total
        mean_rougeL = sum(r.scores.rougeL_f1 for r in results) / total

        cat_groups: Dict[str, List[float]] = {}
        sent_groups: Dict[str, List[float]] = {}

        for r in results:
            cat_groups.setdefault(r.category, []).append(r.scores.composite_heqi)

        for t, r in zip(tickets, results):
            sent_groups.setdefault(t.sentiment, []).append(r.scores.composite_heqi)

        category_breakdown = {
            cat: {
                "mean_heqi": round(sum(scores) / len(scores), 2),
                "count": len(scores)
            }
            for cat, scores in cat_groups.items()
        }

        sentiment_breakdown = {
            sent: {
                "mean_heqi": round(sum(scores) / len(scores), 2),
                "count": len(scores)
            }
            for sent, scores in sent_groups.items()
        }

        high_perf = sum(1 for r in results if r.scores.composite_heqi >= 85.0)
        low_perf = sum(1 for r in results if r.scores.composite_heqi < 70.0)

        summary = BenchmarkSummary(
            total_tickets=total,
            mean_heqi=round(mean_heqi, 2),
            mean_policy_adherence=round(mean_policy, 2),
            mean_intent_resolution=round(mean_intent, 2),
            mean_tone_empathy=round(mean_tone, 2),
            mean_actionability=round(mean_action, 2),
            mean_semantic_similarity=round(mean_semantic, 2),
            mean_rougeL=round(mean_rougeL, 4),
            category_breakdown=category_breakdown,
            sentiment_breakdown=sentiment_breakdown,
            high_performers_count=high_perf,
            low_performers_count=low_perf
        )

        return results, summary

    @staticmethod
    def export_report_json(
        results: List[TicketEvaluationResult],
        summary: BenchmarkSummary,
        output_path: Path
    ) -> None:
        """Exports benchmark results to a formatted JSON file."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "summary": summary.model_dump(),
            "results": [r.model_dump() for r in results]
        }
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    @staticmethod
    def export_report_markdown(
        results: List[TicketEvaluationResult],
        summary: BenchmarkSummary,
        output_path: Path
    ) -> None:
        """Exports a human-readable Markdown evaluation report."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        lines = [
            "# Hiver AI Email Evaluation & Benchmark Report",
            "",
            "## Executive Summary",
            f"- **Total Tickets Evaluated**: {summary.total_tickets}",
            f"- **Overall Mean HEQI Score**: **{summary.mean_heqi} / 100**",
            f"- **Policy & Factual Adherence**: {summary.mean_policy_adherence}%",
            f"- **Intent Resolution & Completeness**: {summary.mean_intent_resolution}%",
            f"- **Tone & Empathy**: {summary.mean_tone_empathy}%",
            f"- **Actionability & Clarity**: {summary.mean_actionability}%",
            f"- **Semantic Similarity to Ground Truth**: {summary.mean_semantic_similarity}%",
            f"- **ROUGE-L F1**: {summary.mean_rougeL}",
            f"- **High Confidence Drafts (HEQI ≥ 85)**: {summary.high_performers_count} / {summary.total_tickets}",
            "",
            "## Category Performance Breakdown",
            "| Category | Count | Mean HEQI Score |",
            "| :--- | :---: | :---: |"
        ]

        for cat, data in summary.category_breakdown.items():
            lines.append(f"| `{cat}` | {data['count']} | **{data['mean_heqi']}** |")

        lines.extend([
            "",
            "## Customer Sentiment Breakdown",
            "| Sentiment | Count | Mean HEQI Score |",
            "| :--- | :---: | :---: |"
        ])

        for sent, data in summary.sentiment_breakdown.items():
            lines.append(f"| `{sent}` | {data['count']} | **{data['mean_heqi']}** |")

        lines.extend([
            "",
            "## Detailed Per-Ticket Evaluation Results",
            ""
        ])

        for r in results:
            lines.extend([
                f"### Ticket: `{r.ticket_id}` ({r.category})",
                f"- **Composite HEQI**: **{r.scores.composite_heqi}/100**",
                f"- **Sub-scores**: Policy: {r.scores.policy_adherence_score} | Intent: {r.scores.intent_resolution_score} | Tone: {r.scores.tone_empathy_score} | Actionability: {r.scores.actionability_score} | Semantic: {r.scores.semantic_similarity}%",
                f"- **ROUGE-L**: {r.scores.rougeL_f1} | **BLEU**: {r.scores.bleu_score}",
                f"- **Strengths**: {', '.join(r.strengths) if r.strengths else 'None noted'}",
                f"- **Improvements**: {', '.join(r.areas_for_improvement) if r.areas_for_improvement else 'None required'}",
                "",
                "<details>",
                "<summary>Click to view Generated Reply vs Ground Truth</summary>",
                "",
                "**Generated Reply:**",
                "```text",
                r.generated_reply,
                "```",
                "",
                "**Ground Truth Reference:**",
                "```text",
                r.ground_truth_reply,
                "```",
                "</details>",
                "",
                "---",
                ""
            ])

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
