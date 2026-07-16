import streamlit as st

from services.api_client import BookingAPI


def show_booking_page():

    option = st.session_state.selected_option

    st.title("🎫 Review Your Journey")

    # ----------------------------------------------------
    # Journey Summary
    # ----------------------------------------------------

    with st.container(border=True):

        st.subheader(option["transport_name"])

        st.caption(option["transport_number"])

        c1, c2 = st.columns(2)

        with c1:

            st.write("📍 Source")

            st.success(option["source"])

            st.write("🕐 Departure")

            st.info(option["departure_time"])

        with c2:

            st.write("📍 Destination")

            st.success(option["destination"])

            st.write("🕐 Arrival")

            st.info(option["arrival_time"])

        st.divider()

        c1, c2, c3 = st.columns(3)

        c1.metric(

            "Duration",

            option["duration"]

        )

        c2.metric(

            "Seats",

            option["available_seats"]

        )

        c3.metric(

            "Rating",

            option["rating"]

        )

    # ----------------------------------------------------
    # Passenger Details
    # ----------------------------------------------------

    st.subheader("👤 Passenger Information")

    full_name = st.text_input(

        "Full Name"

    )

    email = st.text_input(

        "Email"

    )

    phone = st.text_input(

        "Mobile Number"

    )

    # ----------------------------------------------------
    # AI Tips
    # ----------------------------------------------------

    st.info(

        """
🤖 AI Travel Tip

• Reach the station at least 30 minutes early.

• Carry a valid ID proof.

• Keep your booking reference handy.
        """
    )

    # ----------------------------------------------------
    # Fare Summary
    # ----------------------------------------------------

    st.subheader("💰 Fare Summary")

    st.metric(

        "Total Fare",

        f"₹ {option['price']}"

    )

    st.divider()

    left, right = st.columns(2)

    with left:

        if st.button(

            "⬅ Back",

            use_container_width=True

        ):

            st.session_state.page = "results"

            st.rerun()

    with right:

        if st.button(

            "📧 Continue to OTP",

            use_container_width=True,

            type="primary"

        ):

            if not full_name:

                st.error("Enter Full Name")

                st.stop()

            if not email:

                st.error("Enter Email")

                st.stop()

            if not phone:

                st.error("Enter Mobile Number")

                st.stop()

            st.session_state.passenger = {

                "full_name": full_name,

                "email": email,

                "phone": phone

            }

            st.session_state.page = "otp"

            st.rerun()