# Artificial-life-simulation
GPU based Artificial Life simulation engine running 1,000,000 mutating life forms in real time with Taichi.

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

