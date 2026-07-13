from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.sql import func

from app.database import Base


class OTP(Base):

    __tablename__ = "email_otps"

    otp_id = Column(
        Integer,
        primary_key=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.user_id"),
        nullable=False
    )

    email = Column(
        String(120),
        nullable=False
    )

    otp = Column(
        String(6),
        nullable=False
    )

    verified = Column(
        Boolean,
        default=False
    )

    attempt_count = Column(
        Integer,
        default=0
    )

    expires_at = Column(
        DateTime(timezone=True),
        nullable=False
    )

    verified_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )