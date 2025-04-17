import os

import openmc

from materials import *

colors = {
    H2O: (30, 144, 255),
    U: (75, 75, 75),
    UHZr: (85, 107, 47),
    UO2: (0, 100, 0),
    Al: (192, 192, 192),
    Al_pure: (230, 230, 250),
    Air: (135, 206, 235),
    Zr: (173, 216, 230),
    Graphite: (0, 0, 0),
    He: (240, 248, 255),
    SS: (128, 128, 128),
    B4C: (0, 0, 139),
    Pb: (47, 79, 79),
    AmO2_Be: (255, 69, 0),
    Cd: (70, 130, 180),
}
colors = {
    H2O: (0, 191, 255),  # 深水蓝
    U: (47, 79, 79),  # 深石板灰
    UHZr: (143, 151, 121),  # 哑光橄榄
    UO2: (128, 0, 128),  # 紫色
    Al: (169, 169, 169),  # 暗银灰
    Al_pure: (245, 245, 245),  # 极简白
    Air: (224, 255, 255),  # 淡青
    Zr: (70, 130, 180),  # 钢蓝
    Graphite: (54, 69, 79),  # 炭黑
    He: (240, 255, 255),  # 天青白
    SS: (105, 105, 105),  # 哑光灰
    B4C: (0, 0, 128),  # 海军蓝
    Pb: (112, 128, 144),  # 蓝灰
    AmO2_Be: (255, 0, 0),  # 纯红
    Cd: (30, 144, 255),  # 道奇蓝
}


def update_plots(dir = "./pics"):
    pl = openmc.Plot(name="整个堆芯xy")
    pl._basis = "xy"
    pl._color_by = "material"
    pl._colors = colors
    pl._filename = "core_xy"
    pl._origin = (0, 0, 0)
    pl._pixels = [5000, 5000]
    pl._width = [80.0, 80.0]

    pl2 = openmc.Plot(name="整个堆芯xz")
    pl2._basis = "xz"
    pl2._color_by = "material"
    pl2._colors = colors
    pl2._filename = "core_xz"
    pl2._origin = (0, 0, -10)
    pl2._pixels = [8500, 14000]
    pl2._width = [85.0, 140.0]

    pl4 = openmc.Plot(name="跑兔腔xy")
    pl4._basis = "xy"
    pl4._color_by = "material"
    pl4._colors = colors
    pl4._filename = "rab_xy"
    pl4._origin = (0, 0, 0)
    pl4._pixels = [2800, 2800]
    pl4._width = [4.5, 4.5]

    pl3 = openmc.Plot(name="跑兔腔xz")
    pl3._basis = "xz"
    pl3._color_by = "material"
    pl3._colors = colors
    pl3._filename = "rab_xz"
    pl3._origin = (0, 0, 15)
    pl3._pixels = [500, 5000]
    pl3._width = [5.0, 50.0]

    plots = [pl, pl2, pl3, pl4]
    for plot in plots:
        plot._filename = dir + os.sep +plot._filename
    pls = openmc.Plots(plots)
    pls.export_to_xml()
    openmc.plot_geometry()


if __name__ == "__main__":
    update_plots()
