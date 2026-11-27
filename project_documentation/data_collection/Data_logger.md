
# Data_logger.py

- **File:** `Data_logger.py`
- **Part of:** Our machines / CSV results
- **Workflow area:** Data collection
- **Author:** `Constantinos` 

## What it does
Runs a normal `mlagents-learn` training session for DungeonEscape and logs the training data to a CSV file at the same time.

## Where it fits
Last step of the pipeline: `generate_runs.py` → `assign_runs()` → Data_logger.py → CSV
- **Input:** a training config YAML from `yamls/` (made by `yaml_generator.py`)
- **Output:** `results/<run-id>/DungeonEscape/training_data.csv`, plus the usual ML-Agents results (checkpoints, TensorBoard logs)

## How to run it


## Settings
CSV columns: `beta, epsilon, lambda, strength, gamma, runtime` (header)

## How it works
- Wraps `mlagents-learn` (`ml-agents/mlagents/trainers/learn.py`) instead of changing it.
- Patches `POCATrainer._update_policy` so it can read the hyperparameters at each policy update.
- Hooks into `StatsReporter` (`ml-agents/mlagents/trainers/stats.py`) with its own stats writer, which skips resets so they don't end up as rows.
- Note that an ML-Agents update that renames these functions will break it.

## Changed upstream code? *(only if you did)*
No.

## Tested?
No automated testing implemented.

## Known issues / TODO 
- Might be an issue with row ordering (to look into)

