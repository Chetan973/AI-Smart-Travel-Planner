# streamlit-ui/ui/success_ui.py
import streamlit as st


def show_success_page():

    booking = st.session_state.get("booking_response")
    payment = st.session_state.get("payment_response")
    passenger = st.session_state.get("passenger", {})

    st.balloons()

    st.success("🎉 Payment Completed Successfully")
    
    # --- NEW UX ADDITION: Email Notification Banner ---
    email_display = passenger.get("email", "your registered email")
    st.info(f"📩 A confirmation E-Ticket has been securely sent to **{email_display}**!")

    st.markdown("---")

    st.markdown(
        """
        # ✅ Booking Confirmed

        Thank you for booking with **AI Smart Travel Planner**
        """
    )

    st.markdown("---")

    if booking:

        c1, c2 = st.columns(2)

        with c1:

            st.metric(
                "Booking Reference",
                booking.get("booking_reference", "N/A")
            )

            st.metric(
                "Status",
                booking.get("booking_status", "CONFIRMED")
            )

        with c2:

            st.metric(
                "Provider",
                booking.get("provider", "N/A")
            )

            st.metric(
                "Amount",
                f"₹ {booking.get('total_amount', 0)}"
            )

        st.markdown("---")

        st.write("### Journey")

        st.write(
            f"📍 {booking.get('source', '')} ➜ {booking.get('destination', '')}"
        )

        st.write(
            f"🚆 {booking.get('transport_name', '')}"
        )

        st.write(
            f"🗓 {booking.get('journey_date', '')}"
        )

        st.write(
            f"🕐 {booking.get('departure_time', '')} → {booking.get('arrival_time', '')}"
        )

    if payment:

        st.markdown("---")

        st.write("### Payment")

        st.write(
            "Payment Status :",
            payment.get("payment_status", "captured")
        )

    st.markdown("---")

    c1, c2 = st.columns(2)

    with c1:

        if st.button(
            "📚 Booking History",
            use_container_width=True
        ):

            st.session_state.page = "history"

            st.rerun()

    with c2:

        if st.button(
            "🏠 New Search",
            use_container_width=True
        ):

            for key in ("travel_response", "booking_response", "payment_response", "selected_option", "passenger", "otp_user"):
                st.session_state.pop(key, None)

            st.session_state.page = "chat"

            st.rerun()