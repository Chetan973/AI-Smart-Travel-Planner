from enum import Enum


class IdentityType(str, Enum):
    AADHAR = "AADHAR"
    PAN = "PAN"
    PASSPORT = "PASSPORT"