from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class EmailMessage(BaseModel):
    """Represents a single message within an email thread."""
    sender: str = Field(description="'customer' or 'agent'")
    sender_name: str = Field(description="Name of the sender")
    sender_email: str = Field(description="Email address of sender")
    timestamp: str = Field(description="ISO timestamp or relative time string")
    subject: Optional[str] = None
    body: str = Field(description="Email body text")


class CustomerContext(BaseModel):
    """Contextual metadata attached to the customer or ticket."""
    account_id: str
    plan_tier: str = Field(description="Free, Starter, Pro, Enterprise")
    mrr: float = Field(default=0.0, description="Monthly recurring revenue")
    account_status: str = Field(default="active", description="active, past_due, trial, cancelled")
    joined_date: str = "2023-01-15"
    metadata: Dict[str, Any] = Field(default_factory=dict)


class EvaluationRubric(BaseModel):
    """Expected criteria for evaluating replies to this ticket."""
    required_facts: List[str] = Field(default_factory=list, description="Specific policies or facts the reply must mention")
    prohibited_claims: List[str] = Field(default_factory=list, description="False claims or unauthorized promises to avoid")
    expected_action_items: List[str] = Field(default_factory=list, description="Next steps the agent should provide")
    tone_requirement: str = Field(default="empathetic_and_clear", description="Required tone demeanor")
    min_resolution_points: List[str] = Field(default_factory=list, description="Customer points that must be addressed")


class SupportTicket(BaseModel):
    """A customer support ticket representing a shared inbox thread."""
    ticket_id: str
    category: str = Field(description="billing, technical_issue, account_access, cancellation_refund, feature_request, sla_escalation, onboarding")
    priority: str = Field(default="normal", description="low, normal, high, urgent")
    sentiment: str = Field(default="neutral", description="frustrated, angry, urgent, neutral, confused, satisfied")
    subject: str
    customer_context: CustomerContext
    thread: List[EmailMessage]
    ground_truth_reply: str = Field(description="Golden reference reply written by senior support")
    rubric: EvaluationRubric


class EvaluationScores(BaseModel):
    """Multi-dimensional score card for an email reply."""
    policy_adherence_score: float = Field(ge=0.0, le=100.0, description="Adherence to company policies and boundary limits")
    intent_resolution_score: float = Field(ge=0.0, le=100.0, description="Completeness in resolving customer queries")
    tone_empathy_score: float = Field(ge=0.0, le=100.0, description="Empathy, professional warmth, and de-escalation quality")
    actionability_score: float = Field(ge=0.0, le=100.0, description="Clarity of next steps, timelines, and diagnostic instructions")
    hallucination_penalty: float = Field(ge=0.0, le=100.0, default=0.0, description="Deductions for fabricated facts or false commitments")
    semantic_similarity: float = Field(ge=0.0, le=100.0, description="Semantic similarity to ground truth")
    rouge1_f1: float = Field(ge=0.0, le=1.0, default=0.0)
    rouge2_f1: float = Field(ge=0.0, le=1.0, default=0.0)
    rougeL_f1: float = Field(ge=0.0, le=1.0, default=0.0)
    bleu_score: float = Field(ge=0.0, le=100.0, default=0.0)
    composite_heqi: float = Field(ge=0.0, le=100.0, description="Hiver Email Quality Index (HEQI composite 0-100)")


class TicketEvaluationResult(BaseModel):
    """Full evaluation breakdown for a single ticket reply."""
    ticket_id: str
    category: str
    generated_reply: str
    ground_truth_reply: str
    scores: EvaluationScores
    strengths: List[str] = Field(default_factory=list)
    areas_for_improvement: List[str] = Field(default_factory=list)
    policy_violations_detected: List[str] = Field(default_factory=list)
    unaddressed_customer_points: List[str] = Field(default_factory=list)
    reasoning: Optional[str] = None


class BenchmarkSummary(BaseModel):
    """Aggregated benchmark metrics across multiple tickets."""
    total_tickets: int
    mean_heqi: float
    mean_policy_adherence: float
    mean_intent_resolution: float
    mean_tone_empathy: float
    mean_actionability: float
    mean_semantic_similarity: float
    mean_rougeL: float
    category_breakdown: Dict[str, Dict[str, float]]
    sentiment_breakdown: Dict[str, Dict[str, float]]
    high_performers_count: int
    low_performers_count: int
