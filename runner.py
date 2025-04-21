import multiprocessing as mp
import os
import random
from multiprocessing import Manager, Pool, Process

import numpy as np
import openmc

from config import batch_size
from GA.constants import *
from GA.Individual import Individual
from utils import json_serializer


def random_param():
    r1 = int(random.uniform(*RANGES[1]))
    r2 = int(random.uniform(r1 + 5, 170))
    r3 = int(175)
    r4 = int(180)
    z4 = int(random.uniform(-400, -200))
    z1 = int(random.uniform(-1000, z4 - 225))
    z2 = int(random.uniform(z1 + 200, z4 - 25))
    z3 = int(random.uniform(z2 + 20, z4 - 5))
    z5 = int(random.uniform(z4 + 500, 400))
    z6 = int(random.uniform(z5 + 30, z5 + 100))
    z7 = int(random.uniform(z6 + 1500, 2600))
    z8 = int(random.uniform(z7 + 600, 3200))
    z9 = int(3600)
    return [r1, r2, r3, r4, z1, z2, z3, z4, z5, z6, z7, z8, z9]


def calculate_average_variance(tally):
    flux = tally.mean.ravel()
    flux_std = tally.std_dev.ravel()
    flux_var = flux_std**2
    for filter in tally.filters:
        if isinstance(filter, openmc.EnergyFilter):
            energies = filter.values
            break
    mid_energies = np.sqrt(energies[:-1] * energies[1:])
    total_flux = np.sum(flux)
    average_energy = np.sum(flux * mid_energies) / total_flux
    variance = np.sum((mid_energies - average_energy) ** 2 * flux_var) / total_flux**2
    return {"平均中子能量": average_energy, "方差": variance}


def calculate_fast_ratio(tal_fast, tal_total):
    fast_flux = np.sum(tal_fast.mean.ravel())
    total_flux = np.sum(tal_total.mean.ravel())
    return {"快中子通量": fast_flux, "总中子通量": total_flux, "快中子比例": fast_flux / total_flux}


def generate_statepoint(paramQueue, pathQueue):
    while True:
        param = paramQueue.get()
        if param is None:
            pathQueue.put(None)
            break
        ind = Individual(param)
        ind.run_model()
        pathQueue.put(ind.path)


def parse_statepoint(pathQueue):
    while True:
        path = pathQueue.get()
        if path is None:
            break
        with openmc.StatePoint(path + os.sep + f"statepoint.{batch_size}.h5") as sp:
            try:
                tal_1000 = sp.get_tally(name="新跑兔腔中子能谱 1000 groups")
                tal_shem361 = sp.get_tally(name="新跑兔腔中子能谱 SHEM-361")
                tal_vitamin282 = sp.get_tally(name="新跑兔腔中子能谱 VITAMIN-282")

                tal_fast = sp.get_tally(name="新跑兔快中子计数")
                tal_total = sp.get_tally(name="新跑兔总中子计数")
            except:
                raise ("Invalid tally name!")
            tally_info = {
                "能谱": {
                    "1000groups": calculate_average_variance(tal_1000),
                    "SHEM-361": calculate_average_variance(tal_shem361),
                    "VITAMIN-282": calculate_average_variance(tal_vitamin282),
                },
                "快中子": calculate_fast_ratio(tal_fast, tal_total),
            }
            json_serializer(tally_info, path + os.sep + "tally_info.txt")


if __name__ == "__main__":
    testSize = 6
    cpuNum = mp.cpu_count()  # 8

    with Manager() as manager:
        paramQueue, pathQueue = manager.Queue(), manager.Queue()

        for _ in range(testSize):
            paramQueue.put(random_param())
        paramQueue.put(None)

        parser = Process(target=parse_statepoint, args=(pathQueue,))
        parser.start()

        producer = Process(target=generate_statepoint, args=(paramQueue, pathQueue))
        producer.start()

        producer.join()
        parser.join()

    print(f"\n\nYou have {cpuNum} cpu(s) for this script")
    print(f"{testSize} data(s) has been generated")
