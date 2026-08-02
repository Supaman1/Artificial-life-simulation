# 🧬 ALife-GPU: High-Throughput Artificial Life Simulation Engine

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Backend: Taichi GPU](https://img.shields.io/badge/Backend-Taichi%20GPU%20%2F%20CUDA-red.svg)](https://www.taichi-lang.org/)

A massively parallel, GPU-accelerated **Artificial Life (ALife) Simulation Engine** built in Python using **Taichi**. The engine simulates up to **1,200,000+ active entities** (Animals, Plants, and Pathogens) in real-time by running spatial partitioning, drive-reduction utility AI, Reynolds steering kinematics, and evolutionary genetic algorithms directly on VRAM.

---

## ⚡ Key Features

* **Data-Oriented ECS Architecture:** Memory-aligned structs (32-bit $\rightarrow$ 16-bit $\rightarrow$ 8-bit quantization) engineered to maximize GPU L1/L2 cache locality and preserve VRAM memory bandwidth.
* **$O(N)$ Spatial Hash Grid:** Eliminates $O(N^2)$ distance bottlenecks, allowing 300,000+ agents to evaluate local perception neighborhoods in parallel.
* **Drive-Reduction Utility AI:** Fast, deficit-driven decision engine (Hunger, Thirst, Fear, Mating, Rest, Social) controlling real-time agent state transitions.
* **Reynolds Kinematic Steering:** Smooth, vector-based movement (Seek, Flee, Wander, Swarm) backed by sub-pixel precision.
* **Weighted Tier Mutation Engine:** Genetic transmission model supporting micro-adjustments ($85\%$), environmental adaptations ($14\%$), and macro speciation events ($1\%$).
* **Closed-Loop Ecosystem Thermodynamics:** First-law energy conservation loop where animal corpses decompose into fertilizer, driving plant growth and pathogen vectoring.
* **Level-Of-Detail (LOD) Renderer:** Seamless camera transition from high-density point clouds (zoomed out) to procedural phenotype entity views (zoomed in) using Taichi GGUI.

---

## 🏛️ System Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│                       MAIN GPU LOOP                         │
└──────────────────────────────┬──────────────────────────────┘
                               │
       ┌───────────────────────┼───────────────────────┐
       ▼                       ▼                       ▼
┌───────────────┐       ┌───────────────┐       ┌───────────────┐
│ Spatial Grid  │  ──►  │ Vitals & AI   │  ──►  │ Steering &    │
│ Reconstruction│       │ Homeostasis   │       │ Movement      │
└───────────────┘       └───────────────┘       └───────────────┘
                                                       │
       ┌───────────────────────────────────────────────┘
       ▼
┌───────────────┐       ┌───────────────┐       ┌───────────────┐
│ Mutation &    │  ──►  │ Closed-Loop   │  ──►  │ Taichi GGUI   │
│ Reproduction  │       │ Environment   │       │ Render Pass   │
└───────────────┘       └───────────────┘       └───────────────┘

```

## 📊 Memory Layout & VRAM Allocation
To prevent hardware memory padding gaps, all entity structs are strictly ordered by byte-width alignment:

| Entity Buffer | Max Capacity | Footprint / Entity | Total VRAM Allocation |
|---|---|---|---|
| Animal Field | 300,000 Agents | 85 Bytes | ~25.5 MB |
| Plant Field | 1,000,000 Nodes | 16 Bytes | ~16.0 MB |
| Pathogen Field | 10,000 Strains | 20 Bytes | ~0.20 MB |
## 📁 Repository Structure

```
alife-gpu-engine/
├── README.md               # Project documentation
├── requirements.txt        # Dependencies (taichi, numpy)
└── main.py                 # the whole code is in this just run this

```

## 🚀 Getting Started
Prerequisites
 * Python: Version 3.8 or higher
   
 * GPU Hardware: NVIDIA GPU with CUDA support (or Apple Silicon / Vulkan-compatible GPU)
Installation

 * Clone the repository:
   git clone [https://github.com/YOUR_USERNAME/alife-gpu-engine.git](https://github.com/YOUR_USERNAME/alife-gpu-engine.git)
cd alife-gpu-engine

 * Create a virtual environment (Optional but recommended):
   python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

 * Install dependencies:
   pip install -r requirements.txt

 * Run the simulation:
   python main.py

⌨️ Controls & Navigation
| Input | Action |
|---|---|
| Mouse Wheel | Zoom In / Out (Toggles between Point Cloud & Entity LOD view) |
| Left Click + Drag | Pan Camera across world coordinates |
| Spacebar | Pause / Resume Simulation Loop |
| R Key | Reset World State & Re-initialize VRAM |
📜 License
Distributed under the MIT License. See LICENSE for more information.

