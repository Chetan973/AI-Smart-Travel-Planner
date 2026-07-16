import streamlit as st

from services.api_client import BookingAPI


def show_history_page():

    st.title("📚 Booking History")

    user_id = 1

    try:

        bookings = BookingAPI.history(user_id)

    except Exception as ex:

        st.error(str(ex))

        if st.button("⬅ Back"):

            st.session_state.page = "success"

            st.rerun()

        return

    if len(bookings) == 0:

        st.info("No bookings available.")

    else:

        for booking in bookings:

            with st.container(border=True):

                c1, c2 = st.columns([3, 1])

                with c1:

                    st.subheader(
                        booking["transport_name"]
                    )

                    st.write(
                        f"📍 {booking['source']} ➜ {booking['destination']}"
                    )

                    st.write(
                        f"🗓 {booking['journey_date']}"
                    )

                    st.write(
                        f"🕐 {booking['departure_time']} → {booking['arrival_time']}"
                    )

                    st.write(
                        f"🎫 {booking['booking_reference']}"
                    )

                with c2:

                    st.metric(
                        "Fare",
                        f"₹ {booking['total_amount']}"
                    )

                    st.success(
                        booking["booking_status"]
                    )

    st.markdown("---")

    if st.button(
        "🏠 Home",
        use_container_width=True
    ):

        st.session_state.page = "chat"

        st.rerun()
