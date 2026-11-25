import argparse
import logging
import subprocess
import sys
from pathlib import Path
from threading import Event, Thread

import httpx

REPO_ROOT = Path(__file__).resolve().parent.parent
HEARTBEAT_INTERVAL = 20


def register(server_url, machine_id):
    response = httpx.post(
        f"{server_url}/workers/register",
        json={"machine_id": machine_id}
    )
    response.raise_for_status()
    print("Registered:", response.json())


def send_heartbeat(server_url, machine_id):
    response = httpx.post(
        f"{server_url}/workers/{machine_id}/heartbeat"
    )
    response.raise_for_status()
    print("Heartbeat:", response.json())


def get_assigned_runs(server_url, machine_id):
    response = httpx.get(f"{server_url}/workers/{machine_id}/runs")
    response.raise_for_status()
    return response.json()


def report_event(server_url, machine_id, event, run_id):
    response = httpx.post(
        f"{server_url}/webhooks/training-events",
        json={"event": event, "run_id": run_id, "machine_id": machine_id},
    )
    response.raise_for_status()


def keep_heartbeats(stop, server_url, machine_id):
    while not stop.wait(HEARTBEAT_INTERVAL):
        try:
            send_heartbeat(server_url, machine_id)
        except httpx.HTTPError:
            logging.exception("Heartbeat failed")


def run_worker(server_url, machine_id, train=None):
    server_url = server_url.rstrip("/")
    register(server_url, machine_id)
    stop = Event()
    heartbeats = Thread(target=keep_heartbeats, args=(stop, server_url, machine_id))
    heartbeats.start()
    try:
        if train is None:
            stop.wait()
            return

        assigned = get_assigned_runs(server_url, machine_id)
        if not assigned:
            print("No assigned runs")
            return

        run = assigned[0]
        run_id = run["run_id"]
        report_event(server_url, machine_id, "run.started", run_id)
        try:
            train(run)
        except (Exception, KeyboardInterrupt):
            try:
                report_event(server_url, machine_id, "run.failed", run_id)
            except httpx.HTTPError:
                logging.exception("Could not report failure for %s", run_id)
            raise
        report_event(server_url, machine_id, "run.completed", run_id)
    finally:
        stop.set()
        heartbeats.join()


def collect_run_data(run):
    config = REPO_ROOT / run["yaml_file"]
    if not config.is_file():
        raise FileNotFoundError(f"Training config does not exist: {config}")

    run_id = run["run_id"]
    subprocess.run(
        [sys.executable, str(REPO_ROOT / "Data_logger.py"), str(config), "--run-id", run_id],
        cwd=REPO_ROOT,
        check=True,
    )

    csv_file = REPO_ROOT / "results" / run_id / "DungeonEscape" / "training_data.csv"
    if not csv_file.is_file():
        raise FileNotFoundError(f"Run finished without a training CSV: {csv_file}")
    print(f"Saved run data to {csv_file}")


def simulate_training(run):
    print(f"Simulating training for {run['run_id']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--server-url", required=True, help="Base URL of the communication server.")
    parser.add_argument("--machine-id", required=True, help="Worker ID used by the scheduler.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--collect-data",
        action="store_const",
        dest="trainer",
        const=collect_run_data,
        help="Run one assignment through the DungeonEscape CSV logger.",
    )
    mode.add_argument(
        "--simulate",
        action="store_const",
        dest="trainer",
        const=simulate_training,
        help="Process one assigned run with simulated training and report its completion.",
    )
    args = parser.parse_args()
    try:
        run_worker(args.server_url, args.machine_id, args.trainer)
    except KeyboardInterrupt:
        pass
