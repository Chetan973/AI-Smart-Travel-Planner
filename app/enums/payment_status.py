from enum import Enum


class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    CREATED = "CREATED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
