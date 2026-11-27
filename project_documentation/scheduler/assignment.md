
# assignment.py

- **File:** `scheduler/core/assignment.py`
- **Part of:** Scheduler
- **Workflow area:** Data collection
- **Author:** `Himaya` 

## What it does
Spreads the runs over the available machines, so each machine gets roughly the same amount of work.


## Where it fits
`runs.json` → assign_runs() → each machine runs its share with `Data_logger.py`
- **Input:** list of runs from `runs.json`and list of machine ID's
- **Output:** pair run - machine 

## How to run it
`assignment = assign_runs(runs, machine_ids=["A", "B", "C"])`

## Settings
Everything is passed in through agruments. 

## How it works
Hands out runs round-robin across the machines and avoids putting the same config on the same machine twice so that repetitions run on different hardware.

## Changed upstream code? *(only if you did)*
No. 

## Tested?
No automated testing implemented. 

## Known issues / TODO 



