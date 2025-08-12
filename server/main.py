import os.path
from typing import Any, Dict

from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from server.config import PORT, DATA_DIR, MOCK_DATA_FILENAME, STATS_TABLE
from server.data_layer import Postgres
from server.sql import get_create_table_query
from stats_handler import StatsHandler
from contextlib import asynccontextmanager
import os, pandas as pd

app = FastAPI()
handler = StatsHandler()

did_warmup = False

def warmup_once_local():
    global did_warmup
    if did_warmup:
        return
    did_warmup = True

    postgres = Postgres()
    df = pd.read_csv(os.path.join(DATA_DIR, MOCK_DATA_FILENAME))
    postgres.query(get_create_table_query(STATS_TABLE))         # make this idempotent (see below)
    postgres.set(df, "posts_metrics", ["post_id", "timestamp"])  # upsert if possible

@asynccontextmanager
async def lifespan(app: FastAPI):
    warmup_once_local()
    yield

app = FastAPI(lifespan=lifespan)


@app.get("/stats")
def stats() -> JSONResponse:
    try:
        result: Dict[str, Any] | list[Any] = handler.handle()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error") from e

    return JSONResponse(content=jsonable_encoder(result))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)
