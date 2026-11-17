"""Business logic for saving and viewing feedback on AI recommendations."""

import logging

from sqlalchemy import case, func, select
from sqlalchemy.orm import Session

from app.models.ai_feedback import AIFeedback
from app.models.ai_suggestion import AISuggestion
from app.models.ticket import Ticket
from app.models.user import User
from app.schemas.feedback import FeedbackCreate, FeedbackListItem, FeedbackSummary

logger = logging.getLogger(__name__)


class FeedbackAlreadyExistsError(Exception):
    """This user already gave feedback on this suggestion."""


def create_feedback(db: Session, suggestion: AISuggestion, user: User, data: FeedbackCreate) -> AIFeedback:
    """Save one feedback row. ai_feedback.employee_id stores whoever gave it."""
    existing = db.scalars(
        select(AIFeedback.id).where(
            AIFeedback.suggestion_id == suggestion.id,
            AIFeedback.employee_id == user.id,
        )
    ).first()
    if existing is not None:
        raise FeedbackAlreadyExistsError

    feedback = AIFeedback(
        suggestion_id=suggestion.id,
        employee_id=user.id,
        is_helpful=data.is_helpful,
        feedback_comment=data.feedback_comment,
    )
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    logger.info(
        "AI feedback saved: feedback_id=%s suggestion_id=%s user_id=%s helpful=%s",
        feedback.id,
        suggestion.id,
        user.id,
        data.is_helpful,
    )
    return feedback


def list_feedback(db: Session, skip: int = 0, limit: int = 100) -> FeedbackSummary:
    """Feedback with ticket and suggestion details, plus helpful percentage over all feedback."""
    total, helpful = db.execute(
        select(
            func.count(AIFeedback.id),
            func.coalesce(func.sum(case((AIFeedback.is_helpful.is_(True), 1), else_=0)), 0),
        )
    ).one()
    total, helpful = int(total), int(helpful)

    rows = db.execute(
        select(AIFeedback, AISuggestion, Ticket, User)
        .join(AISuggestion, AIFeedback.suggestion_id == AISuggestion.id)
        .join(Ticket, AISuggestion.ticket_id == Ticket.id)
        .join(User, AIFeedback.employee_id == User.id)
        .order_by(AIFeedback.created_at.desc(), AIFeedback.id.desc())
        .offset(skip)
        .limit(limit)
    ).all()

    items = [
        FeedbackListItem(
            id=feedback.id,
            suggestion_id=feedback.suggestion_id,
            employee_id=feedback.employee_id,
            is_helpful=feedback.is_helpful,
            feedback_comment=feedback.feedback_comment,
            created_at=feedback.created_at,
            given_by_name=user.full_name,
            given_by_role=user.role,
            ticket_id=ticket.id,
            ticket_subject=ticket.subject,
            ticket_category=ticket.category,
            ticket_priority=ticket.priority,
            suggested_category=suggestion.suggested_category,
            suggested_priority=suggestion.suggested_priority,
            suggestion_status=suggestion.status,
        )
        for feedback, suggestion, ticket, user in rows
    ]
    return FeedbackSummary(
        total=total,
        helpful_count=helpful,
        not_helpful_count=total - helpful,
        helpful_percentage=round(helpful * 100 / total, 1) if total else None,
        items=items,
    )
