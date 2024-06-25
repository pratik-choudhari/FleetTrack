import random
import time
from datetime import datetime
from multiprocessing import Process
from typing import Type

import requests
from sqlalchemy import delete, update
from sqlalchemy.orm import Session, close_all_sessions

from src.utils.database import engine, Vehicle, TripPings, VehicleType, VehicleStatus

NUM_VEHICLES = 18


def create_vehicles(n: int):
    with Session(engine) as session:
        query = delete(Vehicle)
        session.execute(query)

        query = delete(TripPings)
        session.execute(query)
        session.commit()

        for id_ in range(n):
            type_ = random.choice(list(VehicleType))
            if type_ in (VehicleType.CONTAINER, VehicleType.TRAILER):
                tmp = Vehicle(transmitter_id=id_, type=type_, status=VehicleStatus.IDLE,
                              distance=0, created_at=datetime.now())
            else:
                tmp = Vehicle(transmitter_id=id_, type=type_, status=VehicleStatus.IDLE,
                              distance=random.randint(1000, 5000), created_at=datetime.now())
            session.add(tmp)
            session.commit()


def set_vehicle_status() -> list[Type[Vehicle]]:
    with Session(engine) as session:
        all_vehicles = session.query(Vehicle).all()

    vehicle_sample = random.sample(all_vehicles, round(NUM_VEHICLES / 2))
    remaining_vehicle_ids = [vehicle.vehicle_id for vehicle in all_vehicles if vehicle not in vehicle_sample]

    with Session(engine) as session:
        for idx, vehicle_id in enumerate(remaining_vehicle_ids):
            tmp = update(Vehicle).where(Vehicle.vehicle_id == vehicle_id).values(
                status=VehicleStatus.MAINTENANCE if idx % 2 == 0 else VehicleStatus.NONOPERATIONAL)
            session.execute(tmp)
            session.commit()
    return vehicle_sample


class TripProcess(Process):
    def __init__(self, vehicle: Type[Vehicle], num_steps: int):
        super(TripProcess, self).__init__()
        self.vehicle = vehicle
        self.fuel_pct = random.randrange(start=50, stop=100) / 100
        self.battery_pct = random.randrange(start=80, stop=100) / 100
        self.speed_limits = range(20, 80) if vehicle.type == VehicleType.TRUCK else range(40, 120)
        self.num_steps = num_steps
        self.load = random.randrange(200, 800) if vehicle.type == VehicleType.TRUCK else 0
        self.is_healthy = True if vehicle.vehicle_id % 3 != 0 else False

    def run(self):
        print(f"[START] Trip for {self.vehicle.vehicle_id}")
        with Session(engine) as session:
            tmp = update(Vehicle).where(Vehicle.vehicle_id == self.vehicle.vehicle_id
                                        ).values(status=VehicleStatus.ONTRIP)
            session.execute(tmp)
            session.commit()

        for step in range(self.num_steps):
            self.fuel_pct -= 0.01
            if self.fuel_pct <= 0.2 and step < 2 * self.num_steps / 3:
                self.fuel_pct = 0.9

            if random.choice([True, False]):
                self.battery_pct += 0.01
            else:
                self.battery_pct -= 0.01

            requests.post("http://localhost:8000/ping",
                          json={"fuel": self.fuel_pct,
                                "speed": random.choice(self.speed_limits),
                                "vehicle_id": self.vehicle.vehicle_id,
                                "distance": 30 + step,
                                "load": self.load,
                                "vehicle_type": self.vehicle.type.value,
                                "battery": self.battery_pct,
                                "location": {"lat": 43.70011 - random.choice([0.01, 0.015, 0.02]),
                                             "long": -79.4163 - (step / 100) - random.choice([1, 2, 3, 4])}
                                })
            print(f"[INPROGRESS] Step {step}/{self.num_steps} for {self.vehicle.vehicle_id}")
            time.sleep(5)
        with Session(engine) as session:
            tmp = update(Vehicle).where(Vehicle.vehicle_id == self.vehicle.vehicle_id
                                        ).values(status=VehicleStatus.MAINTENANCE)
            session.execute(tmp)
            session.commit()
        print(f"[END] Trip for {self.vehicle.vehicle_id}")


if __name__ == '__main__':
    create_vehicles(NUM_VEHICLES)
    vehicles = set_vehicle_status()

    processes = []
    for obj in vehicles:
        p = TripProcess(obj, 100)
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
    close_all_sessions()
    engine.dispose()
