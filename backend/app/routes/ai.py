"""AI suggestion routes: analyze a ticket, view suggestions, record staff decisions."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user
from app.dependencies.permissions import require_support_staff
from app.models.ticket import Ticket
from app.models.user import User
from app.schemas.ai import AIDecisionRequest, AIDecisionResponse, AISuggestionResponse
from app.schemas.user import ROLE_SUPPORT_STAFF
from app.services import ai_service

router = APIRouter(prefix="/api", tags=["ai"])

TICKET_NOT_FOUND = "Ticket not found"
SUGGESTION_NOT_FOUND = "AI suggestion not found"


def get_visible_ticket(db: Session, ticket_id: int, user: User, lock: bool = False) -> Ticket:
    """Return the ticket if this user may see it. Employees only see their own (404 otherwise)."""
    ticket = db.get(Ticket, ticket_id, with_for_update=lock)
    if ticket is None or (user.role != ROLE_SUPPORT_STAFF and ticket.requester_id != user.id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=TICKET_NOT_FOUND)
    return ticket


@router.post(
    "/tickets/{ticket_id}/analyze",
    response_model=AISuggestionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Run AI analysis on a ticket (support staff)",
    responses={
        404: {"description": "Ticket not found"},
        502: {"description": "The AI returned invalid content; nothing was saved"},
        503: {"description": "The AI service is unavailable; nothing was saved"},
    },
)
def analyze_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_support_staff),
) -> AISuggestionResponse:
    ticket = get_visible_ticket(db, ticket_id, current_user)
    try:
        suggestion = ai_service.create_suggestion_for_ticket(db, ticket, current_user)
    except ai_service.AIServiceUnavailableError as exc:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc)) from exc
    except ai_service.AIInvalidResponseError as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc)) from exc
    return AISuggestionResponse.model_validate(suggestion)


@router.get(
    "/tickets/{ticket_id}/ai-suggestions",
    response_model=list[AISuggestionResponse],
    summary="List AI suggestions for a ticket (support staff, or the ticket's employee)",
)
def get_ticket_suggestions(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[AISuggestionResponse]:
    get_visible_ticket(db, ticket_id, current_user)
    suggestions = ai_service.list_suggestions_for_ticket(db, ticket_id)
    return [AISuggestionResponse.model_validate(item) for item in suggestions]


@router.patch(
    "/ai-suggestions/{suggestion_id}/decision",
    response_model=AIDecisionResponse,
    summary="Accept, reject or modify an AI suggestion (support staff)",
    responses={
        404: {"description": "Suggestion or ticket not found"},
        409: {"description": "A decision was already recorded"},
        422: {"description": "Invalid request, or stored suggestion values cannot be accepted"},
    },
)
def decide_suggestion(
    suggestion_id: int,
    request: AIDecisionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_support_staff),
) -> AIDecisionResponse:
    suggestion = ai_service.get_suggestion(db, suggestion_id, lock=True)
    if suggestion is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=SUGGESTION_NOT_FOUND)
    ticket = get_visible_ticket(db, suggestion.ticket_id, current_user, lock=True)
    try:
        count = ai_service.apply_decision(db, suggestion, ticket, current_user, request)
    except ai_service.SuggestionAlreadyDecidedError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"This suggestion was already decided (status: {suggestion.status})",
        ) from exc
    except ai_service.InvalidSuggestionError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="This suggestion has invalid category or priority values; use Modified instead",
        ) from exc
    return AIDecisionResponse(
        suggestion=AISuggestionResponse.model_validate(suggestion),
        ticket_id=ticket.id,
        ticket_category=ticket.category,
        ticket_priority=ticket.priority,
        activities_recorded=count,
    )
