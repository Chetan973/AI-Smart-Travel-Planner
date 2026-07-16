from datetime import date
from typing import Any

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field

from app.enums.booking_status import BookingStatus
from app.enums.graph_status import GraphStatus
from app.enums.identity_type import IdentityType
from app.enums.payment_status import PaymentStatus
from app.enums.travel_mode import TravelMode


class TravelState(BaseModel):
    """
    Shared LangGraph State

    This object flows through every LangGraph node.

    User
        ↓
    Identity Verification
        ↓
    Travel Search
        ↓
    AI Recommendation
        ↓
    Provider Search
        ↓
    Booking
        ↓
    Payment
        ↓
    Confirmation
    """

    model_config = ConfigDict(
        validate_assignment=True,
        extra="allow",
        arbitrary_types_allowed=True
    )

    # =====================================================
    # Session
    # =====================================================

    session_id: str | None = None

    # =====================================================
    # User
    # =====================================================

    user_id: int | None = None

    full_name: str | None = None

    email: str | None = None

    mobile_no: str | None = None

    email_verified: bool = False

    # =====================================================
    # Identity Verification
    # =====================================================

    identity_type: IdentityType | None = None

    identity_number: str | None = None

    identity_verified: bool = False

    # =====================================================
    # Travel Details
    # =====================================================

    source: str | None = None

    destination: str | None = None

    journey_date: date | None = None

    return_date: date | None = None

    travel_mode: TravelMode | None = None

    passengers: int | None = None
    budget: float | None = None
    travel_preference: str | None = None
    recommended_option_id: int | None = None

    # =====================================================
    # AI Recommendation
    # =====================================================

    recommendation: str | None = None

    ai_response: str | None = None

    # =====================================================
    # Provider
    # =====================================================

    provider: str | None = None

    provider_reference: str | None = None

    travel_options: list[dict[str, Any]] = Field(default_factory=list)

    selected_option_id: int | None = None

    selected_option: dict[str, Any] = Field(default_factory=dict)

    # =====================================================
    # Booking
    # =====================================================

    booking_status: BookingStatus = BookingStatus.PENDING

    booking_id: str | None = None

    booking_reference: str | None = None

    # =====================================================
    # Payment
    # =====================================================

    payment_status: PaymentStatus = PaymentStatus.PENDING

    payment_id: str | None = None

    payment_reference: str | None = None

    payment_url: str | None = None

    payment_completed: bool = False

    # =====================================================
    # Conversation Memory
    # =====================================================

    # The latest user turn is kept separately so a graph invocation is one
    # deterministic conversation turn.  A production deployment can add a
    # message store without changing the routing contract.
    input_message: str | None = None
    conversation_phase: str = "IDLE"
    requested_action: str | None = None
    missing_fields: list[str] = Field(default_factory=list)

    # =====================================================
    # LangGraph Workflow
    # =====================================================

    graph_status: GraphStatus = GraphStatus.STARTED

    next_node: str | None = None

    # =====================================================
    # Metadata
    # =====================================================

    metadata: dict[str, Any] = Field(default_factory=dict)
