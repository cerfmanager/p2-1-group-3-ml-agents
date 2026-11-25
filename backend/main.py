import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


HEARTBEAT_TIMEOUT = timedelta(seconds=60)
RUN_TRANSITIONS = {
    "run.started": ("assigned", "running"),
    "run.completed": ("running", "completed"),
    "run.failed": ("running", "failed"),
}


app = FastAPI(
    title="Communication Server",
    description="Central HTTP server for managing training runs",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


class WorkerRegistration(BaseModel):
    machine_id: str


workers = {}

runs_file = os.environ.get("TRAINING_RUNS_FILE", Path(__file__).with_name("test_runs.json"))

with open(runs_file, "r", encoding="utf-8") as file:
    runs = json.load(file)


def worker_activity(machine_id: str) -> str:
    if any(run["machine_id"] == machine_id and run["status"] == "running" for run in runs):
        return "busy"
    return "available"


@app.post("/workers/register")
async def register_worker(worker: WorkerRegistration):
    workers[worker.machine_id] = {
        "status": worker_activity(worker.machine_id),
        "last_seen": datetime.now(timezone.utc)
    }
    return {
        "machine_id": worker.machine_id,
        "status": "registered"
    }


class TrainingEvent(BaseModel):
    event: str
    run_id: str
    machine_id: str


@app.get("/workers")
async def get_workers():
    now = datetime.now(timezone.utc)

    for worker in workers.values():
        if now - worker["last_seen"] > HEARTBEAT_TIMEOUT:
            worker["status"] = "offline"

    return workers


@app.post("/workers/{machine_id}/heartbeat")
async def worker_heartbeat(machine_id: str):
    if machine_id not in workers:
        raise HTTPException(
            status_code=404,
            detail="Worker not registered"
        )

    worker = workers[machine_id]
    worker["last_seen"] = datetime.now(timezone.utc)

    worker["status"] = worker_activity(machine_id)

    return {
        "machine_id": machine_id,
        "status": worker["status"]
    }

@app.get("/workers/{machine_id}/runs")
async def get_assigned_runs(machine_id: str):
    if machine_id not in workers:
        raise HTTPException(
            status_code=404,
            detail="Worker not registered"
        )

    assigned_runs = [
        run for run in runs
        if run["machine_id"] == machine_id
        and run["status"] == "assigned"
    ]

    return assigned_runs


@app.post("/webhooks/training-events")
async def receive_training_event(event: TrainingEvent):
    transition = RUN_TRANSITIONS.get(event.event)
    if transition is None:
        raise HTTPException(
            status_code=400,
            detail="Unsupported event type"
        )

    if event.machine_id not in workers:
        raise HTTPException(
            status_code=404,
            detail="Worker not registered"
        )

    run = next(
        (run for run in runs if run["run_id"] == event.run_id),
        None
    )

    if run is None:
        raise HTTPException(
            status_code=404,
            detail="Run not found"
        )

    if run["machine_id"] != event.machine_id:
        raise HTTPException(
            status_code=403,
            detail="Run assigned to a different worker"
        )

    required_status, next_status = transition
    if run["status"] != required_status:
        raise HTTPException(
            status_code=409,
            detail=f"Run is not in {required_status} state"
        )

    run["status"] = next_status
    worker = workers[event.machine_id]
    if datetime.now(timezone.utc) - worker["last_seen"] > HEARTBEAT_TIMEOUT:
        worker["status"] = "offline"
    else:
        worker["status"] = worker_activity(event.machine_id)

    return {
        "run_id": event.run_id,
        "status": next_status
    }
