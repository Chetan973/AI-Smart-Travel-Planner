# app/services/chat_service.py
from app.graph.travel_workflow import travel_agent

class ChatService:
    @staticmethod
    def process_message(session_id: str, user_message: str) -> dict:
        """
        Executes the LangGraph state machine for a given session.
        The checkpointer automatically loads previous history using the thread_id.
        """
        # 1. Define the LangGraph Checkpointer Configuration
        config = {"configurable": {"thread_id": session_id}}
        
        # 2. Fetch the current state from memory (if it exists)
        current_state = travel_agent.get_state(config)
        
        # Extract existing messages or start a new list
        if current_state and current_state.values:
            messages = current_state.values.get("messages", [])
        else:
            messages = []
            
        # 3. Append the new user message
        messages.append({"role": "user", "content": user_message})
        
        # 4. Invoke the Graph with the updated messages
        # The graph will run through Extraction -> (Search) -> AI Response
        final_state = travel_agent.invoke({"messages": messages}, config=config)
        
        # 5. Extract the final AI response from the state
        ai_response = "I'm sorry, I couldn't process that request."
        if final_state.get("messages"):
            # The last message in the list should be from the 'assistant' (from ai_node or user_node)
            last_message = final_state["messages"][-1]
            if last_message.get("role") == "assistant":
                ai_response = last_message.get("content")
                
        # 6. Format the response for the frontend UI
        # app/services/chat_service.py
# ... inside process_message ...
        return {
            "session_id": session_id,
            "ai_response": ai_response,
            "missing_fields": final_state.get("missing_fields", []),
            "source": final_state.get("source"),
            "destination": final_state.get("destination"),
            "journey_date": final_state.get("journey_date"),
            "budget": final_state.get("budget"),
            "preference": final_state.get("preference"),
            
            # ADD THIS: Map the options from the LangGraph state to the API response
            "travel_options": final_state.get("travel_options", []), 
            
            "options_ready": bool(final_state.get("travel_options") and not final_state.get("missing_fields"))
        }
    @staticmethod
    def get_history(session_id: str) -> list:
        """Retrieves the chat history for the UI."""
        config = {"configurable": {"thread_id": session_id}}
        state = travel_agent.get_state(config)
        
        if state and state.values:
            return state.values.get("messages", [])
        return []
        
    @staticmethod
    def clear_session(session_id: str):
        """Clears the session memory."""
        # LangGraph checkpointers retain history permanently by design.
        # To "clear" a session, the frontend simply generates a new session_id (UUID).
        pass


class ChatService:
    """Run one persisted LangGraph turn without duplicating checkpoint state."""

    @staticmethod
    def process_message(session_id: str, user_message: str) -> dict:
        if not session_id.strip():
            raise ValueError("session_id is required.")
        if not user_message.strip():
            raise ValueError("message cannot be empty.")
        config = {"configurable": {"thread_id": session_id}}
        final_state = travel_agent.invoke(
            {"messages": [{"role": "user", "content": user_message.strip()}]},
            config=config,
        )
        messages = final_state.get("messages", [])
        ai_response = next(
            (message["content"] for message in reversed(messages) if message.get("role") == "assistant"),
            "I could not process that request.",
        )
        preferences = final_state.get("preferences", [])
        return {
            "session_id": session_id,
            "ai_response": ai_response,
            "missing_fields": final_state.get("missing_fields", []),
            "source": final_state.get("source"),
            "destination": final_state.get("destination"),
            "journey_date": final_state.get("journey_date"),
            "budget": final_state.get("budget"),
            "preferences": preferences,
            "preference": ", ".join(preferences) or None,
            "travel_options": final_state.get("travel_options", []),
            "search_error": final_state.get("search_error"),
            "options_ready": bool(final_state.get("travel_options") and not final_state.get("missing_fields")),
        }

    @staticmethod
    def get_history(session_id: str) -> list[dict[str, str]]:
        snapshot = travel_agent.get_state({"configurable": {"thread_id": session_id}})
        return list(snapshot.values.get("messages", [])) if snapshot and snapshot.values else []
