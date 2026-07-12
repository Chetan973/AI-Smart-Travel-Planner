"""
Security Utility Functions

This module provides helper methods for generating secure values such as:
- OTP
- Booking IDs
- Session Tokens
- Reference IDs

Note:
------
Do NOT generate Payment IDs or Transaction IDs here.

Those values are returned by external payment gateways
(Razorpay) or banks and must be stored exactly as received.
"""

import secrets
import string
from datetime import datetime

from app.utils.constants import BOOKING_PREFIX


class SecurityUtils:
    """
    Security helper methods.
    """

    @staticmethod
    def generate_otp(length: int = 6) -> str:
        """
        Generate a cryptographically secure numeric OTP.

        Example:
            583921
        """
        digits = string.digits

        return "".join(
            secrets.choice(digits)
            for _ in range(length)
        )

    @staticmethod
    def generate_reference(length: int = 10) -> str:
        """
        Generate a secure alphanumeric reference.

        Example:
            X8KD72PQLA
        """
        characters = string.ascii_uppercase + string.digits

        return "".join(
            secrets.choice(characters)
            for _ in range(length)
        )

    @staticmethod
    def generate_booking_id() -> str:
        """
        Generate Application Booking ID.

        Example:
            BK-20260713-X9K2PLM8
        """

        date = datetime.now().strftime("%Y%m%d")

        reference = SecurityUtils.generate_reference(8)

        return f"{BOOKING_PREFIX}-{date}-{reference}"

    @staticmethod
    def generate_session_token(length: int = 64) -> str:
        """
        Generate a secure session token.

        Example:
            hG82kaM......
        """

        alphabet = (
            string.ascii_letters
            + string.digits
        )

        return "".join(
            secrets.choice(alphabet)
            for _ in range(length)
        )