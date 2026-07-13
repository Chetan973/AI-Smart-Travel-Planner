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

        message = MIMEMultipart()

        message["From"] = settings.smtp_email

        message["To"] = recipient_email

        message["Subject"] = "AI Smart Travel Planner - Email Verification"

        body = f"""
        <h2>Email Verification</h2>

        <p>Your OTP is:</p>

        <h1>{otp}</h1>

        <p>This OTP is valid for 5 minutes.</p>
        """

        message.attach(
            MIMEText(
                body,
                "html"
            )
        )

        server = smtplib.SMTP(
            "smtp.gmail.com",
            587
        )

        server.starttls()

        server.login(
            settings.smtp_email,
            settings.smtp_password
        )

        server.send_message(message)

        server.quit()