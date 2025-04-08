"""r1~r4, z1~z9, to make them change but still in order"""

import random
import sys
from functools import wraps

import matplotlib.pyplot as plt
import numpy as np

from GA.constants import *
from GA.utils import *
from geometry import update_geometry
from materials import materials
from config import update_tallies, settings

# print(sys.path) #只有当前文件所在目录的绝对路径和环境变量
# sys.path.append("..")  # 在GA文件夹使用python执行本文件调用Py内模块方法时可用
# sys.path.append(".")  # 在Py文件夹使用python执行本文件调用Py内模块方法时可用
# isort: split
import geometry  # 按照执行python时的路径查找

# from MultiProcess import Process, Pool

cwd = os.getcwd()


class Individual:
    def __init__(self, p=[None]):
        self.p = p
        self.gene = [self.p[_] - RANGES[_][0] for _ in range(D)]
        self.fit = [None] * OBJSIZE  # TODO 非支配算法fit使用何类型
        self.rank = 0
        self.distans = 0.0
        self.survive = True
        self.path = os.getcwd() + os.sep + "Individuals" + os.sep + timestr()
        self.geometry, self.cell = update_geometry(self.p)
        self.tallies = update_tallies(self.cell)
        os.makedirs(self.path)

    def survive_check(func):
        @wraps(func)
        def within(*args, **kwargs):
            if not args[0].survive:
                raise ("Ciruis: Dead Individual should not %s!" % func.__name__.upper())
            return func(*args, **kwargs)

        return within

    @survive_check
    def update_gene(self):
        self.gene = [self.p[_] - RANGES[_][0] for _ in range(D)]

    @survive_check
    def clone(self):
        return Individual(self.p)  # 是值传递

    @survive_check
    def mutation(self):
        for i, gene in enumerate(self.p):
            # 记录当前值和取值下界的差
            a = self.p[i] - RANGES[i][0]
            if a < 0:
                raise ("Ciruis: Para Out Of Expected Range!")
            else:
                b = bin(a)[2:]
            # print(a,b)
            s = GENELENS
            for x in range(s):
                if random.random() < PM:
                    try:
                        # 从右往左遍历，若是'1'则减去1<<i,若是'0'则加上1<<i
                        a += int(
                            ((1 << x) - ("1" == b[-x - 1]) * (1 << (x + 1))) * (s - x) / s
                        )  # 加权处理，不希望高位比特变化导致变异过大
                    except IndexError:
                        # 若遍历结束说明前置位都是省略了的'0'，都加上1<<i
                        a += 1 << x
                    finally:
                        pass
                        # print(bin(a), a)
                # print(self.p[i])
            if a < 0 or a > WIDTHS[i]:
                self.survive = False
                # print(a, b, RANGES[i], "寄")
                break
            self.p[i] = RANGES[i][0] + a
            # print(self.p[i])
        self.update_gene()

    @survive_check
    def __and__(self, Ind2):  # pylint: disable=C0103
        # 重载&算子作为交叉算子
        chi1 = self.clone()
        chi2 = Ind2.clone()
        gOrd1 = 0  # current gene order
        gLen1 = GENELENS[gOrd1]  # current gene length
        gOrd2 = -1  # last gene order
        odd = True

        for point in range(sum(GENELENS)):
            if random.random() < CM:
                odd ^= 1  # 取非
                while point >= gLen1:
                    gOrd1 += 1
                    gLen1 += GENELENS[gOrd1]
                ii = gLen1 - point
                # print(gOrd1, ii)
                tail1 = chi1.g[gOrd1] - (chi1.g[gOrd1] >> ii << ii)
                tail2 = chi2.g[gOrd1] - (chi2.g[gOrd1] >> ii << ii)
                chi1.g[gOrd1] = (chi1.g[gOrd1] >> ii << ii) + tail2
                chi2.g[gOrd1] = (chi2.g[gOrd1] >> ii << ii) + tail1

                if odd:
                    for gOrd in range(gOrd2 + 1, gOrd1):
                        chi1.g[gOrd], chi2.g[gOrd] = chi2.g[gOrd], chi1.g[gOrd]
                    if not gOrd2 == gOrd1:
                        chi1.g[gOrd1], chi2.g[gOrd1] = chi2.g[gOrd1], chi1.g[gOrd1]
                else:
                    gOrd2 = gOrd1

        if not odd:
            for gOrd in range(gOrd1 + 1, D):
                chi1.g[gOrd], chi2.g[gOrd] = chi2.g[gOrd], chi1.g[gOrd]

        if (np.array(chi1.g) >= 0).all() and (np.array([chi1.p[i] - RANGES[i][1] for i in range(D)]) <= 0).all():
            chi1.p = [chi1.g[i] + RANGES[i][0] for i in range(D)]
        else:
            chi1.survive = False

        if (np.array(chi2.g) >= 0).all() and (np.array([chi2.p[i] - RANGES[i][1] for i in range(D)]) <= 0).all():
            chi2.p = [chi2.g[i] + RANGES[i][0] for i in range(D)]
        else:
            chi2.survive = False

        return chi1, chi2

    @survive_check
    def __rand__(self, Ind2):
        # 重载&算子，作为交叉算子
        return Ind2.__and__(self)

    def __repr__(self):
        print(self.p)
        s = ""
        for i in range(D):
            s += "0" * (GENELENS[i] - len(bin(self.gene[i])[2:])) + bin(self.gene[i])[2:] + " "
        print(s, "\n")

    @survive_check
    def cal_fit(self):
        path = os.getcwd() + os.sep + "Individuals" + os.sep + timestr()
        os.makedirs(path)
        geometry.update(self.p, geodir=path + os.sep)

        pass
        return [None] * OBJSIZE

    def run_model(self):
        model = openmc.Model(self.geometry, materials, settings, self.tallies)
        model.run(cwd=self.path)

if __name__ == "__main__":
    a = Individual([133, 160, 175, 180, -600, -400, -300, -250, 150, 350, 2000, 3000, 3600])
    b = Individual([120, 130, 175, 180, -700, -300, -275, -265, 200, 250, 2200, 2940, 3600])
