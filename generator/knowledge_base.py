"""
Knowledge Base & RAG Retrieval System for Hiver AI.

Provides relevant company policies, SLA agreements, security constraints,
and technical runbooks to ground AI replies in verified facts.
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional
import math
import re

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_KB_PATH = PROJECT_ROOT / "knowledge" / "kb_documents.json"


class KnowledgeBase:
    """In-memory knowledge retrieval engine with lexical & semantic relevance scoring."""
    
    def __init__(self, kb_path: Path = DEFAULT_KB_PATH):
        self.kb_path = kb_path
        self.documents: List[Dict[str, Any]] = []
        self._load_documents()

    def _load_documents(self) -> None:
        if not self.kb_path.exists():
            raise FileNotFoundError(f"Knowledge base document file not found at: {self.kb_path}")
        with open(self.kb_path, "r", encoding="utf-8") as f:
            self.documents = json.load(f)

    @staticmethod
    def _tokenize(text: str) -> List[str]:
        """Simple tokenizer that cleans and normalizes terms."""
        return re.findall(r"\b[a-zA-Z0-9_-]{2,}\b", text.lower())

    def retrieve(
        self,
        query: str,
        category: Optional[str] = None,
        top_k: int = 2
    ) -> List[Dict[str, Any]]:
        """
        Retrieves the top-k most relevant knowledge base documents for a given query.
        Uses BM25-inspired term frequency with category boosting and keyword matching.
        """
        query_tokens = set(self._tokenize(query))
        if not query_tokens:
            return self.documents[:top_k]

        scored_docs = []
        for doc in self.documents:
            score = 0.0
            
            # Boost if category matches
            if category and doc.get("category") == category:
                score += 3.0

            doc_text = f"{doc.get('title', '')} {doc.get('content', '')}".lower()
            doc_tokens = self._tokenize(doc_text)
            doc_token_counts = {}
            for t in doc_tokens:
                doc_token_counts[t] = doc_token_counts.get(t, 0) + 1

            # Keyword match boost
            keywords = [k.lower() for k in doc.get("keywords", [])]
            for kw in keywords:
                if kw in query.lower():
                    score += 4.0

            # Lexical overlap with TF weighting
            for q_tok in query_tokens:
                if q_tok in doc_token_counts:
                    tf = doc_token_counts[q_tok]
                    score += 1.0 + math.log(1.0 + tf)

            scored_docs.append((score, doc))

        # Sort descending by score
        scored_docs.sort(key=lambda x: x[0], reverse=True)
        return [doc for score, doc in scored_docs[:top_k]]

    def get_context_for_prompt(
        self,
        query: str,
        category: Optional[str] = None,
        top_k: int = 2
    ) -> str:
        """Formats retrieved articles into a clean string for system prompt injection."""
        docs = self.retrieve(query, category=category, top_k=top_k)
        if not docs:
            return "No specific internal policy articles found."

        context_blocks = []
        for idx, doc in enumerate(docs, 1):
            context_blocks.append(
                f"[Policy Doc {idx}: {doc['title']} (ID: {doc['id']})]\n{doc['content']}"
            )
        return "\n\n".join(context_blocks)


class PastTicketRetriever:
    """
    Retrieves similar historical customer emails and human responses from the dataset.
    Implements few-shot in-context learning by retrieving relevant past email pairs.
    """

    def __init__(self, tickets_path: Optional[Path] = None):
        self.tickets_path = tickets_path or (PROJECT_ROOT / "data" / "support_tickets.json")
        self.past_tickets = []
        self._load_tickets()

    def _load_tickets(self) -> None:
        if self.tickets_path.exists():
            with open(self.tickets_path, "r", encoding="utf-8") as f:
                self.past_tickets = json.load(f)

    @staticmethod
    def _tokenize(text: str) -> List[str]:
        return re.findall(r"\b[a-zA-Z0-9_-]{2,}\b", text.lower())

    def retrieve_similar(
        self,
        query: str,
        category: Optional[str] = None,
        exclude_ticket_id: Optional[str] = None,
        top_k: int = 1
    ) -> List[Dict[str, Any]]:
        """
        Finds the most relevant historical tickets (excluding the current one) to use as few-shot examples.
        """
        query_tokens = set(self._tokenize(query))
        candidates = [t for t in self.past_tickets if t.get("ticket_id") != exclude_ticket_id]

        if not candidates:
            return []

        scored = []
        for t in candidates:
            score = 0.0
            if category and t.get("category") == category:
                score += 4.0

            text = f"{t.get('subject', '')} " + " ".join(m.get("body", "") for m in t.get("thread", []))
            t_tokens = set(self._tokenize(text))
            overlap = len(query_tokens.intersection(t_tokens))
            score += overlap

            scored.append((score, t))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [t for score, t in scored[:top_k]]

    def get_few_shot_prompt_block(
        self,
        query: str,
        category: Optional[str] = None,
        exclude_ticket_id: Optional[str] = None
    ) -> str:
        """Formats the retrieved historical email pair into a few-shot guidance block."""
        matches = self.retrieve_similar(query, category=category, exclude_ticket_id=exclude_ticket_id, top_k=1)
        if not matches:
            return ""

        t = matches[0]
        customer_msgs = [m.get("body", "") for m in t.get("thread", []) if m.get("sender") == "customer"]
        cust_body = customer_msgs[-1] if customer_msgs else ""
        return (
            f"### RELEVANT PAST EMAIL & HUMAN RESPONSE (FEW-SHOT RETRIEVAL FROM DATASET):\n"
            f"- Category: {t.get('category')} | Sentiment: {t.get('sentiment')}\n"
            f"- Customer Subject: {t.get('subject')}\n"
            f"- Customer Message: {cust_body[:200]}...\n"
            f"- Senior Agent Response Sent:\n{t.get('ground_truth_reply')}\n"
        )

