from typing import Any

from langchain_core.messages import BaseMessage
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field

from app.enums import BookingStatus
from app.enums import GraphStatus
from app.enums import IdentityType
from app.enums import PaymentStatus
from app.enums import TravelMode


class TravelState(BaseModel):
    """
    Shared LangGraph State
    """

    model_config = ConfigDict(
        validate_assignment=True,
        extra="allow",
        arbitrary_types_allowed=True
    )

    # =====================================================
    # User
    # =====================================================

    user_id: int | None = None

    full_name: str | None = None

    email: str | None = None

    mobile_no: str | None = None

    # =====================================================
    # Identity
    # =====================================================

    identity_type: IdentityType | None = None

    identity_number: str | None = None

    identity_verified: bool = False

    # =====================================================
    # Travel
    # =====================================================

    source: str | None = None

    destination: str | None = None

    journey_date: str | None = None

    travel_mode: TravelMode | None = None

    passengers: int = 1

    # =====================================================
    # Search Result
    # =====================================================

    travel_options: list[dict[str, Any]] = Field(default_factory=list)

    selected_option: dict[str, Any] = Field(default_factory=dict)

    # =====================================================
    # Booking
    # =====================================================

    booking_status: BookingStatus = BookingStatus.PENDING

    booking_id: str | None = None

    # =====================================================
    # Payment
    # =====================================================

    payment_status: PaymentStatus = PaymentStatus.PENDING

    payment_id: str | None = None

    # =====================================================
    # Graph
    # =====================================================

    graph_status: GraphStatus = GraphStatus.STARTED

    # =====================================================
    # Conversation
    # =====================================================

    messages: list[BaseMessage] = Field(default_factory=list)

    # =====================================================
    # AI
    # =====================================================

    recommendation: str | None = None

    response: str | None = None