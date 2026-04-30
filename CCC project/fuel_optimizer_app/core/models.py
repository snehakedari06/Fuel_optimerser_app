from dataclasses import dataclass

@dataclass
class Station:
    distance: float
    price: float

@dataclass
class PurchasePlan:
    station_num: int
    location: float
    price: float
    liters_bought: float
    cost: float
    reasoning: str = ""

