PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS pending_runs(
    run_id TEXT PRIMARY KEY,
    config_id TEXT NOT NULL,
    machine_id TEXT,
    repetition INTEGER NOT NULL,
    beta REAL NOT NULL,
    epsilon REAL NOT NULL,
    lambd REAL NOT NULL,
    strength REAL NOT NULL,
    gamma REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS running_runs(
    run_id TEXT PRIMARY KEY,
    config_id TEXT NOT NULL,
    machine_id TEXT,
    repetition INTEGER NOT NULL,
    beta REAL NOT NULL,
    epsilon REAL NOT NULL,
    lambd REAL NOT NULL,
    strength REAL NOT NULL,
    gamma REAL NOT NULL,
    started_at TEXT
);

CREATE TABLE IF NOT EXISTS completed_runs(
    run_id TEXT PRIMARY KEY,
    config_id TEXT NOT NULL,
    machine_id TEXT,
    repetition INTEGER NOT NULL,
    beta REAL NOT NULL,
    epsilon REAL NOT NULL,
    lambd REAL NOT NULL,
    strength REAL NOT NULL,
    gamma REAL NOT NULL,
    started_at TEXT,
    completed_at TEXT
);

CREATE TABLE IF NOT EXISTS failed_runs(
    run_id TEXT PRIMARY KEY,
    config_id TEXT NOT NULL,
    machine_id TEXT,
    repetition INTEGER NOT NULL,
    beta REAL NOT NULL,
    epsilon REAL NOT NULL,
    lambd REAL NOT NULL,
    strength REAL NOT NULL,
    gamma REAL NOT NULL,
    started_at TEXT,
    failed_at TEXT
);

CREATE VIEW all_runs AS SELECT
    run_id, config_id, machine_id, repetition, beta, epsilon, lambd, strength, gamma, 'pending' AS status
FROM pending_runs

UNION ALL
SELECT
    run_id, config_id, machine_id, repetition, beta, epsilon, lambd, strength, gamma, 'running' AS status
FROM running_runs
UNION ALL
SELECT
    run_id, config_id, machine_id, repetition, beta, epsilon, lambd, strength, gamma, 'completed' AS status
FROM completed_runs
UNION ALL
SELECT
    run_id, config_id, machine_id, repetition, beta, epsilon, lambd, strength, gamma, 'failed' AS status
FROM failed_runs;
    

