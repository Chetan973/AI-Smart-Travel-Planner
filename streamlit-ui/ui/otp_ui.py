# streamlit-ui/ui/otp_ui.py
import streamlit as st
from services.api_client import BookingAPI, OTPAPI

def show_otp_page():
    """Verify the traveller before creating the booking and payment order."""
    passenger = st.session_state.get("passenger")
    option = st.session_state.get("selected_option")
    context = st.session_state.get("travel_context", {})

    if not passenger or not option:
        st.error("Your booking details are missing. Please choose a travel option again.")
        if st.button("Back to results"):
            st.session_state.page = "results"
            st.rerun()
        return

    st.title("Email verification")
    st.write(f"We will send a six-digit verification code to **{passenger['email']}**.")

    if "otp_user" not in st.session_state:
        if st.button("Send verification code", type="primary", use_container_width=True):
            try:
                with st.spinner("Sending verification code..."):
                    st.session_state.otp_user = OTPAPI.initialize_user(
                        {"full_name": passenger["full_name"], "email": passenger["email"], "mobile_no": passenger["phone"]}
                    )
                st.success("Verification code sent. Check your inbox.")
                st.rerun()
            except Exception as exc:
                st.error(f"Could not send the verification code: {exc}")
        return

    otp = st.text_input("Verification code", max_chars=6, type="password")
    left, right = st.columns(2)
    with left:
        if st.button("Back", use_container_width=True):
            st.session_state.pop("otp_user", None)
            st.session_state.page = "booking"
            st.rerun()
    with right:
        if st.button("Verify and continue", type="primary", use_container_width=True):
            if len(otp) != 6 or not otp.isdigit():
                st.error("Enter the six-digit code from your email.")
                return
            try:
                with st.spinner("Verifying your email and creating the booking..."):
                    # 1. Verify OTP (If it fails, it will automatically jump to the "except" block)
                    OTPAPI.verify(passenger["email"], otp)
                    
                    # 2. Create the Booking Record
                    st.session_state.booking_response = BookingAPI.create(
                        {
                            "user_id": st.session_state.otp_user["user_id"], 
                            "session_id": st.session_state.session_id,
                            "option_id": option["option_id"], 
                            "passengers": context.get("passengers") or 1
                        }
                    )
                # 3. Move forward to the Payment Page!
                st.session_state.page = "payment"
                st.rerun()
            except Exception as exc:
                st.error(f"Invalid OTP or Verification Failed. Please try again.")
