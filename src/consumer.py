import json
import logging

from sqlalchemy.orm import Session
from sqlalchemy.orm.session import close_all_sessions
from kafka import KafkaConsumer, errors

from src.utils.database import *
from src.utils.models import VehiclePing

consumer = KafkaConsumer("vehicle-ping", bootstrap_servers=KAFKA_SERVERS, auto_offset_reset='earliest',
                         enable_auto_commit=True, group_id='ping-group')
logging.basicConfig(filename="logs/consumer.log", level=logging.INFO,
                    format='(%(asctime)s) %(name)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

with engine.begin() as conn:
    Base.metadata.create_all(bind=conn)

with Session(engine):
    pass


for messsage in consumer:
    obj = VehiclePing.parse_obj(json.loads(messsage.value))
    print(obj)
