import multiprocessing as mp
import random
from multiprocessing import Manager, Pool, Process

from GA.constants import *
from GA.Individual import Individual

testSize = 20
cpuNum = mp.cpu_count()
print(f"You have {cpuNum} cpu(s) for python")


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


def run_model(param):
    ind = Individual(param)
    # ind.run_model()
    print(f"run_model in {ind.path}...")
    return ind.path


def data_analyser(path):
    print(f"parse in {path}...")
    pass


def generate_statepoint(paramQueue):
    param = paramQueue.get()
    path = run_model(param)
    # pathQueue.put(path)
    return path


def parse_statepoint(pathQueue):
    while True:
        path = pathQueue.get()
        if path is None:
            break
        data_analyser(path)


if __name__ == "__main__":
    with Manager() as manager:
        paramQueue, pathQueue = manager.Queue(), manager.Queue()
        for _ in range(testSize):
            paramQueue.put(random_param())

        parser = Process(target=parse_statepoint, args=(pathQueue,))
        parser.start()

        with Pool() as producers:

            def callback(result):
                pathQueue.put(result)

            for _ in range(testSize):
                producers.apply_async(generate_statepoint, args=(paramQueue,), callback=callback)

            producers.close()
            producers.join()
        pathQueue.put(None)
        parser.join()

    print(f"{testSize} data(s) has been generated..")
