import streamlit as st
from services.api_client import APIClient


def handle_user_input():
    user_msg = st.session_state.chat_input
    if user_msg:
        # 1. Show user message
        st.session_state.messages.append({"role": "user", "content": user_msg})
        
        # 2. Call our updated API
        result = APIClient.send_chat_message(st.session_state.session_id, user_msg)
        
        # 3. Show AI response (which now contains beautiful Markdown itineraries from Gemini)
        st.session_state.messages.append({"role": "assistant", "content": result.get("ai_response")})
        
        # 4. SMART FLOW: If the agent successfully gathered everything and searched, unlock booking!
        if result.get("options_ready"):
            st.success("✨ Live travel options retrieved! You can now proceed to book.")
            # Save the extracted data to session state for the booking form
            st.session_state.booking_data = {
                "source": result.get("source"),
                "destination": result.get("destination"),
                "journey_date": result.get("journey_date")
            }
            # Trigger your existing UI state change to move to the booking screen
            st.session_state.current_page = "booking"
