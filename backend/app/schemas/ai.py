"""AI suggestion request and response schemas."""

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

# ---------- shared constants (exact values stored in the database) ----------

# Categories the AI is allowed to suggest (README section 5.2).
# Ticket category itself is free text; this list only limits the AI's suggestion.
AI_CATEGORIES: tuple[str, ...] = (
    "Hardware",
    "Software",
    "Network",
    "Access and Permissions",
    "Email",
    "Other",
)
CATEGORY_OTHER = "Other"

# Ticket priority values used by the whole team (README section 5.2).
TICKET_PRIORITIES: tuple[str, ...] = ("Low", "Medium", "High", "Critical")
TicketPriority = Literal["Low", "Medium", "High", "Critical"]

# ai_suggestions.status values.
SUGGESTION_PENDING = "Pending"
SUGGESTION_ACCEPTED = "Accepted"
SUGGESTION_REJECTED = "Rejected"
SUGGESTION_MODIFIED = "Modified"

# ticket_activities.activity_type values written by the AI decision workflow.
ACTIVITY_AI_APPLIED = "ai_recommendation_applied"
ACTIVITY_AI_REJECTED = "ai_recommendation_rejected"

# Common shorthand the model may use, mapped to the official category name.
_CATEGORY_ALIASES = {
    "access": "Access and Permissions",
    "access & permissions": "Access and Permissions",
    "permissions": "Access and Permissions",
}

# Length limits that keep AI text reasonable before it is saved.
_MAX_SUMMARY = 1000
_MAX_EXPLANATION = 1000
_MAX_RESPONSE = 2000
_MAX_STEP = 300
_MAX_STEPS = 10


def _clean_text(value: Any, limit: int) -> str:
    if not isinstance(value, str):
        raise ValueError("must be text")
    text = value.strip()
    if not text:
        raise ValueError("must not be empty")
    return text[:limit]


# ---------- AI model output (validated before anything is saved) ----------

class AIAnalysisResult(BaseModel):
    """The structured answer expected from the local AI model."""

    suggested_category: str
    suggested_priority: TicketPriority
    summary: str
    explanation: str
    suggested_response: str
    troubleshooting_steps: list[str]
    confidence: float | None = None

    @field_validator("suggested_category", mode="before")
    @classmethod
    def normalize_category(cls, value: Any) -> str:
        """Match the category case-insensitively; anything unknown becomes 'Other'."""
        if not isinstance(value, str):
            return CATEGORY_OTHER
        text = value.strip().lower()
        for category in AI_CATEGORIES:
            if text == category.lower():
                return category
        return _CATEGORY_ALIASES.get(text, CATEGORY_OTHER)

    @field_validator("suggested_priority", mode="before")
    @classmethod
    def normalize_priority(cls, value: Any) -> Any:
        """Accept 'high' or ' HIGH ' as 'High'; unknown values fail validation."""
        if isinstance(value, str):
            text = value.strip().lower()
            for priority in TICKET_PRIORITIES:
                if text == priority.lower():
                    return priority
        return value

    @field_validator("summary", mode="before")
    @classmethod
    def clean_summary(cls, value: Any) -> str:
        return _clean_text(value, _MAX_SUMMARY)

    @field_validator("explanation", mode="before")
    @classmethod
    def clean_explanation(cls, value: Any) -> str:
        return _clean_text(value, _MAX_EXPLANATION)

    @field_validator("suggested_response", mode="before")
    @classmethod
    def clean_response(cls, value: Any) -> str:
        return _clean_text(value, _MAX_RESPONSE)

    @field_validator("troubleshooting_steps", mode="before")
    @classmethod
    def clean_steps(cls, value: Any) -> list[str]:
        if not isinstance(value, list):
            raise ValueError("must be a list of steps")
        steps = [item.strip()[:_MAX_STEP] for item in value if isinstance(item, str) and item.strip()]
        if not steps:
            raise ValueError("must contain at least one step")
        return steps[:_MAX_STEPS]

    @field_validator("confidence", mode="before")
    @classmethod
    def clean_confidence(cls, value: Any) -> float | None:
        """Keep a 0-1 number; anything else is stored as 'unknown' (null)."""
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            return None
        return float(value) if 0 <= value <= 1 else None


# ---------- API responses ----------

class AISuggestionResponse(BaseModel):
    """One saved AI suggestion (a row of ai_suggestions)."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    ticket_id: int
    suggested_category: str | None
    suggested_priority: str | None
    summary: str | None
    explanation: str | None
    suggested_response: str | None
    troubleshooting_steps: list[Any] | dict[str, Any] | None
    confidence: float | None
    model_name: str | None
    status: str | None
    created_at: datetime | None


class AIDecisionRequest(BaseModel):
    """Support staff decision on a Pending suggestion.

    - Accepted: copy the AI's category and/or priority onto the ticket.
    - Modified: apply the staff member's own final_category and/or final_priority.
    - Rejected: change nothing on the ticket.
    """

    decision: Literal["Accepted", "Rejected", "Modified"]
    apply_category: bool = Field(default=True, description="Accepted only: copy the AI category")
    apply_priority: bool = Field(default=True, description="Accepted only: copy the AI priority")
    final_category: str | None = Field(default=None, max_length=100, description="Modified only (free text)")
    final_priority: TicketPriority | None = Field(default=None, description="Modified only")
    note: str | None = Field(default=None, max_length=1000)

    @field_validator("final_category", "note", mode="before")
    @classmethod
    def blank_to_none(cls, value: Any) -> Any:
        if isinstance(value, str):
            value = value.strip()
            return value or None
        return value

    @model_validator(mode="after")
    def check_decision_fields(self) -> "AIDecisionRequest":
        has_final = self.final_category is not None or self.final_priority is not None
        if self.decision == "Modified" and not has_final:
            raise ValueError("Modified needs final_category and/or final_priority")
        if self.decision != "Modified" and has_final:
            raise ValueError("final_category/final_priority are only used with Modified")
        if self.decision == "Accepted" and not (self.apply_category or self.apply_priority):
            raise ValueError("Accepted needs apply_category and/or apply_priority set to true")
        return self


class AIDecisionResponse(BaseModel):
    """Result of a decision: the updated suggestion and the ticket's current values."""

    suggestion: AISuggestionResponse
    ticket_id: int
    ticket_category: str | None
    ticket_priority: str | None
    activities_recorded: int
