import enum
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, DECIMAL, TIMESTAMP, Column, Integer, Enum
from sqlalchemy.orm import DeclarativeBase

if not load_dotenv():
    raise RuntimeError('dotenv not found')

KAFKA_SERVERS = [f"{os.getenv('KAFKA_HOST')}:{os.getenv('KAFKA_PORT')}"]

CXN_URL = "postgresql+psycopg2://{}:{}@{}:{}/{}"
CXN_URL = CXN_URL.format(os.getenv('POSTGRES_USER'), os.getenv('POSTGRES_PASSWORD'), os.getenv('POSTGRES_HOST'),
                         os.getenv('POSTGRES_PORT'), os.getenv('POSTGRES_DB_NAME'))

engine = create_engine(CXN_URL)


class Base(DeclarativeBase):
    pass


class VehicleType(enum.Enum):
    CAR = 1
    TRUCK = 2
    VAN = 3
    TRAILER = 4
    CONTAINER = 5


class VehicleStatus(enum.Enum):
    IDLE = 1
    ONTRIP = 2
    MAINTENANCE = 3
    NONOPERATIONAL = 4


class Vehicle(Base):
    __tablename__ = "Vehicle"
    vehicle_id = Column(Integer, primary_key=True, autoincrement=True)
    transmitter_id = Column(Integer, nullable=False)
    type = Column(Enum(VehicleType, create_type=False), nullable=False)
    status = Column(Enum(VehicleStatus), nullable=False)
    distance = Column(DECIMAL(9, 2), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)


class TripPings(Base):
    __tablename__ = "TripPings"
    id = Column(Integer, primary_key=True, autoincrement=True)
    vehicle_id = Column(Integer)
    timestamp = Column(TIMESTAMP, nullable=False)
    lat = Column(DECIMAL(8, 6), nullable=False)
    long = Column(DECIMAL(9, 6), nullable=False)
    fuel_pct = Column(DECIMAL(3, 2))
    speed = Column(DECIMAL(5, 2), nullable=False)
    battery_pct = Column(DECIMAL(3, 2))
