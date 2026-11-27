# Repository Structure

## Top-level overview

```
<repo root>/
├── Data_logger.py                  [OURS] Training wrapper that writes a CSV
├── yaml_generator.py               [OURS] Generates a training config with one hyperparameter changed
├── scheduler/                      [OURS] Experiment planning and run assignment
├── project_docs/                   [OURS] Team documentation (you are here)
│
├── docs/                           Upstream ML-Agents docs (+ our Readme.md)
├── config/                         Training configs + tool configs
├── tests/                          Test setup and requirements
│
├── ml-agents/                      Python trainers (mlagents-learn)
├── ml-agents-envs/                 Python ↔ Unity communication layer
├── ml-agents-trainer-plugin/       Example custom trainer plugin
├── ml-agents-plugin-examples/      Example plugins
│
├── com.unity.ml-agents/            Unity C# package
├── com.unity.ml-agents.extensions/ Extra Unity C# features
├── Project/                        Unity project with the example environments
├── DevProject/                     Unity project used for upstream development
├── PerformanceProject/             Unity project used for upstream benchmarks
│
├── protobuf-definitions/           gRPC messages (Unity ↔ Python)
├── localized_docs/                 Translated docs
├── colab/                          Jupyter notebook tutorials
├── utils/                          Upstream maintenance scripts
├── unity-volume/                   Docker mount point
│
├── .github/  .yamato/              CI configuration
└── Dockerfile, LICENSE.md, CODE_OF_CONDUCT.md, .pre-commit-config.yaml, .editorconfig, .gitignore
```

---

## Our code in detail

```
├── Data_logger.py                  [OURS] Wraps mlagents-learn for DungeonEscape (POCA).
│                                     Hooks into POCATrainer._update_policy and StatsReporter,
│                                     writes results/<run-id>/DungeonEscape/training_data.csv
│
├── yaml_generator.py               [OURS] CLI: python yaml_generator.py --<param> <value>
│                                     params: --beta --epsilon --lambda --strength --gamma
│                                     writes yamls/DungeonEscape_<param>_<value>.yaml
│
├── scheduler/                      [OURS]
│   ├── experiment_config.json        Baseline hyperparameters, the value grid per parameter, repetitions
│   ├── generate_runs.py              Reads the config, calls yaml_generator.py, writes scheduler/runs.json
│   └── core/
│       ├── __init__.py
│       └── assignment.py             assign_runs(runs, machine_ids): balances runs across machines,
│                                     avoiding running the same config twice on one machine
│
├── project_docs/                   [OURS]
│   ├── TEMPLATE.md                   Template for documenting new code
│   ├── phase2-workflow.md            Phase 2 review/documentation workflow
│   ├── repo-structure.md             This file
│   └── architecture/
│       └── system-architecture.puml  Planned system architecture (GUI, server, scheduler, machines)
│
└── docs/Readme.md                  [OURS] Project README (research question, setup)
```

**Generated at runtime:** `yamls/`, `scheduler/runs.json`, `results/`

### Pipeline

```
experiment_config.json
        │
        ▼
generate_runs.py ──calls──▶ yaml_generator.py ──▶ yamls/*.yaml
        │
        ▼
runs.json ──▶ assign_runs() ──▶ machines run Data_logger.py <yaml> ──▶ training_data.csv
```

---

## Upstream ML-Agents in detail

### Python

```
ml-agents/mlagents/
├── trainers/
│   ├── learn.py                    Entry point for `mlagents-learn` (Data_logger.py uses it)
│   ├── trainer_controller.py       Main training loop
│   ├── settings.py                 Parses the YAML config into settings objects
│   ├── stats.py                    StatsReporter / StatsWriter (Data_logger.py hooks in here)
│   ├── poca/                       POCA trainer (used by DungeonEscape)
│   ├── ppo/  sac/                  Other trainers
│   ├── ghost/                      Self-play
│   ├── optimizer/  policy/  torch_entities/   Neural network and optimisation code
│   ├── model_saver/                Checkpoints / ONNX export
│   └── tests/
└── plugins/                        Trainer plugin system

ml-agents-envs/mlagents_envs/       Low-level Python API to talk to Unity
├── environment.py                  UnityEnvironment
├── base_env.py                     Core interfaces
├── side_channel/                   Extra Unity ↔ Python messaging
├── communicator_objects/           Generated protobuf classes
└── envs/                           Gym / PettingZoo wrappers
```

### Unity / C#

```
com.unity.ml-agents/
├── Runtime/                        Agent, Academy, sensors, actuators, inference
├── Editor/                         Unity editor tooling
├── Tests/                          C# tests
├── Plugins/                        Native/managed dependencies (e.g. gRPC, protobuf)
└── Documentation~/

com.unity.ml-agents.extensions/     Extra sensors and Input System integration

Project/
├── Assets/ML-Agents/Examples/
│   ├── DungeonEscape/              ← OUR ENVIRONMENT
│   │   └── Scripts/
│   │       ├── DungeonEscapeEnvController.cs   Episode/group logic and rewards
│   │       ├── PushAgentEscape.cs              Agent behaviour
│   │       └── SimpleNPC.cs                    Dragon NPC
│   ├── 3DBall/ Basic/ Crawler/ PushBlock/ Soccer/ Walker/ … (other examples)
│   └── SharedAssets/
├── Packages/
└── ProjectSettings/
```

### Configuration and tooling

```
config/
├── poca/DungeonEscape.yaml         Upstream config for our environment (our generator's base)
├── poca/  ppo/  sac/  imitation/   Training configs for all example environments
├── setup.cfg  pytest.ini           Tool configs (moved here from the root by our team)
└── mkdocs.yml                      Builds the docs website

tests/                              conftest.py, test_requirements.txt, test_constraints_version.txt
utils/                              Upstream scripts: validate versions/links/meta files, generate docs
protobuf-definitions/               .proto files + make.sh / make_for_win.bat to regenerate
.github/                            GitHub Actions workflows, issue/PR templates
.yamato/                            Unity's internal CI (unused by us)
```

### Documentation

```
project_documentation/                            
├── template.md          Template for the documentation 
├── repo-structure.md    This file 
│
├── architecture/
│   └──  graph.puml      Graph structure of the project
│
├── data_collection/
├── scheduler/
├── agent_changes/
├── prediction_model/
├── server/
└── gui/
```

