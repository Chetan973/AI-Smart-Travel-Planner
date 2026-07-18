# app/graph/nodes/ai_node.py
import re
from typing import Any
from datetime import date, datetime

from app.graph.state.travel_state import TravelState
from app.database import SessionLocal
from app.services.user_service import UserService
from app.services.otp_service import OTPService
from app.services.payment_service import PaymentService, PaymentFeatureDisabled
from app.services.booking_service import BookingService
from app.api.schemas import UserInitializationRequest
from app.models.booking import Booking
from app.enums.booking_status import BookingStatus
from app.repository.booking_repository import BookingRepository
from app.repository.user_repository import UserRepository

def generate_response(state: TravelState) -> dict[str, Any]:
    phase = state.get("current_phase", 1)
    messages = state.get("messages", [])
    last_user_text = messages[-1]["content"].strip() if messages else ""
    last_user_text_lower = last_user_text.lower()

    output_text = ""
    next_phase = phase
    updates: dict[str, Any] = {}

    # GLOBAL OVERRIDE: HISTORY
    if "booking history" in last_user_text_lower or "history" in last_user_text_lower:
        email = state.get("passenger_email")
        if not email:
            email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', last_user_text)
            if email_match:
                email = email_match.group(0)
                updates["passenger_email"] = email
            else:
                return {"messages": [{"role": "assistant", "content": "I need your email address to fetch your booking history. Please reply with: **'History [your email]'**."}]}
        
        try:
            with SessionLocal() as db:
                user = UserRepository.find_by_email(db, email)
                if user:
                    bookings = BookingService.get_user_bookings(db, user.user_id)
                    if bookings:
                        lines = [f"### 🗃️ Booking History for {email}\n"]
                        for b in bookings:
                            lines.append(f"- **{b.booking_reference}**: {b.source} ➔ {b.destination} on {b.journey_date} ({b.travel_mode.title()}) - **{b.booking_status.value}**")
                        output_text = "\n".join(lines)
                    else:
                        output_text = "No bookings found for this email address."
                else:
                    output_text = "No registered user found with that email address."
            return {**updates, "messages": [{"role": "assistant", "content": output_text}]}
        except Exception as e:
            return {"messages": [{"role": "assistant", "content": f"⚠️ Failed to fetch history: {str(e)}"}]}

    # GLOBAL OVERRIDE: RESTART
    restart_triggers = ["book another", "new trip", "restart", "book hotel", "book a", "book flight", "book train", "book bus"]
    if phase >= 4 and any(trigger in last_user_text_lower for trigger in restart_triggers):
        updates.update({
            "current_phase": 1,
            "source": None, "destination": None, "journey_date": None, "travel_mode": None, "budget": None,
            "preferences": [], "travel_options": [], "missing_fields": ["source", "destination", "journey_date", "travel_mode"],
            "selected_option_id": None, "generated_otp": None, "otp_verified": False, "otp_attempts": 0,
            "active_booking_reference": None, "search_error": None
        })
        output_text = "✨ I have cleared your previous itinerary! Where would you like to travel next? (e.g., 'Book a flight to Delhi tomorrow')"
        return {**updates, "messages": [{"role": "assistant", "content": output_text}]}

    # PHASE 1: LAZY SLOTS
    if phase == 1:
        missing = state.get("missing_fields", [])
        if "travel_mode" in missing:
            output_text = "Would you like to check options for a **Bus, Train, or Flight**?"
        elif missing:
            readable_fields = ", ".join(f.replace("_", " ").title() for f in missing)
            output_text = f"I need a few more details to find the best options. Please provide your: **{readable_fields}**."
        else:
            output_text = "Got all the details! Say **'search'** to fetch live itineraries."
            next_phase = 2

    # PHASE 2: LIVE SEARCH
    elif phase == 2:
        options = state.get("travel_options", [])
        search_err = state.get("search_error")
        match = re.search(r'\b([1-5])\b', last_user_text)
        
        if ("book" in last_user_text_lower or match) and options:
            idx = int(match.group(1)) if match else 1
            if 1 <= idx <= len(options):
                updates["selected_option_id"] = options[idx-1]["option_id"]
                output_text = "### 📋 Passenger Verification\nPlease provide your details to secure this booking:\n`Name: [Your Name] | Email: [Your Email] | Phone: [10 Digits]`"
                next_phase = 3
            else:
                output_text = "Invalid option selected. Please choose a valid number from the list above."
        elif search_err:
            output_text = f"⚠️ {search_err}\n\nPlease modify your budget constraints or dates to find available options."
        elif options:
            lines = [f"### 🎯 Live Routes: {state.get('source', '')} to {state.get('destination', '')}", "Ranked by parameters and budget restrictions:\n"]
            for o in options[:5]:
                # Safe String Replacement guarantees HTML won't render invisibly
                safe_name = str(o.get('transport_name', 'Unknown')).replace('<', '').replace('>', '')
                departure = o.get('departure_time') or '06:00'
                price = float(o.get('price', 0.0))
                
                lines.append(f"**Option {o.get('option_id', 1)}: {safe_name}** ({o.get('transport_number', 'N/A')})")
                lines.append(f"👉 Fare: ₹{price:,.2f} | Departs: {departure}\n")
                
            lines.append("\nType **'1'** (or your preferred number) to start the check-in process.")
            output_text = "\n".join(lines)
        else:
            output_text = "Live travel updates gathered. Type 'show results' to look into your options."

    # PHASE 3: PII COLLECTION
    elif phase == 3:
        if state.get("generated_otp") and not state.get("otp_verified"):
            clean_digits = "".join(filter(str.isdigit, last_user_text))
            email = state.get("passenger_email")
            
            if len(clean_digits) == 6:
                try:
                    with SessionLocal() as db:
                        user = OTPService.verify_otp(db, email, clean_digits)
                        selected_option = next((opt for opt in state.get("travel_options", []) if opt["option_id"] == state.get("selected_option_id")), None)
                        if not selected_option: raise ValueError("Selected transit option target is invalid.")
                            
                        booking = Booking(
                            user_id=user.user_id,
                            provider=selected_option["provider"],
                            travel_mode=selected_option["travel_mode"].upper(),
                            transport_name=selected_option["transport_name"],
                            transport_number=selected_option.get("transport_number"),
                            source=selected_option["source"],
                            destination=selected_option["destination"],
                            journey_date=date.fromisoformat(state["journey_date"]),
                            departure_time=selected_option.get("departure_time") or "06:00",
                            arrival_time=selected_option.get("arrival_time") or "12:00",
                            passengers=1,
                            total_amount=float(selected_option["price"]),
                            booking_status=BookingStatus.PENDING,
                            payment_completed=False
                        )
                        booking = BookingRepository.save(db, booking)
                        booking.booking_reference = f"BK-{datetime.now():%Y%m%d}-{booking.booking_id:06d}"
                        BookingRepository.update(db, booking)
                        
                        updates["active_booking_reference"] = booking.booking_reference
                        updates["otp_verified"] = True
                        output_text = f"### ✅ Identity Authenticated!\nYour booking **{booking.booking_reference}** is reserved.\n\nWould you like to proceed with **'Demo'** payment or **'Pay'** via Razorpay?"
                        next_phase = 4
                except Exception as e:
                    output_text = f"❌ Verification Failed: {str(e)}. Please check your code and try again."
            else:
                output_text = "Please enter the 6-digit code sent to your email."
        else:
            email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', last_user_text)
            phone_match = re.search(r'\b\d{10}\b', last_user_text)
            
            if email_match and phone_match:
                email = email_match.group(0)
                phone = phone_match.group(0)
                name_part = last_user_text.split("|")[0]
                name = re.sub(r'(?i)name:', '', name_part).strip() or "Passenger"
                
                try:
                    with SessionLocal() as db:
                        req = UserInitializationRequest(full_name=name, email=email, mobile_no=phone)
                        user = UserService.get_or_create_user(db, req)
                        OTPService.generate_and_send(db, user)
                    updates["passenger_email"] = email
                    updates["passenger_name"] = name
                    updates["generated_otp"] = "SENT" 
                    output_text = f"### 📧 Authentication Token Dispatched\nA 6-digit verification code has been sent to **{email}**.\n\nPlease enter the code here to confirm."
                except Exception as e:
                    output_text = f"⚠️ Failed to dispatch OTP: {str(e)}"
            else:
                output_text = "⚠️ **Input Mismatch.** Provide details exactly like:\n`Name: Chetan | Email: chetan@example.com | Phone: 9876543210`"

    # PHASE 4: PAYMENT BRANCHING
    elif phase == 4:
        ref = state.get("active_booking_reference")
        
        if "demo" in last_user_text_lower:
            try:
                with SessionLocal() as db:
                    PaymentService.process_demo_bypass(db, ref)
                output_text = "### 🎉 Transaction Authorized (Simulation)\nPayment was successful! Your ticket has been emailed to you.\n\nType **'Booking History'** at any time to view your past journeys."
                next_phase = 5
            except Exception as e:
                output_text = f"⚠️ Simulation failed: {e}"
                
        elif "pay" in last_user_text_lower or "razorpay" in last_user_text_lower:
            try:
                PaymentService.ensure_enabled()
                
                # HTML Button explicitly injected
                checkout_url = f"http://127.0.0.1:8000/checkout?booking_reference={ref}"
                button_html = f"<br><br><a href='{checkout_url}' target='_blank' style='display: inline-block; padding: 12px 24px; background-color: #0b5ed7; color: white; text-align: center; text-decoration: none; border-radius: 8px; font-weight: bold; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>💳 Open Secure Razorpay Checkout</a><br><br>"
                
                output_text = f"### 💳 Secure Checkout Terminal\n{button_html}Once your payment is completed in the new tab, your ticket will be emailed to you. Type **'Booking History'** here to view your confirmed journeys."
                next_phase = 5
                
            except PaymentFeatureDisabled:
                try:
                    with SessionLocal() as db:
                        PaymentService.process_demo_bypass(db, ref)
                    output_text = "Live payments are currently unavailable; proceeding with simulation mode.\n\n### 🎉 Transaction Authorized (Simulation)\nPayment was successful! Your ticket has been emailed to you.\n\nType **'Booking History'** at any time to view your past journeys."
                    next_phase = 5
                except Exception as e:
                    output_text = f"⚠️ Fallback to simulation failed: {e}"
        else:
            output_text = "Would you like to proceed with **'Demo'** payment or **'Pay'** via Razorpay?"

    # PHASE 5: POST-BOOKING
    elif phase == 5:
        output_text = "Your journey is fully booked! Type **'Booking History'** at any time to view your past journeys, or start a new chat to book another trip."

    updates["current_phase"] = next_phase
    return {
        **updates,
        "messages": [{"role": "assistant", "content": output_text}]
    }