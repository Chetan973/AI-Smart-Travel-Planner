"""
General Helper Methods
"""

from datetime import datetime


class Helpers:

    @staticmethod
    def current_timestamp():
        return datetime.now()

    @staticmethod
    def current_date():
        return datetime.now().date()

    @staticmethod
    def format_datetime(dt: datetime) -> str:
        return dt.strftime("%d-%m-%Y %H:%M:%S")

    @staticmethod
    def mask_email(email: str) -> str:
        """
        Example:
        chetan@gmail.com
        ↓
        che***@gmail.com
        """
        username, domain = email.split("@")
        return f"{username[:3]}***@{domain}"

    @staticmethod
    def mask_mobile(mobile: str) -> str:
        """
        Example:
        9876543210
        ↓
        987*****10
        """
        return mobile[:3] + "*****" + mobile[-2:]