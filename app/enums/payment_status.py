from enum import Enum


class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    CREATED = "CREATED"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"