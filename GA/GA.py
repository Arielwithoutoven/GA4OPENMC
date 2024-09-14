import random
import time

from constants import *
from Individual import Individual


class GA:
    def __init__(self):
        self.curPop = [None] * POPSIZE
        self.nexPop = [None] * POPSIZE
        self.starTime = time.time()
        self.parFronts = set()
        self.pool = 1

    def initialize(self):
        # 随机生成初始个体
        for _ in range(POPSIZE):
            r1 = int(random.uniform(*RRANGE[1]))
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
            self.curPop[_] = Individual(
                [r1, r2, r3, r4, z1, z2, z3, z4, z5, z6, z7, z8, z9]
            )

    def calFit(self):
        # TODO 考虑使用多进程加速
        for ind in self.cur_pop:
            ind.calFit()

    def sort(self):
        # 非支配排序
        pass

    def crossover(self):
        pass

    def mutation(self):
        # TODO 考虑使用多线程加速
        for ind in self.nexPop:
            ind.mutation()

    def replacement(self):
        pass

    def run(self):
        self.initialize()
        self.calFit()
        self.sort()
        for gen in range(GENSIZE):
            print("第%d次迭代" % gen)
            self.crossover()
            self.mutation()
            self.calFit()
            self.sort()
            self.replacement()
