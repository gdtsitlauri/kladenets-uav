
# Proekt Kladenets

**Author:** George David Tsitlauri  
**Affiliation:** Dept. of Informatics & Telecommunications, University of Thessaly, Greece  
**Contact:** gdtsitlauri@gmail.com  
**Year:** 2026

**A Decentralized Dual-Use Cyber-Physical Architecture for Autonomous Swarms**

## Overview
Proekt Kladenets is a comprehensive, dual-use cyber-physical cognitive architecture for autonomous search and rescue (SAR) swarms operating in extreme disaster relief environments. This project is validated as a synthetic Proof-of-Concept (PoC), demonstrating how decentralized, low-cost edge AI swarms can outperform monolithic, high-cost legacy systems. All results are generated on affordable hardware (NVIDIA GTX 1650, 4GB VRAM) using only synthetic data and lightweight algorithms.

## Features
- **Edge Perception:** Post-training quantization (PTQ) and Leaky Integrate-and-Fire (LIF) spiking neural networks for efficient, robust perception.
- **Resilient Communications:** Cognitive radio (Q-learning), post-quantum cryptography, and orbital FSOC for secure, jam-resistant links.
- **Swarm Logic & Learning:** Artificial potential fields for deception, federated averaging for distributed learning.
- **Physics, Survival & XAI:** Extended Kalman Filter (EKF), Doppler detection, and explainable AI for robust navigation and human-in-the-loop safety.
- **Command, Control & Economics:** Unified dashboard, COTS hardware, and economic analysis (Asymmetric Cost-to-Deployment ratio).

## Directory Structure
- `src/` — Source code for all modules (perception, comms, swarm logic, physics, dashboard)
- `results/` — All simulation outputs, plots, and logs
- `paper/` — LaTeX paper, images, and references
- `.gitignore`, `LICENCE`, `README.md` — Project meta-files

## Quick Start
1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd Kladenets
   ```
2. (Optional) Create a Python virtual environment and install dependencies:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. Run simulations and generate results:
   ```bash
   python src/<module>/run_<module>.py
   ```
4. Compile the LaTeX paper:
   ```bash
   cd paper
   pdflatex kladenets-uav.tex
   ```

## Requirements
- Python 3.8+
- PyTorch, NumPy, Matplotlib, Streamlit, cryptography
- LaTeX (for compiling the paper)

## Academic Paper
The full methodology, equations, results, and references are documented in `paper/kladenets-uav.tex`. All references are inlined for portability. The paper explicitly clarifies the synthetic PoC nature of the results for academic transparency.

## License
This project is licensed under the MIT License. See `LICENCE` for details.

## Author
George David Tsitlauri  
Department of Informatics and Telecommunications, University of Thessaly

---

For questions or contributions, open an issue or contact the author at gdtsitlauri@gmail.com.

## Citation

```bibtex
@misc{tsitlauri2026kladenets,
  author = {George David Tsitlauri},
  title  = {Proekt Kladenets: A Decentralized Dual-Use Cyber-Physical Architecture for Autonomous Swarms},
  year   = {2026},
  institution = {University of Thessaly},
  email  = {gdtsitlauri@gmail.com}
}
```
