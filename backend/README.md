# HTTP communication server

## Setup

From the repository root, install the server dependencies once in your Python environment:

```
python -m pip install fastapi pydantic uvicorn
```

Start the server with the scheduler’s assignment file:

```sh
TRAINING_RUNS_FILE=scheduler/runs.json python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

For a quick test with the bundled sample, omit `TRAINING_RUNS_FILE=scheduler/runs.json`. Open `/health` to check the server or `/docs` to try the endpoints.

## How it works

1. The scheduler provides a JSON file of runs. Each assigned run has a `run_id`, a `machine_id`, and the status `assigned`.
2. The server loads the file at startup. Each worker registers and asks the server for runs assigned to its machine ID.

   ```sh
   python -m backend.worker_client --server-url "<server-url>" --machine-id "<machine-id>" --simulate
   ```

3. The worker reports when a run starts, completes, or fails. It sends a heartbeat every 20 seconds so the server can track which workers are online. The server keeps run updates in memory until it restarts.
