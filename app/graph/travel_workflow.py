# app/graph/travel_workflow.py
from typing import Literal
from langgraph.graph import END, START, StateGraph
from langgraph.checkpoint.postgres import PostgresSaver
from psycopg_pool import ConnectionPool
from psycopg.rows import dict_row

from app.config import settings
from app.graph.state.travel_state import TravelState
from app.graph.nodes.travel_node import extract_travel_intent
from app.graph.nodes.user_node import ask_missing_info
from app.graph.nodes.provider_node import fetch_live_travel_data
from app.graph.nodes.ai_node import generate_response

def route_conditional_path(state: TravelState) -> Literal["ask_user", "search_live_data", "generate_itinerary"]:
    messages = state.get("messages", [])
    last_msg = messages[-1]["content"].lower() if messages else ""
    
    if "history" in last_msg or "booking history" in last_msg:
        return "generate_itinerary"
        
    restart_triggers = ["book another", "new trip", "restart", "book hotel", "book a", "book flight", "book train", "book bus"]
    phase = state.get("current_phase", 1)
    if phase >= 4 and any(trigger in last_msg for trigger in restart_triggers):
        return "generate_itinerary"

    missing = state.get("missing_fields", [])
    if missing and len(missing) > 0:
        return "ask_user"
        
    if phase == 2 and not state.get("travel_options"):
        return "search_live_data"
        
    return "generate_itinerary"

def build_travel_orchestrator():
    workflow = StateGraph(TravelState)
    workflow.add_node("extract_intent", extract_travel_intent)
    workflow.add_node("ask_user", ask_missing_info)
    workflow.add_node("search_live_data", fetch_live_travel_data)
    workflow.add_node("generate_itinerary", generate_response)
    
    workflow.add_edge(START, "extract_intent")
    workflow.add_conditional_edges("extract_intent", route_conditional_path)
    workflow.add_edge("ask_user", END) 
    workflow.add_edge("search_live_data", "generate_itinerary")
    workflow.add_edge("generate_itinerary", END)
    
    db_uri = settings.checkpoint_database_url or settings.database_url
    if db_uri.startswith("postgresql+"):
        db_uri = "postgresql://" + db_uri.split("://", 1)[1]
        
    pool = ConnectionPool(
        conninfo=db_uri,
        min_size=1,
        max_size=4,
        kwargs={"autocommit": True, "row_factory": dict_row}
    )
    
    checkpointer = PostgresSaver(pool)
    checkpointer.setup()  
    
    return workflow.compile(checkpointer=checkpointer)

travel_agent = build_travel_orchestrator()