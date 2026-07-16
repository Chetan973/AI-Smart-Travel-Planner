import streamlit as st

from services.api_client import TravelAPI
from components.ai_card import render as ai_card
from components.travel_card import render as travel_card


def show_results():

    st.title("🚆 AI Travel Recommendation")

    ctx = st.session_state.travel_context

    # -----------------------------------------
    # Search only once
    # -----------------------------------------

    if "travel_response" not in st.session_state:

        with st.spinner("🤖 AI is finding the best travel options..."):

            st.session_state.travel_response = TravelAPI.search({

                "user_id": 1,

                "session_id": "travel-session-001",

                "source": ctx["source"],

                "destination": ctx["destination"],

                "journey_date": ctx["journey_date"],

                "travel_mode": ctx["travel_mode"],

                "passengers": ctx["passengers"]

            })

    response = st.session_state.travel_response

    # -----------------------------------------
    # AI Recommendation
    # -----------------------------------------

    ai_card(
        response["recommendation"]
    )

    st.divider()

    st.subheader("🚆 Available Travel Options")

    if len(response["travel_options"]) == 0:

        st.warning("No travel options available.")

        if st.button("⬅ Back"):

            st.session_state.page = "chat"

            st.rerun()

        return

    # -----------------------------------------
    # Travel Cards
    # -----------------------------------------

    for option in response["travel_options"]:

        booked = travel_card(option)

        if booked:

            st.session_state.selected_option = option

            st.session_state.page = "booking"

            st.rerun()

    st.divider()

    if st.button("⬅ Modify Search"):

        if "travel_response" in st.session_state:

            del st.session_state.travel_response

        st.session_state.page = "chat"

        st.rerun()