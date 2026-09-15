"""
FastAPI Server for Hiver AI Email Assistant & Evaluation Suite.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
from typing import Optional, Dict, Any, List
import os
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from dataset.build_dataset import load_dataset
from dataset.schema import SupportTicket
from generator.engine import get_generator
from generator.knowledge_base import KnowledgeBase
from evaluation.evaluator import HiverEvaluator

app = FastAPI(
    title="Hiver AI Email Assistant API",
    description="End-to-end Gen-AI support email generation and multi-dimensional evaluation suite.",
    version="1.0.0"
)

# Enable CORS for local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cached resources
kb = KnowledgeBase()
tickets_list = load_dataset()
evaluator = HiverEvaluator()


class GenerateRequest(BaseModel):
    ticket_id: str
    provider: str = "auto"
    custom_instruction: Optional[str] = None


class EvaluateRequest(BaseModel):
    ticket_id: str
    reply: str


class BenchmarkRequest(BaseModel):
    provider: str = "auto"


@app.get("/api/tickets")
def get_tickets():
    """Returns all support tickets in the dataset."""
    return [
        {
            "ticket_id": t.ticket_id,
            "category": t.category,
            "priority": t.priority,
            "sentiment": t.sentiment,
            "subject": t.subject,
            "customer_name": t.thread[0].sender_name,
            "customer_email": t.thread[0].sender_email,
            "plan_tier": t.customer_context.plan_tier,
            "mrr": t.customer_context.mrr,
            "message_count": len(t.thread)
        }
        for t in tickets_list
    ]


@app.get("/api/tickets/{ticket_id}")
def get_ticket_detail(ticket_id: str):
    """Returns full details of a single ticket."""
    target = next((t for t in tickets_list if t.ticket_id == ticket_id), None)
    if not target:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    # Retrieve relevant KB docs for this ticket
    customer_msgs = [m for m in target.thread if m.sender == "customer"]
    query = f"{target.subject} {customer_msgs[-1].body if customer_msgs else ''}"
    relevant_kb = kb.retrieve(query, category=target.category, top_k=2)

    return {
        "ticket": target.model_dump(),
        "relevant_kb": relevant_kb
    }


@app.get("/api/kb")
def get_kb_documents():
    """Returns all knowledge base policy documents."""
    return kb.documents


@app.post("/api/generate")
def generate_reply(req: GenerateRequest):
    """Generates an email reply for a ticket."""
    target = next((t for t in tickets_list if t.ticket_id == req.ticket_id), None)
    if not target:
        raise HTTPException(status_code=404, detail="Ticket not found")

    gen = get_generator(provider=req.provider, kb=kb)
    reply = gen.generate(target, custom_instruction=req.custom_instruction)
    
    # Automatically evaluate the generated reply
    eval_result = evaluator.evaluate_ticket(target, generated_reply=reply)

    return {
        "ticket_id": req.ticket_id,
        "provider_used": req.provider,
        "reply": reply,
        "evaluation": eval_result.model_dump()
    }


@app.post("/api/evaluate")
def evaluate_reply(req: EvaluateRequest):
    """Evaluates an arbitrary or edited reply for a ticket."""
    target = next((t for t in tickets_list if t.ticket_id == req.ticket_id), None)
    if not target:
        raise HTTPException(status_code=404, detail="Ticket not found")

    eval_result = evaluator.evaluate_ticket(target, generated_reply=req.reply)
    return eval_result.model_dump()


@app.post("/api/benchmark")
def run_benchmark(req: BenchmarkRequest):
    """Runs batch benchmark across all tickets."""
    gen = get_generator(provider=req.provider, kb=kb)
    bench_evaluator = HiverEvaluator(generator=gen)
    results, summary = bench_evaluator.evaluate_all(tickets_list)
    return {
        "summary": summary.model_dump(),
        "results": [r.model_dump() for r in results]
    }


# Static files mount
static_dir = Path(__file__).resolve().parent / "static"
static_dir.mkdir(parents=True, exist_ok=True)
app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")
