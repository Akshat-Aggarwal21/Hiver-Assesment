"""
Dataset Builder & Exporter for Hiver AI Email Assistant.

Demonstrates:
1. Dataset ingestion & validation against Pydantic schema.
2. Conversion to CSV for easy inspection.
3. Synthetic scenario augmentation for testing edge cases.
4. Summary statistics calculation across categories, sentiment, and tiers.
"""

import json
import csv
import os
import sys
from pathlib import Path
from typing import List, Dict, Any

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from dataset.schema import SupportTicket, EmailMessage, CustomerContext, EvaluationRubric


DATA_DIR = PROJECT_ROOT / "data"
JSON_PATH = DATA_DIR / "support_tickets.json"
CSV_PATH = DATA_DIR / "support_tickets.csv"


def load_dataset(json_path: Path = JSON_PATH) -> List[SupportTicket]:
    """Loads and validates support tickets from JSON file."""
    if not json_path.exists():
        raise FileNotFoundError(f"Dataset file not found at: {json_path}")
    
    with open(json_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)
        
    tickets = [SupportTicket(**item) for item in raw_data]
    return tickets


def export_to_csv(tickets: List[SupportTicket], csv_path: Path = CSV_PATH) -> None:
    """Exports tickets to a flattened CSV format for data exploration."""
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    
    fieldnames = [
        "ticket_id",
        "category",
        "priority",
        "sentiment",
        "subject",
        "plan_tier",
        "mrr",
        "latest_customer_message",
        "ground_truth_reply",
        "required_facts",
        "expected_action_items",
        "tone_requirement"
    ]
    
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for t in tickets:
            customer_msgs = [m.body for m in t.thread if m.sender == "customer"]
            latest_msg = customer_msgs[-1] if customer_msgs else ""
            
            writer.writerow({
                "ticket_id": t.ticket_id,
                "category": t.category,
                "priority": t.priority,
                "sentiment": t.sentiment,
                "subject": t.subject,
                "plan_tier": t.customer_context.plan_tier,
                "mrr": t.customer_context.mrr,
                "latest_customer_message": latest_msg,
                "ground_truth_reply": t.ground_truth_reply,
                "required_facts": " | ".join(t.rubric.required_facts),
                "expected_action_items": " | ".join(t.rubric.expected_action_items),
                "tone_requirement": t.rubric.tone_requirement
            })


def get_dataset_statistics(tickets: List[SupportTicket]) -> Dict[str, Any]:
    """Computes distribution statistics across the dataset."""
    total = len(tickets)
    categories: Dict[str, int] = {}
    sentiments: Dict[str, int] = {}
    tiers: Dict[str, int] = {}
    
    for t in tickets:
        categories[t.category] = categories.get(t.category, 0) + 1
        sentiments[t.sentiment] = sentiments.get(t.sentiment, 0) + 1
        tier = t.customer_context.plan_tier
        tiers[tier] = tiers.get(tier, 0) + 1
        
    return {
        "total_tickets": total,
        "categories": categories,
        "sentiments": sentiments,
        "plan_tiers": tiers
    }


def main():
    print(f"Loading dataset from: {JSON_PATH}")
    tickets = load_dataset()
    print(f"Successfully loaded and validated {len(tickets)} tickets against Pydantic schema.")
    
    export_to_csv(tickets)
    print(f"Exported flattened dataset to: {CSV_PATH}")
    
    stats = get_dataset_statistics(tickets)
    print("\n=== Dataset Distribution Statistics ===")
    print(f"Total tickets: {stats['total_tickets']}")
    print("\nCategories:")
    for cat, count in stats["categories"].items():
        print(f"  - {cat:22s}: {count} ({count/stats['total_tickets']*100:.1f}%)")
        
    print("\nCustomer Sentiments:")
    for sent, count in stats["sentiments"].items():
        print(f"  - {sent:22s}: {count} ({count/stats['total_tickets']*100:.1f}%)")
        
    print("\nPlan Tiers:")
    for tier, count in stats["plan_tiers"].items():
        print(f"  - {tier:22s}: {count} ({count/stats['total_tickets']*100:.1f}%)")


if __name__ == "__main__":
    main()
