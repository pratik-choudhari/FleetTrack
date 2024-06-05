from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.orm.session import close_all_sessions

from src.utils.database import *


@asynccontextmanager
async def lifespan(_):
    with engine.begin() as conn:
        Base.metadata.create_all(bind=conn)

    with Session(engine):
        pass

    yield
    close_all_sessions()
    engine.dispose()


app = FastAPI(lifespan=lifespan)
app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"], )


@app.get("/")
def ping():
    return "ping...pong"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
