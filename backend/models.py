# backend/models.py
from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime
import uuid

class Transaction(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    source: Literal["nessie", "manual"]
    status: Literal["pending_review", "reviewed"]
    merchant: Optional[str] = None
    amount: Optional[float] = None
    timestamp: datetime
    mood_rating: Optional[int] = None
    user_reason: Optional[str] = None
    unstructured_entry: Optional[str] = None
    analyzed_mood: Optional[str] = None

class ReviewPayload(BaseModel):
    mood_rating: int
    user_reason: str

class ManualEntryPayload(BaseModel):
    entry_text: str


class InterventionResponsePayload(BaseModel):
    user_choice: Literal["accept_delay", "reject_suggestion"]

class DashboardData(BaseModel):
    daily_summary_word: str
    daily_summary_sentence: str
    reviewed_transactions: List[Transaction]