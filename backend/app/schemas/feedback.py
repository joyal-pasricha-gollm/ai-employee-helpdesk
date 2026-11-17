"""AI feedback request and response schemas."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class FeedbackCreate(BaseModel):
    """Body for marking an AI suggestion helpful or not helpful."""

    is_helpful: bool
    feedback_comment: str | None = Field(default=None, max_length=1000)

    @field_validator("feedback_comment", mode="before")
    @classmethod
    def blank_to_none(cls, value: Any) -> Any:
        if isinstance(value, str):
            value = value.strip()
            return value or None
        return value


class FeedbackResponse(BaseModel):
    """One saved row of ai_feedback.

    employee_id is the id of the user who gave the feedback (employee or support staff).
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    suggestion_id: int
    employee_id: int
    is_helpful: bool
    feedback_comment: str | None
    created_at: datetime | None


class FeedbackListItem(FeedbackResponse):
    """Feedback plus its ticket and suggestion details, for the support feedback page."""

    given_by_name: str
    given_by_role: str
    ticket_id: int
    ticket_subject: str
    ticket_category: str | None
    ticket_priority: str | None
    suggested_category: str | None
    suggested_priority: str | None
    suggestion_status: str | None


class FeedbackSummary(BaseModel):
    """Feedback list with overall helpfulness numbers."""

    total: int
    helpful_count: int
    not_helpful_count: int
    helpful_percentage: float | None
    items: list[FeedbackListItem]
