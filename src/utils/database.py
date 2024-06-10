import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

if not load_dotenv():
    raise RuntimeError('dotenv not found')

KAFKA_SERVERS = [f"{os.getenv('KAFKA_HOST')}:{os.getenv('KAFKA_PORT')}"]

url = "postgresql+psycopg2://{}:{}@{}:{}/{}"
url = url.format(os.getenv('POSTGRES_USER'), os.getenv('POSTGRES_PASSWORD'), os.getenv('POSTGRES_HOST'),
                 os.getenv('POSTGRES_PORT'), os.getenv('POSTGRES_DB_NAME'))

engine = create_engine(url)
session_maker = sessionmaker(engine)


class Base(DeclarativeBase):
    pass


