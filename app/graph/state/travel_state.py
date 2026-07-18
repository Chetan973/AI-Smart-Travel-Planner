"""Persisted LangGraph state for a travel-planning session."""

# app/graph/state/travel_state.py
import operator
from typing import Annotated, Any, TypedDict, List, Optional

class TravelState(TypedDict, total=False):
    """Durable state schema capturing the entire orchestrator pipeline history."""
    messages: Annotated[list[dict[str, str]], operator.add]
    
    # Phase 1 & 2: Core Travel Lookups
    source: Optional[str]
    destination: Optional[str]
    journey_date: Optional[str]
    travel_mode: Optional[str]
    budget: Optional[float]
    preferences: List[str]
    missing_fields: List[str]
    validation_error: Optional[str]
    
    # Phase 2: Live Engine Aggregations
    search_results: List[dict[str, Any]]
    travel_options: List[dict[str, Any]]
    selected_option_id: Optional[int]
    search_error: Optional[str]
    
    # Workflow Progression Core
    current_phase: int  # Tracking states (Phases 1 to 5)
    
    # Phase 3: PII Collection & OTP Verification Slots
    passenger_name: Optional[str]
    passenger_email: Optional[str]
    passenger_phone: Optional[str]
    generated_otp: Optional[str]
    otp_verified: bool
    otp_attempts: int
    
    # Phase 4 & 5: Bookings, Webhooks, & Post-Confirmation
    active_booking_reference: Optional[str]
    payment_status: Optional[str]