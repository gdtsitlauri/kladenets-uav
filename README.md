# Proekt Kladenets

**A Dual-Use Synthetic Research Platform for Autonomous Swarm Coordination**


Proekt Kladenets is a simulation-heavy cyber-physical research repository that combines swarm coordination, edge AI perception, resilient communications, basic cryptographic messaging, explainability, and command-and-control visualization. The repository is best understood as a synthetic proof-of-concept platform rather than a deployment-validated UAV system.


## Project Metadata

| Field | Value |
| --- | --- |
| Author | George David Tsitlauri |
| Affiliation | Dept. of Informatics & Telecommunications, University of Thessaly, Greece |
| Contact | gdtsitlauri@gmail.com |
| Year | 2026 |

## Evidence Status

| Item | Current status |
| --- | --- |
| Multi-module simulation code | Present |
| Committed result artifacts (`.txt`, `.npy`, `.png`) | Present |
| Low-cost / constrained-hardware experiments | Present in selected modules |
| Real flight or hardware-in-the-loop validation | Not present |
| Broad superiority claims over operational systems | Not supported |

## Research Positioning

The strongest credible claim supported by the repository is:

> Proekt Kladenets demonstrates a broad synthetic architecture for decentralized autonomous-swarm research, with committed artifacts across perception, communications, tracking, and command logic, but it remains a proof-of-concept simulation platform rather than an operationally validated UAV system.

## What Exists

Examples of committed artifacts include:

- `results/ilya_muromets_bench.txt` with local perception benchmark output
- `results/dobrynya_rewards.txt` with Q-learning reward traces
- `results/vasilisa_xai_iff.txt` with human-in-the-loop override evidence
- multiple `.png` and `.npy` simulation outputs for trajectory, spoofing, and line-of-sight scenarios

## Main Modules

| Module family | Purpose |
| --- | --- |
| Perception | lightweight model / spiking-style perception experiments |
| Communications | Q-learning radio behavior, FSOC, cryptographic messaging |
| Swarm logic | role allocation, decoy/striker simulation, federated updates |
| Navigation and survival | EKF-style tracking, spoofing response, trigger logic |
| XAI / command | explanation and dashboard-oriented outputs |

## Result Interpretation

- The repository contains real artifact files rather than empty claims.
- Most evidence is synthetic and module-level.
- Some modules show simple but concrete local benchmarks, such as the `0.0587 s / 100 runs` FP32 perception benchmark in `results/ilya_muromets_bench.txt`.
- The repository should therefore be described as broad and technically interesting, but not as a field-validated swarm platform.

## Repository Layout

```text
src/
results/
paper/
README.md
.gitignore
LICENSE
```

## Reproducibility

```bash
pip install -r requirements.txt
python src/<module>/run_<module>.py
```

Paper source:

```bash
cd paper
pdflatex kladenets-uav.tex
```

## Limitations

- Evaluation is simulation-only.
- The repository spans many subsystems, which reduces evidential depth per subsystem.
- Hardware, radio, and airframe validation remain future work.

## Why Kladenets Can Still Be Strong

Kladenets is strongest when treated as a synthetic swarm-systems platform:

- many modules already produce real artifacts,
- the repo covers perception, comms, navigation, and explanation together,
- and its breadth is architectural rather than decorative.

The right upgrade path is to keep that synthetic integration identity and deepen
selected task slices later, not to pretend it is already a field-tested UAV
stack.


