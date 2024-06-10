import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from kafka import KafkaProducer, errors
from starlette.responses import JSONResponse

from src.utils.database import KAFKA_SERVERS
from src.utils.models import VehiclePing

producer = KafkaProducer(bootstrap_servers=KAFKA_SERVERS,
                         value_serializer=lambda x: x.encode('utf-8'))
logging.basicConfig(filename="logs/producer.log", level=logging.INFO,
                    format='(%(asctime)s) %(name)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_):
    yield
    producer.close()


app = FastAPI(lifespan=lifespan)
app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"], )


@app.get("/")
def home():
    return "ping...pong"


@app.post("/ping")
def ping(data: VehiclePing):
    try:
        metadata = producer.send("trip-ping", data.json())
        return {"status": "OK", "detail": ""}
    except errors.KafkaTimeoutError:
        logger.error(f"Kafka producer timed out: {data.json()}")
        return JSONResponse({"status": "error", "detail": "Kafka timeout"}, status_code=500)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
