"""
Command-Line Interface for Hiver AI Email Assistant & Evaluation Suite.

Usage:
    python -m hiver_ai.cli evaluate [--ticket-id TICK-101] [--output-json reports/eval.json]
    python -m hiver_ai.cli generate --ticket-id TICK-101
    python -m hiver_ai.cli dataset-stats
    python -m hiver_ai.cli inspect-ticket --ticket-id TICK-101
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from dataset.build_dataset import load_dataset, get_dataset_statistics
from generator.engine import get_generator
from evaluation.evaluator import HiverEvaluator


def command_evaluate(args):
    """Runs evaluation benchmark across dataset or a single ticket."""
    dataset_path = Path(args.dataset) if args.dataset else PROJECT_ROOT / "data" / "support_tickets.json"
    print(f"\n========================================================")
    print(f"   HIVER AI EMAIL QUALITY BENCHMARK (HEQI EVALUATION)   ")
    print(f"========================================================")
    print(f"Loading dataset: {dataset_path}")
    
    tickets = load_dataset(dataset_path)
    generator = get_generator(provider=args.provider)
    evaluator = HiverEvaluator(generator=generator)
    
    if args.ticket_id:
        target = next((t for t in tickets if t.ticket_id == args.ticket_id), None)
        if not target:
            print(f"[Error] Ticket with ID '{args.ticket_id}' not found.")
            sys.exit(1)
            
        print(f"\nEvaluating single ticket: {target.ticket_id} ({target.category})")
        res = evaluator.evaluate_ticket(target)
        
        print("\n--- GENERATED AI REPLY ---")
        print(res.generated_reply)
        print("\n--- GROUND TRUTH REFERENCE ---")
        print(res.ground_truth_reply)
        
        s = res.scores
        print("\n--- SCORECARD ---")
        print(f"Composite HEQI Score:    {s.composite_heqi} / 100")
        print(f"Policy Adherence:        {s.policy_adherence_score}%")
        print(f"Intent Resolution:       {s.intent_resolution_score}%")
        print(f"Tone & Empathy:          {s.tone_empathy_score}%")
        print(f"Actionability & Clarity: {s.actionability_score}%")
        print(f"Semantic Similarity:     {s.semantic_similarity}%")
        print(f"ROUGE-L F1:              {s.rougeL_f1}")
        print(f"BLEU Score:              {s.bleu_score}")
        
        print("\nStrengths:")
        for st in res.strengths:
            print(f"  + {st}")
        print("\nAreas for Improvement:")
        for imp in res.areas_for_improvement:
            print(f"  - {imp}")
            
    else:
        print(f"Evaluating all {len(tickets)} tickets using '{args.provider}' generator...\n")
        results, summary = evaluator.evaluate_all(tickets)
        
        # Print summary table
        print(f"{'Metric':<32} | {'Score':<10}")
        print("-" * 46)
        print(f"{'Overall Mean HEQI':<32} | {summary.mean_heqi} / 100")
        print(f"{'Mean Policy Adherence':<32} | {summary.mean_policy_adherence}%")
        print(f"{'Mean Intent Resolution':<32} | {summary.mean_intent_resolution}%")
        print(f"{'Mean Tone & Empathy':<32} | {summary.mean_tone_empathy}%")
        print(f"{'Mean Actionability':<32} | {summary.mean_actionability}%")
        print(f"{'Mean Semantic Similarity':<32} | {summary.mean_semantic_similarity}%")
        print(f"{'Mean ROUGE-L F1':<32} | {summary.mean_rougeL}")
        print(f"{'High Performers (HEQI >= 85)':<32} | {summary.high_performers_count} / {summary.total_tickets}")
        print(f"{'Low Performers  (HEQI < 70)':<32}  | {summary.low_performers_count} / {summary.total_tickets}")
        
        print("\n--- Category Breakdown ---")
        for cat, data in summary.category_breakdown.items():
            print(f"  - {cat:<24} : {data['mean_heqi']} (n={data['count']})")

        print("\n--- Sentiment Breakdown ---")
        for sent, data in summary.sentiment_breakdown.items():
            print(f"  - {sent:<24} : {data['mean_heqi']} (n={data['count']})")
            
        # Export files
        if args.output_json:
            out_json = Path(args.output_json)
            evaluator.export_report_json(results, summary, out_json)
            print(f"\n[Saved] Detailed JSON report: {out_json}")
            
        if args.output_md:
            out_md = Path(args.output_md)
            evaluator.export_report_markdown(results, summary, out_md)
            print(f"[Saved] Human-readable Markdown report: {out_md}")


def command_generate(args):
    """Generates an email reply for a specified ticket."""
    tickets = load_dataset()
    target = next((t for t in tickets if t.ticket_id == args.ticket_id), None)
    if not target:
        print(f"[Error] Ticket with ID '{args.ticket_id}' not found.")
        sys.exit(1)
        
    generator = get_generator(provider=args.provider)
    reply = generator.generate(target, custom_instruction=args.instruction)
    
    print(f"\n========================================================")
    print(f"Generated AI Reply for {target.ticket_id}: {target.subject}")
    print(f"Customer: {target.thread[0].sender_name} | Sentiment: {target.sentiment} | Plan: {target.customer_context.plan_tier}")
    print(f"========================================================\n")
    print(reply)
    print("\n" + "=" * 56)


def command_dataset_stats(args):
    """Displays dataset breakdown and statistics."""
    tickets = load_dataset()
    stats = get_dataset_statistics(tickets)
    print("\n=== HIVER SUPPORT TICKET DATASET OVERVIEW ===")
    print(f"Total Tickets: {stats['total_tickets']}\n")
    print("Ticket Categories:")
    for cat, count in stats['categories'].items():
        bar = "#" * int(count * 2)
        print(f"  {cat:<24} | {count:>2} ({count/stats['total_tickets']*100:>4.1f}%) {bar}")
        
    print("\nCustomer Sentiments:")
    for sent, count in stats['sentiments'].items():
        bar = "#" * int(count * 2)
        print(f"  {sent:<24} | {count:>2} ({count/stats['total_tickets']*100:>4.1f}%) {bar}")

    print("\nCustomer Plan Tiers:")
    for tier, count in stats['plan_tiers'].items():
        bar = "#" * int(count * 2)
        print(f"  {tier:<24} | {count:>2} ({count/stats['total_tickets']*100:>4.1f}%) {bar}")


def command_inspect_ticket(args):
    """Inspects a ticket's full thread, context, and ground truth."""
    tickets = load_dataset()
    target = next((t for t in tickets if t.ticket_id == args.ticket_id), None)
    if not target:
        print(f"[Error] Ticket with ID '{args.ticket_id}' not found.")
        sys.exit(1)
        
    print(f"\n=== TICKET: {target.ticket_id} ===")
    print(f"Subject:   {target.subject}")
    print(f"Category:  {target.category}")
    print(f"Priority:  {target.priority}")
    print(f"Sentiment: {target.sentiment}")
    print(f"Plan Tier: {target.customer_context.plan_tier} (MRR: ${target.customer_context.mrr})")
    print("\n--- THREAD HISTORY ---")
    for idx, msg in enumerate(target.thread, 1):
        print(f"[{idx}] {msg.sender.upper()} ({msg.sender_name}) - {msg.timestamp}:")
        print(f"    {msg.body}\n")
    print("--- GROUND TRUTH HUMAN REPLY ---")
    print(target.ground_truth_reply)
    print("\n--- EVALUATION RUBRIC ---")
    print("Required facts:")
    for rf in target.rubric.required_facts:
        print(f"  * {rf}")
    print("Expected action items:")
    for act in target.rubric.expected_action_items:
        print(f"  * {act}")


