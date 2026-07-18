# app/graph/workflow.py
import redis
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.checkpoint.redis import RedisSaver
from psycopg_pool import ConnectionPool
from psycopg.rows import dict_row # Added requirement for LangGraph

from app.config import settings
from app.graph.state.travel_state import TravelState
from app.graph.nodes.travel_node import extract_travel_intent
from app.graph.nodes.provider_node import fetch_live_travel_data
from app.graph.nodes.ai_node import generate_response
from app.graph.nodes.user_node import ask_missing_info
from app.memory.redis_manager import RedisManager

# ======================================================
# 1. State Machine Configuration
# ======================================================
builder = StateGraph(TravelState)

# Register workflow nodes
builder.add_node("extract", extract_travel_intent)
builder.add_node("ask_user", ask_missing_info)
builder.add_node("search_live_data", fetch_live_travel_data)
builder.add_node("generate_itinerary", generate_response)

def route_after_extraction(state: TravelState):
    """
    Conditional routing engine logic.
    If mandatory parameters are missing, redirect to interactive form collection.
    Otherwise, move forward with real-time API integrations.
    """
    if len(state.missing_fields) > 0:
        return "ask_user"
    return "search_live_data"

# Wire state routing conditional edges and path bounds
builder.add_conditional_edges("extract", route_after_extraction)
builder.add_edge("ask_user", END)
builder.add_edge("search_live_data", "generate_itinerary")
builder.add_edge("generate_itinerary", END)

builder.set_entry_point("extract")

# ======================================================
# 2. Dynamic Checkpointer Strategy Assignment
# ======================================================
checkpointer = None

# Primary checkpointer route: In-Memory High-Performance Redis Checkpointer
if settings.checkpointer_type == "redis":
    try:
        redis_client = RedisManager.get_client()
        # Ping connection to verify accessibility
        redis_client.ping()
        checkpointer = RedisSaver(redis_client)
        print("⚡ LangGraph Memory orchestrated via High-Performance Redis Checkpointer.")
    except Exception as e:
        print(f"⚠️ Redis Checkpointer failed to initialize ({e}). Falling back to PostgreSQL.")
        settings.checkpointer_type = "postgres"

# Secondary/Fallback route: Relational Persistent PostgreSQL Checkpointer
if checkpointer is None or settings.checkpointer_type == "postgres":
    # Clean up connection strings dynamically:
    conn_info = settings.database_url
    if conn_info.startswith("postgresql+"):
        conn_info = "postgresql://" + conn_info.split("://", 1)[1]

    try:
        # Instantiate thread-safe connection pooler using normalized credentials
        pg_pool = ConnectionPool(
            conninfo=conn_info,
            kwargs={
                "autocommit": True,     # Fixes the transaction block crash
                "row_factory": dict_row # Fixes tuple indices TypeError
            }
        )
        checkpointer = PostgresSaver(pg_pool)
        
        # Instantiates system tracking tables structurally if missing in schemas
        checkpointer.setup() 
        print("💾 LangGraph Memory orchestrated via Persistent PostgreSQL Checkpointer.")
    except Exception as e:
        print(f"❌ Critical Error: Failed to initialize PostgreSQL Checkpointer: {e}")
        raise e

# ======================================================
# 3. Compilation with Hybrid Memory Adapter
# ======================================================
travel_agent = builder.compile(checkpointer=checkpointer)