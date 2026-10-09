# Unity ML-Agents P1-2 — Intelligent Agents in 3D Environments

## Research Questions
How accurately can the training performance of an agent training run be predicted from its hyperparameters, algorithm and environment?

---

## Overview
This repository contains our work for Project 2.1 – AI and Machine Learning at Maastricht University.
Our goal is to apply Machine Learning (ML) techniques to data collected from Unity ML‑Agents, training intelligent agents in 3D real‑time simulations and analyzing their performance using supervised and unsupervised ML methods. 

---

## Project Objectives
1. Collect data from Unity ML‑Agents training runs.  
2. Analyze and model relationships between training parameters and outcomes (e.g., performance, duration, resource usage).  
3. Build a clean, well‑documented, reproducible pipeline for data collection and ML analysis.  
4. Maintain a public GitHub repository that demonstrates professional version control and documentation practices.

---

## Dungeon Escape Environment
Dungeon Escape is a multi-agent POCA-based Unity environment where agents must navigate a maze, avoid obstacles, and reach a goal.
It provides a controlled setting for studying how hyperparameters influence learning speed, stability, and final performance.

---

## Setup Instructions
### Requirements
- **Unity (2022.x or later)** — with ML‑Agents package installed  
- **Python 3.10.x** — recommended version 3.10.11  
- **Virtual environment** for Python dependencies  
- **Git** for version control

---

### Installation
1. Clone this repository:
` git clone https://github.com/<cerfmanager>/p2‑1‑group‑3‑ml‑agents.git `

2. Set up the Python environment:
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---
   
## Data Collection & ML Analysis
We collect data from training runs, including:
- hyperparameters (learning rate, batch size, buffer size, etc.)
- environment configuration (Dungeon Escape settings)
- performance metrics (reward curves, steps to threshold, training duration)
- hardware information (RAM, CPU, etc.)
Using this data, we train ML models to predict:
- training duration
- memory usage
- reward progression
- steps required to reach a predefined reward threshold

This work is inspired by literature on hyperparameter sensitivity, performance prediction, and surrogate modeling in DRL.

---

## Contributors
- Gabriela Linkova
- Alexandre Kozlowski
- Simona Dilovska
- Himaya Gunasekara
- Constantinos Lambrides
- Odhran O'reilly
- Matteo Ranieri

---

## References 
- Juliani et al. (2020). Unity: A general platform for intelligent agents. arXiv:1809.02627.
- Dierkes et al. (2025). Predicting Reinforcement Learning Performance.
- Parker-Holder et al. (2022). AutoRL: Automated Reinforcement Learning.
 
