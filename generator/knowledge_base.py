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
