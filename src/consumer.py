import json
import logging
import datetime

from sqlalchemy.orm import Session
from sqlalchemy.orm.session import close_all_sessions
from kafka import KafkaConsumer

from src.utils.database import KAFKA_SERVERS, engine, Base, TripPings
from src.utils.models import VehiclePing

consumer = KafkaConsumer("trip-ping", bootstrap_servers=KAFKA_SERVERS, auto_offset_reset='earliest',
                         enable_auto_commit=True, group_id='ping-group')
logging.basicConfig(filename="logs/consumer.log", level=logging.INFO,
                    format='(%(asctime)s) %(name)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

with engine.begin() as conn:
    Base.metadata.create_all(bind=conn)


try:
    with Session(engine) as session:
        for messsage in consumer:
            obj = VehiclePing.parse_obj(json.loads(messsage.value))
            print(obj)
            obj = TripPings(vehicle_id=1, timestamp=datetime.datetime.now(), lat=obj.location.lat, long=obj.location.long,
                            fuel_pct=obj.fuel, speed=obj.speed, battery_pct=obj.battery)
            session.add(obj)
            session.commit()
except KeyboardInterrupt:
    close_all_sessions()
    engine.dispose()
    consumer.close()
