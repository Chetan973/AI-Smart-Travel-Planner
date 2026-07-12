"""
Validation Utility Functions
"""

import re


class Validators:

    @staticmethod
    def validate_mobile(mobile: str) -> bool:
        """
        Validate Indian Mobile Number.
        """
        pattern = r"^[6-9]\d{9}$"
        return bool(re.fullmatch(pattern, mobile))

    @staticmethod
    def validate_pan(pan: str) -> bool:
        """
        Validate PAN Number.
        Example: ABCDE1234F
        """
        pattern = r"^[A-Z]{5}[0-9]{4}[A-Z]$"
        return bool(re.fullmatch(pattern, pan.upper()))

    @staticmethod
    def validate_aadhaar(aadhaar: str) -> bool:
        """
        Validate Aadhaar Number.
        """
        pattern = r"^\d{12}$"
        return bool(re.fullmatch(pattern, aadhaar))

    @staticmethod
    def validate_name(name: str) -> bool:
        """
        Validate Full Name.
        """
        return len(name.strip()) >= 3