def main():
    parser = argparse.ArgumentParser(
        description="Hiver AI Email Assistant CLI - Generation & Evaluation Suite",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Evaluate command
    eval_parser = subparsers.add_parser("evaluate", help="Run benchmark evaluation")
    eval_parser.add_argument("--dataset", type=str, help="Path to custom JSON dataset")
    eval_parser.add_argument("--ticket-id", type=str, help="Evaluate a single ticket ID")
    eval_parser.add_argument("--provider", type=str, default="auto", choices=["auto", "mock", "openai", "gemini"])
    eval_parser.add_argument("--output-json", type=str, default="reports/evaluation_report.json")
    eval_parser.add_argument("--output-md", type=str, default="reports/evaluation_report.md")

    # Generate command
    gen_parser = subparsers.add_parser("generate", help="Generate reply for a ticket")
    gen_parser.add_argument("--ticket-id", type=str, required=True, help="Ticket ID to reply to")
    gen_parser.add_argument("--provider", type=str, default="auto", choices=["auto", "mock", "openai", "gemini"])
    gen_parser.add_argument("--instruction", type=str, help="Custom prompt instruction")

    # Dataset stats
    subparsers.add_parser("dataset-stats", help="Display dataset distribution statistics")

    # Inspect ticket
    inspect_parser = subparsers.add_parser("inspect-ticket", help="Inspect thread and ground truth")
    inspect_parser.add_argument("--ticket-id", type=str, required=True, help="Ticket ID to inspect")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(0)

    if args.command == "evaluate":
        command_evaluate(args)
    elif args.command == "generate":
        command_generate(args)
    elif args.command == "dataset-stats":
        command_dataset_stats(args)
    elif args.command == "inspect-ticket":
        command_inspect_ticket(args)


if __name__ == "__main__":
    main()
