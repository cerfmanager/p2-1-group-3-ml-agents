from contextlib import ExitStack
from unittest import TestCase
from unittest.mock import patch

from fastapi.testclient import TestClient

from backend import main


class TrainingEventTests(TestCase):
    def setUp(self):
        self.worker = "worker-a"
        runs = [
            {"run_id": "run-a", "machine_id": self.worker, "status": "assigned"},
            {"run_id": "run-b", "machine_id": self.worker, "status": "assigned"},
        ]
        stack = ExitStack()
        self.addCleanup(stack.close)
        stack.enter_context(patch.object(main, "runs", runs))
        stack.enter_context(patch.object(main, "workers", {}))
        self.client = stack.enter_context(TestClient(main.app))
        self.register(self.worker)

    def register(self, worker):
        self.client.post("/workers/register", json={"machine_id": worker}).raise_for_status()

    def event(self, event, run_id="run-a", worker=None):
        return self.client.post(
            "/webhooks/training-events",
            json={"event": event, "run_id": run_id, "machine_id": worker or self.worker},
        )

    def status(self):
        return self.client.get("/workers").json()[self.worker]["status"]

    def test_completion_and_failure_release_worker_after_last_active_run(self):
        self.event("run.started").raise_for_status()
        self.event("run.started", "run-b").raise_for_status()
        self.assertEqual(self.client.get(f"/workers/{self.worker}/runs").json(), [])
        completed = self.event("run.completed")
        completed.raise_for_status()
        self.assertEqual(completed.json(), {"run_id": "run-a", "status": "completed"})
        self.assertEqual(self.status(), "busy")
        failed = self.event("run.failed", "run-b")
        failed.raise_for_status()
        self.assertEqual(failed.json(), {"run_id": "run-b", "status": "failed"})
        self.assertEqual(self.status(), "available")

    def test_rejects_invalid_transitions_and_wrong_worker(self):
        self.register("worker-b")
        self.assertEqual(self.event("run.completed").status_code, 409)
        self.assertEqual(self.event("run.failed").status_code, 409)
        self.event("run.started").raise_for_status()
        self.assertEqual(self.event("run.started").status_code, 409)
        self.assertEqual(self.event("run.completed", worker="worker-b").status_code, 403)
        self.event("run.failed").raise_for_status()
        self.assertEqual(self.event("run.completed").status_code, 409)
        self.assertEqual(main.runs[0]["status"], "failed")

    def test_reconnecting_worker_stays_busy_until_run_finishes(self):
        self.event("run.started").raise_for_status()
        main.workers[self.worker]["last_seen"] -= main.HEARTBEAT_TIMEOUT
        self.assertEqual(self.status(), "offline")
        heartbeat = self.client.post(f"/workers/{self.worker}/heartbeat")
        self.assertEqual(heartbeat.json()["status"], "busy")
        self.register(self.worker)
        self.assertEqual(self.status(), "busy")
        main.workers[self.worker]["last_seen"] -= main.HEARTBEAT_TIMEOUT
        self.event("run.completed").raise_for_status()
        self.assertEqual(main.workers[self.worker]["status"], "offline")
        heartbeat = self.client.post(f"/workers/{self.worker}/heartbeat")
        self.assertEqual(heartbeat.json()["status"], "available")
