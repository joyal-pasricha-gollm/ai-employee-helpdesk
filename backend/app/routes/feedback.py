"""Endpoints for feedback on AI recommendations (helpful / not helpful)."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.permissions import require_roles, require_support_staff
from app.models.user import User
from app.routes.ai import SUGGESTION_NOT_FOUND, get_visible_ticket
from app.schemas.feedback import FeedbackCreate, FeedbackResponse, FeedbackSummary
from app.schemas.user import ROLE_EMPLOYEE, ROLE_SUPPORT_STAFF
from app.services import ai_service, feedback_service

router = APIRouter(prefix="/api", tags=["feedback"])

require_employee_or_staff = require_roles(ROLE_EMPLOYEE, ROLE_SUPPORT_STAFF)


@router.post(
    "/ai-suggestions/{suggestion_id}/feedback",
    response_model=FeedbackResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Mark an AI suggestion helpful or not (ticket's employee or support staff)",
    responses={
        404: {"description": "Suggestion not found, or not your ticket"},
        409: {"description": "You already gave feedback on this suggestion"},
    },
)
def give_feedback(
    suggestion_id: int,
    data: FeedbackCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_employee_or_staff),
) -> FeedbackResponse:
    suggestion = ai_service.get_suggestion(db, suggestion_id)
    if suggestion is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=SUGGESTION_NOT_FOUND)
    try:
        get_visible_ticket(db, suggestion.ticket_id, current_user)
    except HTTPException as exc:
        # Same message as a missing suggestion, so other employees learn nothing.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=SUGGESTION_NOT_FOUND) from exc
    try:
        feedback = feedback_service.create_feedback(db, suggestion, current_user, data)
    except feedback_service.FeedbackAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You have already given feedback on this suggestion",
        ) from exc
    return FeedbackResponse.model_validate(feedback)


@router.get(
    "/ai-feedback",
    response_model=FeedbackSummary,
    summary="View all AI feedback and helpful percentage (support staff only)",
)
def view_feedback(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_support_staff),
) -> FeedbackSummary:
    return feedback_service.list_feedback(db, skip=skip, limit=limit)
