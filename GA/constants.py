"""
定义了 GA 运算需要用到的常量，供 GA 文件夹内的子模块调用
"""

POPSIZE = 50  # 种群数（考虑13-3个优化参数，这个种群数有点少）
GENSIZE = 20  # 最大迭代次数
# BINSIZE = 12  # 编码长度（弃置，每个基因有自己的编码长度）
PC = 1  # 交叉概率
PM = 0.05  # 突变概率
OBJSIZE = 13  # 目标函数个数

# [1.2, 1.3, 1.75, 1.8]
# [-7., -3., -2.75, -2.65, 2., 2.5, 22., 29.4, 36.06]

# r4=r3+5=180;
# r1>=120;
# r3>=r2+5>=r1+10
# 1. Check r1 in [120, 165]
# 2. Check r2 in [r1+5, 170]

# -1000 <= z1 <= z2 - 200
# z2 <= z3 - 20
# z3 <= z4 - 5
# z4 <= min{z5-500,0}&& |z4+z5|<=100 # 保证样品室在堆芯居中处
# z5 <= z6 - 30
# z6 <= z7 - 1500
# z7 <= z8 - 600
# z8 <= z9 - 400
# z9 = 3600
# 1. z4 in [-400, -200]
# 2. z1 in [-1000, z4-225]
# 3. z2 in [z1+200, z4-25]
# 4. z3 in [z2+20, z4-5]
# 5. z5 in [z4+500, 400]
# 6. z6 in [z5+30, z5+100]
# 7. z7 in [z6+1500, 2600]
# 8. z8 in [z7+600, 3200]
# 9. z9 = 3600
RANGES = [
    [120, 165],
    [125, 170],
    [175, 175],
    [180, 180],
    [-1000, -425],
    [-800, -225],
    (-780, -205),
    (-400, -200),
    (100, 400),
    (130, 500),
    (1600, 2600),
    (2200, 3200),
    (3600, 3600),
]
D = len(RANGES)
WIDTHS = [t[1] - t[0] for t in RANGES]
GENELENS = [len(bin(t)) - 2 for t in WIDTHS]

CM = D / sum(GENELENS)
# 优化目标暂定为：
# 1.中子通量高
# 2.快中子（暂定为E>0.1MeV的中子）比例大
# 3.反应性在1±0.005以内

# 最好保证
# 快中子达到10e12-10e13 n/cm2/s
# 平均能量达到1.2MeV以上
# 空间不小于直径25mm*高度50mm
# 不确定度<20%

if __name__ == "__main__":
    print(RANGES)
    print(WIDTHS)
    print(GENELENS)
    print(CM)
