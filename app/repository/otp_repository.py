from sqlalchemy.orm import Session

from app.models import OTP


class OTPRepository:

    @staticmethod
    def save(
        db: Session,
        otp: OTP
    ) -> OTP:

        db.add(otp)

        db.commit()

        db.refresh(otp)

        return otp

    @staticmethod
    def get_latest_otp(
        db: Session,
        user_id: int
    ) -> OTP | None:

        return (
            db.query(OTP)
            .filter(OTP.user_id == user_id)
            .order_by(OTP.created_at.desc())
            .first()
        )
    
    @staticmethod
    def update(
        db: Session,
        otp: OTP
    ) -> OTP:

        db.commit()

        db.refresh(otp)

        return otp


    @staticmethod
    def get_by_email(
        db: Session,
        email: str
    ) -> OTP | None:

        return (
            db.query(OTP)
            .filter(
                OTP.email == email,
                OTP.verified == False
            )
            .order_by(
                OTP.created_at.desc()
            )
            .first()
        )