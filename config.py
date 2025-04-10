import openmc

from geometry import *
import numpy as np


space = openmc.stats.Box(
    lower_left=[-11.9, 0.0, -19.5],
    upper_right=[13.9, 0.0, 19.5],
    only_fissionable=True,
)  # spatial sites should only be accepted if they occur in fissionable materials
source = openmc.IndependentSource(space=space, particle="neutron", strength=1.0)

settings = openmc.Settings(
    run_mode="eigenvalue",
    batches=250,
    particles=100000,
    inactive=50,
    source=source,
)


def update_tallies(cell):
    mesh = openmc.RegularMesh(name="Core Mesh")
    mesh.dimension = [50, 50]  # 网格数，也可以是三维的
    mesh.upper_right = [35, 35]
    mesh.lower_left = [-35, -35]

    meshFil = openmc.MeshFilter(mesh)  # 基于网格的Filter

    cellFil = openmc.CellFilter(cell)
    energies = np.logspace(np.log10(1e-5), np.log10(20.0e6), 1001)  # 1000个能量网格
    energyFil = openmc.EnergyFilter(energies)

    tal1 = openmc.Tally(name="跑兔腔中子谱 手动")
    tal1.filters = [cellFil, energyFil]
    tal1.scores = ["flux"]

    tal2 = openmc.Tally(name="堆芯中子通量和裂变")
    tal2.filters = [meshFil, energyFil]
    tal2.scores = ["flux", "fission"]

    # print(openmc.mgxs.GROUP_STRUCTURES.keys()) # 可用的能群计算方式
    energies_shem = openmc.mgxs.GROUP_STRUCTURES["SHEM-361"]
    shem_fil = openmc.EnergyFilter(energies_shem)
    tal_shem = openmc.Tally(name="跑兔腔中子谱 SHEM-361")
    tal_shem.filters = [cellFil, shem_fil]
    tal_shem.scores = ["flux"]

    trigger = openmc.Trigger(trigger_type="std_dev", threshold=5e-5)
    trigger.scores = ["absorption"]

    return openmc.Tallies([tal1, tal_shem])
