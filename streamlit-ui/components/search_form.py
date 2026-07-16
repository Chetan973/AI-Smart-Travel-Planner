import streamlit as st
from datetime import date


def render():

    st.subheader("🔍 Search Journey")

    col1, col2 = st.columns(2)

    with col1:

        source = st.text_input(
            "Source",
            placeholder="Bangalore"
        )

    with col2:

        destination = st.text_input(
            "Destination",
            placeholder="Hubli"
        )

    col3, col4, col5 = st.columns(3)

    with col3:

        journey_date = st.date_input(
            "Journey Date",
            value=date.today()
        )

    with col4:

        travel_mode = st.selectbox(

            "Travel Mode",

            [

                "TRAIN",

                "FLIGHT",

                "BUS"

            ]

        )

    with col5:

        passengers = st.number_input(

            "Passengers",

            min_value=1,

            max_value=10,

            value=1

        )

    st.write("")

    clicked = st.button(

        "🚀 Search Travel",

        use_container_width=True

    )

    return {

        "clicked": clicked,

        "source": source,

        "destination": destination,

        "journey_date": str(journey_date),

        "travel_mode": travel_mode,

        "passengers": passengers

    }