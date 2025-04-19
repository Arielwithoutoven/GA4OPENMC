import os

import numpy as np
import openmc

batch_size = 500

space = openmc.stats.Box(
    lower_left=[-11.9, 0.0, -19.5],
    upper_right=[13.9, 0.0, 19.5],
    only_fissionable=True,
)  # spatial sites should only be accepted if they occur in fissionable materials
source = openmc.IndependentSource(space=space, particle="neutron", strength=1.0)


settings_fixed_source = openmc.Settings(
    run_mode="fixed source",
    particles=100000,
    batches=batch_size,
    source=source,
)

settings = openmc.Settings(
    run_mode="eigenvalue",
    batches=batch_size,
    generations_per_batch=10,
    particles=20000,
    inactive=50,
)

# test_use
# settings = openmc.Settings(
#     run_mode="eigenvalue",
#     batches=batch_size,
#     generations_per_batch=10,
#     particles=20,
#     inactive=5,
# )


# 减少不必要的运行开销但是内存消耗变多
energies = np.logspace(np.log10(1e-5), np.log10(20.0e6), 1001)  # 1000个能量网格
energy1000Fil = openmc.EnergyFilter(energies)
shem361Fil = openmc.EnergyFilter.from_group_structure("SHEM-361")
vitamin282Fil = openmc.EnergyFilter.from_group_structure("VITAMIN-J-175")
fastFil = openmc.EnergyFilter([0.1e6, 20e6])

mesh = openmc.RegularMesh(name="Core Mesh")
mesh.dimension = [50, 50]  # 网格数，也可以是三维的
mesh.upper_right = [35, 35]
mesh.lower_left = [-35, -35]
meshFil = openmc.MeshFilter(mesh)  # 基于网格的Filter

tal2 = openmc.Tally(name="全堆中子通量")
tal2.filters = [meshFil, energy1000Fil]
tal2.scores = ["flux"]


def update_tallies(cell):
    cellFil = openmc.CellFilter(cell)

    tal_1000 = openmc.Tally(name="新跑兔腔中子能谱 1000 groups")
    tal_1000.filters = [cellFil, energy1000Fil]
    tal_1000.scores = ["flux"]

    # print(openmc.mgxs.GROUP_STRUCTURES.keys()) # 可用的能群计算方式
    tal_shem361 = openmc.Tally(name="新跑兔腔中子能谱 SHEM-361")
    tal_shem361.filters = [cellFil, shem361Fil]
    tal_shem361.scores = ["flux"]

    tal_vitamin282 = openmc.Tally(name="新跑兔腔中子能谱 VITAMIN-282")
    tal_vitamin282.filters = [cellFil, vitamin282Fil]
    tal_vitamin282.scores = ["flux"]

    tal_fast = openmc.Tally(name="新跑兔快中子计数")
    tal_fast.filters = [fastFil, cellFil]
    tal_fast.scores = ["flux"]

    tal_total = openmc.Tally(name="新跑兔总中子计数")
    tal_total.filters = [cellFil]
    tal_total.scores = ["flux"]

    trigger = openmc.Trigger(trigger_type="std_dev", threshold=1e-5)
    trigger.scores = ["flux"]

    return openmc.Tallies([tal_1000, tal_shem361, tal_vitamin282, tal_fast, tal_total])
