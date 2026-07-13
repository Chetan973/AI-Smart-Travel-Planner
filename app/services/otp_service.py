from app.models import OTP
from app.repository.otp_repository import OTPRepository
from app.services.email_service import EmailService
from app.utils import SecurityUtils
from datetime import datetime
from datetime import timedelta

from app.repository.user_repository import UserRepository


class OTPService:

    @staticmethod
    def generate_and_send(
        db,
        user
    ):

        otp = SecurityUtils.generate_otp()

        otp_entity = OTP(
            user_id=user.user_id,
            email=user.email,
            otp=otp,
            verified=False,
            attempt_count=0,
            expires_at=datetime.now() + timedelta(minutes=5),
            verified_at=None
        )

        OTPRepository.save(
            db=db,
            otp=otp_entity
        )

        EmailService.send_otp(
            recipient_email=user.email,
            otp=otp
        )

        print("OTP Generated :", otp)
        print("OTP Saved Successfully")

        return otp_entity
    
    @staticmethod
    def verify_otp(
        db,
        email: str,
        otp: str
    ):

        otp_entity = OTPRepository.get_by_email(
            db,
            email
        )

        if otp_entity is None:
            raise ValueError("OTP not found.")

        if otp_entity.verified:
            raise ValueError("OTP already verified.")

        expiry_time = otp_entity.expires_at.replace(tzinfo=None)

        if datetime.now() > expiry_time:
            raise ValueError("OTP expired.")

        if otp_entity.otp != otp:

            otp_entity.attempt_count += 1

            OTPRepository.update(
                db,
                otp_entity
            )

            raise ValueError("Invalid OTP.")

        otp_entity.verified = True

        otp_entity.verified_at = datetime.now()

        OTPRepository.update(
            db,
            otp_entity
        )

        user = UserRepository.find_by_email(
            db,
            email
        )

        user.email_verified = True

        UserRepository.update(
            db,
            user
        )
        return user