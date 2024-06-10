from typing import Optional

from pydantic import BaseModel


class Location(BaseModel):
    lat: float
    long: float


class VehiclePing(BaseModel):
    fuel: Optional[float]
    speed: float
    location: Location
    distance: float
    load: float
    vehicle_type: int
    battery: Optional[float]
