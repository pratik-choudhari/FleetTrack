import datetime
import json
import logging

from kafka import KafkaConsumer
from sqlalchemy.orm import Session
from sqlalchemy.orm.session import close_all_sessions

from src.utils.database import KAFKA_SERVERS, engine, TripPings
from src.utils.models import VehiclePing

consumer = KafkaConsumer("trip-ping", bootstrap_servers=KAFKA_SERVERS, auto_offset_reset='earliest',
                         enable_auto_commit=True, group_id='ping-group')
logging.basicConfig(filename="logs/consumer.log", level=logging.INFO,
                    format='(%(asctime)s) %(name)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)


count = 0
try:
    with Session(engine) as session:
        print("[INFO] Open DB session")
        print("[INFO] Reading messages from kafka")
        for messsage in consumer:
            obj = VehiclePing.parse_obj(json.loads(messsage.value))
            print(f"[INFO] Message received: {obj}")
            obj = TripPings(vehicle_id=obj.vehicle_id, lat=obj.location.lat, long=obj.location.long,
                            timestamp=datetime.datetime.now() + datetime.timedelta(minutes=count),
                            fuel_pct=obj.fuel, speed=obj.speed, battery_pct=obj.battery)
            session.add(obj)
            session.commit()
            count += 1
except KeyboardInterrupt:
    pass
except Exception as e:
    logger.exception(e)
    print(e)
finally:
    close_all_sessions()
    engine.dispose()
    consumer.close()
    print("[INFO] Closed all resources")
