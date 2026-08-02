import taichi as ti
import time
import math
import numpy as np
import matplotlib.pyplot as plt

ti.init(arch=ti.cuda)

# ====================
# 1. STRUCT DEFINITIONS
# ====================
animal_variables = ti.types.struct(
    # --- Subsystem F: Metadata & Bitmask (32-bit) ---
    agent_id=ti.i32,
    species_id=ti.i32,
    parent_id=ti.i32,
    bitmask_flags=ti.u32,

    # --- Subsystem A & E: Spatial Coordinates & Memory (16-bit) ---
    grid_x=ti.i16,
    grid_y=ti.i16,
    vel_x=ti.f16,
    vel_y=ti.f16,
    acc_x=ti.f16,
    acc_y=ti.f16,
    mem_food_grid_x=ti.i16,
    mem_food_grid_y=ti.i16,
    mem_threat_grid_x=ti.i16,
    mem_threat_grid_y=ti.i16,
    mem_home_grid_x=ti.i16,
    mem_home_grid_y=ti.i16,

    # --- Subsystem A: Sub-pixel Kinematics (8-bit) ---
    sub_x=ti.u8,
    sub_y=ti.u8,

    # --- Subsystem B: Physical Vitals & Homeostasis (8-bit) ---
    energy=ti.u8,
    max_energy=ti.u8,
    health=ti.u8,
    hydration=ti.u8,
    stamina=ti.u8,
    body_temp=ti.u8,
    toxicity=ti.u8,
    age=ti.u8,
    immune_strength=ti.u8,
    pathogen_load=ti.u8,

    # --- Subsystem C: Drive Deficits (8-bit) ---
    drive_hunger=ti.u8,
    drive_thirst=ti.u8,
    drive_fear=ti.u8,
    drive_rest=ti.u8,
    drive_mating=ti.u8,
    drive_social=ti.u8,
    drive_aggression=ti.u8,
    drive_thermo=ti.u8,
    drive_curiosity=ti.u8,
    drive_dominance=ti.u8,

    # --- Subsystem D: Mutable Genetics & Phenotypes (8-bit) ---
    gene_max_speed=ti.u8,
    gene_size=ti.u8,
    gene_perception_rad=ti.u8,
    gene_perception_fov=ti.u8,
    gene_diet_spectrum=ti.u8,
    gene_base_metabolism=ti.u8,
    gene_digestion_eff=ti.u8,
    gene_sanguivore=ti.u8,
    gene_detritivore=ti.u8,
    gene_camouflage=ti.u8,
    gene_armor=ti.u8,
    gene_attack_power=ti.u8,
    gene_venom=ti.u8,
    gene_repro_threshold=ti.u8,
    gene_litter_size=ti.u8,
    gene_mutation_rate=ti.u8,
    gene_swarm_inclination=ti.u8,
    gene_thermo_tolerance=ti.u8,
    gene_color_r=ti.u8,
    gene_color_g=ti.u8,
    gene_color_b=ti.u8,
    gene_lifespan=ti.u8,
    gene_sleep_cycle=ti.u8,
    gene_tool_aptitude=ti.u8,
    gene_pheromone_emit=ti.u8,

    # --- Subsystem E: Social Rank & Markers (8-bit) ---
    social_rank=ti.u8,
    pheromone_marker=ti.u8
)

plant_variables = ti.types.struct(
    plant_flags=ti.u32,
    grid_x=ti.i16,
    grid_y=ti.i16,
    biomass=ti.u8,
    max_biomass=ti.u8,
    plant_type=ti.u8,
    growth_rate=ti.u8,
    toxicity_level=ti.u8,
    spread_radius=ti.u8,
    soil_req_fert=ti.u8,
    water_consumption=ti.u8
)

pathogen_variables = ti.types.struct(
    strain_id=ti.i32,
    disease_flags=ti.u32,
    virulence=ti.u8,
    lethality=ti.u8,
    mutation_rate=ti.u8,
    incubation_time=ti.u8,
    transmission_type=ti.u8,
    target_host_diet=ti.u8,
    recovery_rate=ti.u8,
    stamina_drain=ti.u8,
    mutation_vector=ti.u8,
    persistence=ti.u8,
    immune_evasion=ti.u8
)

# ===============================
# 2. MAP & SPATIAL GRID CONSTANTS
# ===============================
map_size = 65536
tile_size = 128
n_tiles = map_size // tile_size  # 512 cells per axis

MAX_ANIMALS = 300_000

# VRAM Allocation

animals = ti.Struct.field(animal_variables.members, shape=MAX_ANIMALS)

cell_bin = ti.field(dtype=ti.i32, shape=(n_tiles, n_tiles))

# ======================
# 3. SPATIAL GRID KERNELS
# ======================

# Clear grid count at start of frame
@ti.kernel
def clear_cell_bin():
    for gx, gy in cell_bin:
        cell_bin[gx, gy] = 0

# Scatter animals to spatial grid using atomic add

@ti.kernel
def scatter_animals_to_grid():
    for i in animals:
        
        # Check if animal is active
        
        if (animals[i].bitmask_flags & 1) != 0:
            
            # Map world coordinates to tile bin
            
            gx = ti.cast(animals[i].grid_x // tile_size, ti.i32)
            gy = ti.cast(animals[i].grid_y // tile_size, ti.i32)
            
            # Boundary clamp safety
            
            if 0 <= gx < n_tiles and 0 <= gy < n_tiles:
                ti.atomic_add(cell_bin[gx, gy], 1)

print("Engine initialized successfully!")
