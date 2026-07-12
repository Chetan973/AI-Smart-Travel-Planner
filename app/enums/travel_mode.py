from enum import Enum


class TravelMode(str, Enum):
    TRAIN = "TRAIN"
    BUS = "BUS"
    FLIGHT = "FLIGHT"