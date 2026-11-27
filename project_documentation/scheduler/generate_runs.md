
# generate_runs.py + experiment_config.json

- **File:** `scheduler/generate_runs.py`, `scheduler/experiment_config.json`
- **Part of:** Sheduler 
- **Workflow area:** Data collection
- **Author:** `Himaya` 

## What it does
Turns the experiment plan in `experiment_config.json` into a list of runs (`runs.json`) and creates the YAML config each run needs.

## Where it fits
`experiment_config.json` → generate_runs.py → (calls `yaml_generator.py`) → `runs.json` → `assign_runs()`
- **Input:** `scheduler/experiment_config.json`
- **Output:** `scheduler/runs.json` and the YAML files in `yamls/`

## How to run it
`python scheduler/generate_runs.py`

## Settings
In `experiment_config.json`:
- baseline hyperparameter values
- the grid: which values to try for each hyperparameter
- repetitions: how many times each config is run

## How it works
For each hyperparameter and each value in the grid, it runs `yaml_generator.py` as a separate process, then works out the generated file name itself and adds one entry to `runs.json` per repetition.

## Changed upstream code? *(only if you did)*
No.

## Tested?
No automated testing implemented. 

## Known issues / TODO 
- add `runs.json`to the `.gitignore`file. 


