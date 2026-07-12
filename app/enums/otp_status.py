from enum import Enum


class OTPStatus(str, Enum):
    PENDING = "PENDING"
    SENT = "SENT"
    VERIFIED = "VERIFIED"
    EXPIRED = "EXPIRED"
    FAILED = "FAILED"