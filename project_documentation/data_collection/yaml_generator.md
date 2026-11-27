
# yaml_generator.py

- **File:** `yaml_generator.py`
- **Part of:** Scheduler
- **Workflow area:** Data collection
- **Author:** Created by:`Constantinos`, updated by `Himaya`

## What it does
Writes a DungeonEscape training config that is the same as the baseline except for one hyperparameter.

## Where it fits
Called by `generate_runs.py` for each value in the experiment grid.
- **Input:** one command line flag with the value to change
- **Output:** `yamls/DungeonEscape_<param>_<value>.yaml`, in a `yamls/` folder

## How to run it
(example): `python yaml_generator.py --beta 0.01`

## Settings
- `PATH_TO_YAMLS`: output folder, `<folder of yaml_generator.py>/yamls`
- Baseline values: hard-coded in the script
- `summary_freq: 60000` and the rest of the config are written out in full in an f-string (`mod_file`) inside the script.

## How it works
1. Checks the arguments, then picks the hyperparameter with a `match` statement. Each `case` sets its variable to the new value and sets `changed_param` (used also in the file name).
2. Fills the new value into the full YAML text (`mod_file`), with the baseline values for everything else.
3. Writes it to `PATH_TO_YAMLS / f"DungeonEscape_{changed_param}_{value}.yaml"`.

## Changed upstream code? *(only if you did)*
No.

## Tested?
No automated testing implemented.

## Known issues / TODO 



