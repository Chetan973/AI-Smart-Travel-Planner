# streamlit-ui/ui/payment_ui.py
import streamlit as st

from services.api_client import PaymentAPI


def show_payment_page():
    booking = st.session_state.get("booking_response")
    if not booking:
        st.error("No booking is ready for payment.")
        return

    st.title("Secure payment")
    st.success("Your booking is reserved. Complete payment to confirm it.")
    st.metric("Booking reference", booking["booking_reference"])
    st.metric("Amount", f"₹ {booking['total_amount']}")

    st.link_button(
        "Open Razorpay checkout",
        PaymentAPI.checkout_url(booking["booking_reference"]),
        type="primary",
        use_container_width=True,
    )
    st.caption("After paying in the Razorpay window, return here and verify the payment.")

    # ----------------------------------------------------
    # Demo Presentation Bypass
    # ----------------------------------------------------
    st.markdown("---")
    st.write("##### 🛠️ Presentation Mode")
    if st.button("Skip Payment (Demo Bypass)", use_container_width=True):
        try:
            with st.spinner("Authorizing demo mode bypass..."):
                # Fetch email from passenger state, fallback to a dummy if missing
                passenger = st.session_state.get("passenger", {})
                email = passenger.get("email", "demo@example.com")
                
                # Call the new bypass endpoint
                bypass_resp = PaymentAPI.demo_bypass({
                    "booking_reference": booking["booking_reference"],
                    "email": email
                })

                if bypass_resp.get("status") == "SUCCESS":
                    st.success("Bypass authorized!")
                    # Mock the payment state so success_ui.py renders correctly
                    st.session_state.payment_response = {"payment_status": "captured (Demo Mode)"}
                    st.session_state.page = "success"
                    st.rerun()
        except Exception as exc:
            st.error(f"Demo bypass failed. Ensure backend DEMO_MODE_ENABLED=True. Error: {exc}")
    st.markdown("---")

    # ----------------------------------------------------
    # Standard Flow
    # ----------------------------------------------------
    left, right = st.columns(2)
    with left:
        if st.button("Back to booking", use_container_width=True):
            st.session_state.page = "booking"
            st.rerun()
    with right:
        if st.button("Verify payment", use_container_width=True):
            try:
                payment = PaymentAPI.status(booking["booking_reference"])
                if payment["payment_status"].lower() == "captured":
                    st.session_state.payment_response = payment
                    st.session_state.page = "success"
                    st.rerun()
                st.warning(f"Payment is not complete yet. Current status: {payment['payment_status']}")
            except Exception as exc:
                st.error(f"Could not verify the payment: {exc}")