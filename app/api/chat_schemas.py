from pydantic import BaseModel, Field
from typing import List, Optional

class ChatRequest(BaseModel):
    session_id: str = Field(..., description="Unique identifier for the LangGraph memory thread")
    message: str = Field(..., description="The user's natural language input")

class ChatResponse(BaseModel):
    session_id: str
    ai_response: str
    missing_fields: List[str] = Field(default_factory=list)
    
    # ADD THIS: Allow the API to send travel options to the frontend
    travel_options: List[dict] = Field(default_factory=list)
    
    source: Optional[str] = None
    destination: Optional[str] = None
    journey_date: Optional[str] = None
    budget: Optional[float] = None
    preference: Optional[str] = None
    preferences: List[str] = Field(default_factory=list)
    search_error: Optional[str] = None
    
    options_ready: bool = False
