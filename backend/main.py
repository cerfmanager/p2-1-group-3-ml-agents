import json
import os
import logging
import sqlite3 as sql
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path


DATABASE_NAME = "database/runs.db"
SCHEMA_NAME = "database/squema.sql"
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

logger = logging.getLogger(__name__)
logging.basicConfig(filename="serv.log", level=logging.INFO)
logger.info("Logging started")



db_connection: sql.Connection|None = None
cursor: sql.Cursor|None = None

from fastapi import FastAPI, HTTPException



HEARTBEAT_TIMEOUT = timedelta(seconds=60)
RUN_TRANSITIONS = {
    "run.started": ("assigned", "running"),
    "run.completed": ("running", "completed"),
    "run.failed": ("running", "failed"),
}

@dataclass
class RunState:
    run_id: str
    config_id: str
    machine_id: str
    hyperparameter: str|None
    value: float|None
    repetitions: int
    status: str = "pending"


@dataclass
class RunResponse:
    run_id: str
    status: str
    #this is an ENTIRE csv
    result: str




@asynccontextmanager
async def lifespan(app: FastAPI):
    global db_connection, cursor
    logger.info("Starting server")
    try:
        is_new = not os.path.exists(DATABASE_NAME)
        db_connection = sql.connect(DATABASE_NAME)
        cursor = db_connection.cursor()
        if is_new:
            with open(SCHEMA_NAME) as f:
                cursor.executescript(f.read())
        logger.info("Connected to database")
        #TODO implement this
        #scheduler.populatedb(cursor)
    except sql.OperationalError:
        logger.exception("Failed to connect to database")

    yield

    if cursor is not None:
        cursor.close()
    if db_connection is not None:
        db_connection.close()
    logger.info("Disconnected from database")
    logger.info("Stopping server")

app = FastAPI(
    title="Communication Server",
    description="Central HTTP server for managing training runs",
    version="0.1.0",
    lifespan=lifespan,
)






@app.get("/health")
def health_check():
    return {"status": "ok"}



@app.get("/get_run/{machine_id}",response_model=RunState)
async def get_run(machine_id: str):

    run_state =  await get_top_run_set_machine_id(machine_id)

    logger.info(f"{machine_id} got run {run_state.run_id}")

    await move_to_table_by_run_id(run_state.run_id,"pending_runs","running_runs")


    return run_state


@app.post("/complete_run/")
async def complete_run(run: RunResponse):
    path =  os.path.join(UPLOAD_DIR, f"{run.run_id}.csv")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(run.result)

    cursor.execute("""
    SELECT started_at from running_runs WHERE run_id = ?
    """)
    start_time = cursor.fetchone()[0]

    time = datetime.now()

    await move_to_table_by_run_id(run.run_id,"running_runs","completed_runs")

    cursor.execute("""
                   UPDATE pending
                   SET
                       started_at=?
                       completed_at=?
                   WHERE run_id = ?
                   """, ( start_time,time, run.run_id))
    db_connection.commit()

    logger.info(f"{run.run_id} completed !")

    return {"OK":""}







async def get_top_run_set_machine_id(machine_id: str):
    cursor.execute("""
    SELECT * FROM pending ORDER BY run_id LIMIT 1;
    """)
    row = cursor.fetchone()
    if row is None:
        raise HTTPException(404, "No pending runs")
    run = RunState(
        run_id=row[0],
        config_id=row[1],
        machine_id=row[2],
        repetitions=row[5],
        hyperparameter=row[3],
        value=row[4],
    )

    time = datetime.now()

    ## update the field
    cursor.execute("""
    UPDATE pending SET machine_id=?,started_at=? WHERE run_id=?
    """, (machine_id,time, run.run_id))
    db_connection.commit()

    return run


async def move_to_table_by_run_id(run_id,from_table,to_table):
    #get the row how it currently is
    cursor.execute(f"""
    SELECT * FROM {from_table} WHERE run_id=?;
    """,(run_id,))
    row = cursor.fetchone()

    #add it to the other table
    cursor.execute(f"""
    INSERT INTO {to_table} (run_id, config_id, machine_id,repetition,hyperparameter,value) VALUES (?,?,?,?,?,?);
    """,(row[0],row[1],row[2],row[3],row[4],row[5]))

    #remove it from the first table
    cursor.execute(f"""
    DELETE FROM {from_table} WHERE run_id=?;
    """,(run_id,))
    db_connection.commit()
