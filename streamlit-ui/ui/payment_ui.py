# streamlit-ui/ui/payment_ui.py
import streamlit as st
import requests
from services.api_client import PaymentAPI

# Base URL for direct backend calls if PaymentAPI doesn't have create_order
BASE_URL = "http://127.0.0.1:8000/api"

def show_payment_page():
    booking = st.session_state.get("booking_response")
    if not booking:
        st.error("No booking is ready for payment.")
        return

    st.title("Secure payment")
    
    # ----------------------------------------------------
    # Smart Check: Is Razorpay Disabled?
    # ----------------------------------------------------
    if "payment_initialized" not in st.session_state:
        with st.spinner("Initializing secure gateway..."):
            try:
                # Ask the backend to create an order
                resp = requests.post(
                    f"{BASE_URL}/payments/create-order",
                    json={"booking_reference": booking["booking_reference"]}
                )
                resp.raise_for_status()
                order_data = resp.json()
                
                # If backend says skipped, bypass everything!
                if order_data.get("razorpay_order_id") == "skipped_no_config":
                    st.success("✅ Payment module is disabled. Booking confirmed automatically!")
                    st.info(order_data.get("message", "Proceeding securely without payment."))
                    
                    st.session_state.payment_response = {"payment_status": "captured (No-Config Bypass)"}
                    st.session_state.page = "success"
                    st.rerun()
                    return
                
                # Otherwise, mark as initialized and proceed normally
                st.session_state.payment_initialized = True
            except Exception as exc:
                st.error(f"Failed to initialize payment gateway: {exc}")
                return

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
                passenger = st.session_state.get("passenger", {})
                email = passenger.get("email", "demo@example.com")
                
                bypass_resp = PaymentAPI.demo_bypass({
                    "booking_reference": booking["booking_reference"],
                    "email": email
                })

                if bypass_resp.get("status") == "SUCCESS":
                    st.success("Bypass authorized!")
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
            st.session_state.pop("payment_initialized", None) # Clear init state if going back
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