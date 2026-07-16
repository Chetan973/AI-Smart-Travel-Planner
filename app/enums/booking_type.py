from enum import Enum


class BookingType(str, Enum):

    TRAVEL = "TRAVEL"

    HOTEL = "HOTEL"

    PACKAGE = "PACKAGE"