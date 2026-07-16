import uuid

import streamlit as st

from components.chat_window import show_chat
from components.hero import hero
from components.navbar import show
from services.api_client import ChatAPI
from ui.booking_ui import show_booking_page
from ui.history_ui import show_history_page
from ui.otp_ui import show_otp_page
from ui.payment_ui import show_payment_page
from ui.search_result_ui import show_results
from ui.success_ui import show_success_page

st.set_page_config(page_title="AI Smart Travel Planner", page_icon="✈️", layout="wide")

if "page" not in st.session_state:
    st.session_state.page = "chat"
if "chat_session_id" not in st.session_state:
    st.session_state.chat_session_id = str(uuid.uuid4())

if st.session_state.page == "chat":
    show()
    hero()
    st.markdown("## AI Travel Assistant")
    prompt = show_chat()
    if prompt:
        try:
            with st.spinner("Planning your trip..."):
                reply = ChatAPI.message(st.session_state.chat_session_id, prompt)
        except Exception as exc:
            st.session_state.messages.append({"role": "assistant", "content": f"I couldn't reach the travel service: {exc}"})
            st.rerun()

        st.session_state.messages.append({"role": "assistant", "content": reply["message"]})
        if reply["travel_options"]:
            st.session_state.travel_response = {
                "recommendation": reply["message"],
                "provider": reply["travel_options"][0]["provider"],
                "travel_options": reply["travel_options"],
            }
            st.session_state.travel_context = reply["travel_details"]
            st.session_state.page = "results"
        st.rerun()
elif st.session_state.page == "results":
    show_results()
elif st.session_state.page == "booking":
    show_booking_page()
elif st.session_state.page == "otp":
    show_otp_page()
elif st.session_state.page == "payment":
    show_payment_page()
elif st.session_state.page == "success":
    show_success_page()
elif st.session_state.page == "history":
    show_history_page()
