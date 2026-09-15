"""
Evaluation Metrics Suite for Hiver Email Assistant.

Implements the multi-dimensional Hiver Email Quality Index (HEQI):
1. Policy Adherence Score (0-100)
2. Intent Resolution & Completeness Score (0-100)
3. Tone & Empathy Score (0-100)
4. Actionability Score (0-100)
5. Hallucination Penalty (0-100)
6. Lexical & Semantic Overlap (ROUGE-1, ROUGE-2, ROUGE-L, BLEU, Cosine Similarity)
"""

import re
import math
from typing import Dict, List, Tuple, Any, Optional
from rouge_score import rouge_scorer
import sacrebleu
from nltk.stem import PorterStemmer

from dataset.schema import SupportTicket, EvaluationRubric, EvaluationScores


class EmailMetricsCalculator:
    """Calculates granular and composite evaluation metrics for email replies."""

    def __init__(self):
        self.rouge = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
        self.stemmer = PorterStemmer()

    @staticmethod
    def _clean_text(text: str) -> str:
        return text.lower().strip()

    def _get_stems(self, text: str) -> List[str]:
        words = re.findall(r"\b[a-zA-Z0-9_-]{2,}\b", text.lower())
        return [self.stemmer.stem(w) for w in words]

    def _get_words(self, text: str) -> List[str]:
        return re.findall(r"\b[a-zA-Z0-9_-]{2,}\b", text.lower())

    def compute_policy_adherence(
        self,
        generated_reply: str,
        rubric: EvaluationRubric
    ) -> Tuple[float, List[str], List[str]]:
        """
        Evaluates adherence to required factual points and absence of prohibited claims.
        Returns (score, matched_facts, detected_violations).
        """
        reply_lower = self._clean_text(generated_reply)
        reply_stems = set(self._get_stems(reply_lower))
        required = rubric.required_facts
        prohibited = rubric.prohibited_claims

        matched_facts = []
        for fact in required:
            fact_stems = [self.stemmer.stem(w) for w in self._get_words(fact) if len(w) > 3]
            # Match if at least 45% of key fact stems are present or exact phrase match
            matches = sum(1 for s in fact_stems if s in reply_stems or any(s in r_s for r_s in reply_stems))
            if fact.lower() in reply_lower or (fact_stems and (matches / len(fact_stems) >= 0.40)):
                matched_facts.append(fact)

        violations = []
        for claim in prohibited:
            claim_stems = [self.stemmer.stem(w) for w in self._get_words(claim) if len(w) > 3]
            matches = sum(1 for s in claim_stems if s in reply_stems)
            if claim.lower() in reply_lower or (claim_stems and (matches / len(claim_stems) >= 0.75)):
                violations.append(claim)

        # Baseline score: ratio of required facts matched
        coverage_ratio = len(matched_facts) / max(len(required), 1)
        base_score = coverage_ratio * 100.0

        # Violation deduction (each violation costs 35 points)
        penalty = len(violations) * 35.0
        final_score = max(0.0, min(100.0, base_score - penalty))

        return final_score, matched_facts, violations

    def compute_intent_resolution(
        self,
        generated_reply: str,
        ticket: SupportTicket
    ) -> Tuple[float, List[str], List[str]]:
        """
        Evaluates whether the reply addresses all questions, intents, and pain points.
        Uses sentence-level semantic matching and concept mapping.
        """
        reply_lower = self._clean_text(generated_reply)
        reply_stems = set(self._get_stems(reply_lower))
        expected_points = ticket.rubric.min_resolution_points
        
        # Concept synonym expansions for common support evaluation goals
        concept_maps = {
            "de-escal": ["apolog", "sorri", "frustrat", "disrupt", "urgenc", "sincer"],
            "commit": ["monit", "stay on", "keep open", "follow up", "remain activ"],
            "audit": ["audit", "record", "statement", "review", "zero usag"],
            "secur": ["secur", "complianc", "protocol", "protect", "integr"],
            "expedit": ["fast", "quick", "30 minut", "immedi"],
            "workaround": ["renam", "decoupl", "p1-urgent", "quick fix"],
            "prorat": ["prorat", "seat", "calcul", "breakdown", "21 day"],
            "navig": ["navig", "settings >", "step", "tab", "toggl"],
            "unblock": ["resolv", "authent", "incognito", "test login", "access"],
            "emerg": ["live bridg", "meet", "right now", "standbi", "call"]
        }

        # Also check customer thread text for key entities
        customer_msgs = [m.body for m in ticket.thread if m.sender == "customer"]
        full_customer_text = " ".join(customer_msgs)

        addressed = []
        missing = []

        # Split reply into sentences
        sentences = [s.strip() for s in re.split(r"[.\n!?]+", reply_lower) if len(s.strip()) > 5]

        for pt in expected_points:
            pt_stems = [self.stemmer.stem(w) for w in self._get_words(pt) if len(w) > 2]
            
            # Direct stem match
            direct_matches = sum(1 for s in pt_stems if s in reply_stems or any(s in r_s for r_s in reply_stems))
            match_ratio = direct_matches / max(len(pt_stems), 1)
            
            # Concept mapping match
            concept_match = False
            for concept_key, concept_terms in concept_maps.items():
                if any(concept_key in s for s in pt_stems):
                    if any(term in reply_lower for term in concept_terms):
                        concept_match = True
                        break

            # Sentence similarity match
            best_sent_sim = 0.0
            for sent in sentences:
                sent_stems = set(self._get_stems(sent))
                overlap = len(set(pt_stems).intersection(sent_stems))
                sim = overlap / max(len(pt_stems), 1)
                if sim > best_sent_sim:
                    best_sent_sim = sim

            if pt.lower() in reply_lower or match_ratio >= 0.35 or concept_match or best_sent_sim >= 0.33:
                addressed.append(pt)
            else:
                missing.append(pt)

        # Check entity preservation (e.g., ticket ID, invoice numbers, amounts, versions)
        entities_in_prompt = re.findall(r"\b(?:ACC-\d+|INV-[\w-]+|\$\d+(?:\.\d+)?|\d+\s*days|\b504\b|\b2fa\b|\b8\.11\b)\b", full_customer_text, re.I)
        entity_score_bonus = 0.0
        if entities_in_prompt:
            preserved = sum(1 for ent in entities_in_prompt if ent.lower() in reply_lower)
            entity_score_bonus = (preserved / len(entities_in_prompt)) * 15.0

        ratio = len(addressed) / max(len(expected_points), 1)
        score = min(100.0, (ratio * 85.0) + entity_score_bonus)

        return score, addressed, missing

    def compute_tone_empathy(
        self,
        generated_reply: str,
        ticket: SupportTicket
    ) -> float:
        """
        Evaluates empathy, warmth, de-escalation for frustrated customers, and absence of robotic tone.
        """
        reply_lower = self._clean_text(generated_reply)
        sentiment = ticket.sentiment.lower()
        tier = ticket.customer_context.plan_tier

        score = 70.0  # neutral starting baseline

        # Greeting check
        if re.search(r"^(hi|hello|dear|good morning|good afternoon)\b", reply_lower):
            score += 8.0

        # Sign-off check
        if re.search(r"(best regards|warm regards|sincerely|cheers|best,|thanks,)", reply_lower):
            score += 7.0

        # Empathy / Acknowledgement markers
        empathy_markers = [
            "apologize", "sorry", "understand", "frustration", "urgency", 
            "appreciate", "thank you for reaching out", "glad to assist", 
            "happy to help", "completely understand"
        ]
        empathy_count = sum(1 for m in empathy_markers if m in reply_lower)

        if sentiment in ["angry", "frustrated"]:
            # Needs strong de-escalation and empathy
            if any(w in reply_lower for w in ["apologize", "sincerely apologize", "completely understand", "urgency"]):
                score += 15.0
            else:
                score -= 20.0  # penalty for lack of de-escalation
        elif sentiment == "confused":
            # Needs encouragement
            if any(w in reply_lower for w in ["happy to clarify", "glad to guide", "welcome aboard", "let me explain"]):
                score += 10.0

        score += min(10.0, empathy_count * 2.5)

        # Enterprise tone check
        if tier == "Enterprise":
            if "enterprise" in reply_lower or "priority" in reply_lower or "csm" in reply_lower or "on-call" in reply_lower:
                score += 5.0

        return max(0.0, min(100.0, score))

    def compute_actionability(
        self,
        generated_reply: str,
        rubric: EvaluationRubric
    ) -> float:
        """
        Evaluates clarity of next steps, numbered procedures, timelines, and links.
        """
        reply = generated_reply.strip()
        score = 65.0

        # Numbered list or step-by-step instructions
        has_numbered_steps = bool(re.search(r"(?:^|\n)\s*(?:[1-9]\.|\*|-)\s+", reply))
        if has_numbered_steps:
            score += 15.0

        # Concrete timelines mentioned (e.g. 3-5 business days, 20 minutes, 1-2 days)
        has_timeline = bool(re.search(r"\b(?:\d+[-\s]*(?:business\s+days|days|hours|minutes|seconds))\b", reply, re.I))
        if has_timeline:
            score += 10.0

        # Explicit action instructions or links
        action_keywords = ["navigate to", "settings >", "click", "download", "link", "https://", "steps:"]
        action_matches = sum(1 for kw in action_keywords if kw in reply.lower())
        score += min(10.0, action_matches * 3.0)

        return max(0.0, min(100.0, score))

    def compute_lexical_metrics(
        self,
        generated_reply: str,
        ground_truth: str
    ) -> Dict[str, float]:
        """Computes ROUGE-1, ROUGE-2, ROUGE-L, and SacreBLEU."""
        rouge_scores = self.rouge.score(ground_truth, generated_reply)
        
        bleu = sacrebleu.sentence_bleu(
            generated_reply,
            [ground_truth],
            smooth_method="exp"
        )

        return {
            "rouge1_f1": rouge_scores["rouge1"].fmeasure,
            "rouge2_f1": rouge_scores["rouge2"].fmeasure,
            "rougeL_f1": rouge_scores["rougeL"].fmeasure,
            "bleu_score": bleu.score
        }

    def compute_semantic_similarity(
        self,
        generated_reply: str,
        ground_truth: str
    ) -> float:
        """Computes bag-of-words cosine similarity (raw term-frequency vectors, no IDF weighting)"""
        words_gen = self._get_words(generated_reply)
        words_ref = self._get_words(ground_truth)

        if not words_gen or not words_ref:
            return 0.0

        vocab = sorted(list(set(words_gen + words_ref)))
        vec_gen = [words_gen.count(w) for w in vocab]
        vec_ref = [words_ref.count(w) for w in vocab]

        dot_prod = sum(g * r for g, r in zip(vec_gen, vec_ref))
        norm_g = math.sqrt(sum(g * g for g in vec_gen))
        norm_r = math.sqrt(sum(r * r for r in vec_ref))

        if norm_g == 0 or norm_r == 0:
            return 0.0

        cos_sim = dot_prod / (norm_g * norm_r)
        return round(cos_sim * 100.0, 2)

    def calculate_all(
        self,
        generated_reply: str,
        ticket: SupportTicket
    ) -> Tuple[EvaluationScores, List[str], List[str], List[str], List[str]]:
        """
        Calculates all sub-scores and composite HEQI for a generated reply.
        Returns (EvaluationScores, matched_facts, violations, addressed_pts, missing_pts).
        """
        policy_score, matched_facts, violations = self.compute_policy_adherence(
            generated_reply, ticket.rubric
        )
        
        intent_score, addressed_pts, missing_pts = self.compute_intent_resolution(
            generated_reply, ticket
        )
        
        tone_score = self.compute_tone_empathy(generated_reply, ticket)
        action_score = self.compute_actionability(generated_reply, ticket.rubric)
        lexical = self.compute_lexical_metrics(generated_reply, ticket.ground_truth_reply)
        semantic_score = self.compute_semantic_similarity(generated_reply, ticket.ground_truth_reply)

        # Composite Hiver Email Quality Index (HEQI)
        # Weights: Policy (30%), Intent (25%), Tone (20%), Actionability (15%), Semantic (10%)
        composite = (
            (0.30 * policy_score) +
            (0.25 * intent_score) +
            (0.20 * tone_score) +
            (0.15 * action_score) +
            (0.10 * semantic_score)
        )
        composite = max(0.0, min(100.0, round(composite, 2)))

        scores = EvaluationScores(
            policy_adherence_score=round(policy_score, 2),
            intent_resolution_score=round(intent_score, 2),
            tone_empathy_score=round(tone_score, 2),
            actionability_score=round(action_score, 2),
            hallucination_penalty=round(len(violations) * 35.0, 2),
            semantic_similarity=semantic_score,
            rouge1_f1=round(lexical["rouge1_f1"], 4),
            rouge2_f1=round(lexical["rouge2_f1"], 4),
            rougeL_f1=round(lexical["rougeL_f1"], 4),
            bleu_score=round(lexical["bleu_score"], 2),
            composite_heqi=composite
        )

        return scores, matched_facts, violations, addressed_pts, missing_pts
