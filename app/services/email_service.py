# app/services/email_service.py
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app.config import settings

class EmailService:

    @staticmethod
    def send_otp(
        recipient_email: str,
        otp: str
    ):
        # "alternative" is best practice for HTML emails
        message = MIMEMultipart("alternative")
        message["From"] = settings.smtp_email
        message["To"] = recipient_email
        
        # Making the subject unique prevents Gmail from "threading" and hiding the body!
        message["Subject"] = f"Your OTP is {otp} - AI Smart Travel Planner"

        # Wrapped in proper HTML tags
        body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; color: #333;">
                <h2>Email Verification</h2>
                <p>Your one-time password (OTP) for booking is:</p>
                <h1 style="color: #0b5ed7;">{otp}</h1>
                <p>This OTP is valid for 5 minutes.</p>
            </body>
        </html>
        """

        message.attach(MIMEText(body, "html"))

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(settings.smtp_email, settings.smtp_password)
            server.send_message(message)
            server.quit()
            print(f"OTP successfully emailed to {recipient_email}")
        except Exception as e:
            print(f"Failed to send OTP email: {e}")

    @staticmethod
    def send_booking_confirmation(
        recipient_email: str,
        booking_details: dict
    ):
        """
        Sends an HTML E-Ticket confirmation email after successful payment.
        """
        message = MIMEMultipart("alternative")
        message["From"] = settings.smtp_email
        message["To"] = recipient_email
        message["Subject"] = f"🎟️ E-Ticket Confirmed: {booking_details.get('booking_reference')} - AI Smart Travel Planner"

        body = f"""
        <html>
        <body style="background-color: #f2f6fb; padding: 20px;">
            <div style="font-family: Arial, sans-serif; background-color: white; max-width: 600px; margin: auto; border: 1px solid #ddd; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
                <div style="background-color: #0b5ed7; color: white; padding: 20px; text-align: center;">
                    <h2 style="margin:0;">🎟️ E-Ticket Confirmed</h2>
                    <p style="margin-top:5px; font-size:14px; color: #e0e0e0;">Thank you for booking with AI Smart Travel Planner!</p>
                </div>
                <div style="padding: 25px; color: #333;">
                    <p style="font-size: 16px;"><strong>Booking Reference:</strong> <span style="color:#0b5ed7;">{booking_details.get('booking_reference')}</span></p>
                    <p style="font-size: 16px;"><strong>Status:</strong> <span style="color: green; font-weight: bold;">PAID & CONFIRMED</span></p>
                    
                    <hr style="border: 0; border-top: 1px solid #eee; margin: 20px 0;">
                    
                    <h3 style="color:#333;">Journey Details</h3>
                    <table style="width: 100%; text-align: left; border-collapse: collapse;">
                        <tr>
                            <td style="padding: 8px 0; border-bottom: 1px solid #f9f9f9;"><strong>Transport:</strong></td>
                            <td style="padding: 8px 0; border-bottom: 1px solid #f9f9f9;">{booking_details.get('transport_name')} ({booking_details.get('transport_number')})</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; border-bottom: 1px solid #f9f9f9;"><strong>Route:</strong></td>
                            <td style="padding: 8px 0; border-bottom: 1px solid #f9f9f9;">{booking_details.get('source')} ➜ {booking_details.get('destination')}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; border-bottom: 1px solid #f9f9f9;"><strong>Date:</strong></td>
                            <td style="padding: 8px 0; border-bottom: 1px solid #f9f9f9;">{booking_details.get('journey_date')}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; border-bottom: 1px solid #f9f9f9;"><strong>Timings:</strong></td>
                            <td style="padding: 8px 0; border-bottom: 1px solid #f9f9f9;">{booking_details.get('departure_time')} - {booking_details.get('arrival_time')}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; border-bottom: 1px solid #f9f9f9;"><strong>Passengers:</strong></td>
                            <td style="padding: 8px 0; border-bottom: 1px solid #f9f9f9;">{booking_details.get('passengers')}</td>
                        </tr>
                    </table>

                    <hr style="border: 0; border-top: 1px solid #eee; margin: 20px 0;">
                    
                    <h3 style="color:#333;">Payment Summary</h3>
                    <p style="font-size: 18px; font-weight: bold;">Total Amount Paid: ₹ {booking_details.get('total_amount')}</p>
                    
                    <br>
                    <p style="text-align:center; color:#777; font-size:14px;">Have a safe and wonderful journey!</p>
                </div>
            </div>
        </body>
        </html>
        """

        message.attach(MIMEText(body, "html"))

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(settings.smtp_email, settings.smtp_password)
            server.send_message(message)
            server.quit()
            print(f"Confirmation ticket successfully emailed to {recipient_email}")
        except Exception as e:
            print(f"Failed to send confirmation email: {e}")