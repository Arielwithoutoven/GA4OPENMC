import openmc
from mat_no_tem import *
from math import pi

############################################################################
#堆芯外围曲面
fir_Al_ins = openmc.ZCylinder(x0=0, y0=0, r=34.9, name='第1层Al筒内径')
fir_Al_out = openmc.ZCylinder(x0=0, y0=0, r=36.1, name='第1层Al筒外径')
sec_H2O_out = openmc.ZCylinder(x0=0, y0=0, r=36.7, name='第2层H2O外径')
thi_Al_out = openmc.ZCylinder(x0=0, y0=0, r=37.5, name='第3层Al筒外径')
fou_Pb_out = openmc.ZCylinder(x0=0, y0=0, r=40.0, name='第4层Pb外径')
fif_Al_out = openmc.ZCylinder(x0=0, y0=0, r=40.8, name='第5层Al外径')
six_H2O_out = openmc.ZCylinder(x0=0, y0=0, r=60.0, name='最外围H2O外径', boundary_type='vacuum')

H2O_low = openmc.ZPlane(z0=-100.0, name='下层水面', boundary_type='vacuum')
core_low = openmc.ZPlane(z0=-35.5, name='堆芯下平面')
core_upp = openmc.ZPlane(z0=35.5, name='堆芯上平面')
H2O_upp = openmc.ZPlane(z0=100.0, name='上层水面', boundary_type='vacuum')

#堆芯外围栅元
#fir_Al_inner = openmc.Cell(name='堆芯筒体内', region=-fir_Al_ins & +H2O_low & -H2O_upp) # replaced by ins_reactor
fir_Al = openmc.Cell(name='第1层Al', fill=Al_pure, region=+fir_Al_ins & -fir_Al_out & +core_low & -core_upp)
sec_H2O = openmc.Cell(name='第2层H2O', fill=H2O, region=+fir_Al_out & -sec_H2O_out & +core_low & -core_upp)
thi_Al = openmc.Cell(name='第3层Al', fill=Al_pure, region=+sec_H2O_out & -thi_Al_out & +core_low & -core_upp)
fou_Pb = openmc.Cell(name='第4层Pb', fill=Pb, region=+thi_Al_out & -fou_Pb_out & +core_low & -core_upp)
fif_Al = openmc.Cell(name='第5层Al', fill=Al_pure, region=+fou_Pb_out & -fif_Al_out & +core_low & -core_upp)
six_H2O = openmc.Cell(name='最外围H2O', fill=H2O, region=(+fif_Al_out & -six_H2O_out & +core_low & -core_upp) | (+fir_Al_ins & -six_H2O_out & +core_upp & -H2O_upp) | (+fir_Al_ins & -six_H2O_out & -core_low & +H2O_low))


############################################################################
#无限水栅元
inf_H2O = openmc.Cell(name='无限水栅元', fill=H2O)

#无限水Universe
H2OUni = openmc.Universe(name='无限水栅元', cells=[inf_H2O])


############################################################################
#燃料棒栅元曲面
fuelRod_Zr_out = openmc.ZCylinder(r=0.23, name='Zr芯外径')
fuelRod_core_out = openmc.ZCylinder(r=1.805, name='燃料芯外径')
fuelRod_He_out = openmc.ZCylinder(r=1.81, name='燃料棒He气外径')
fuelRod_clad_out = openmc.ZCylinder(r=1.86, name='燃料棒包壳外径')

fuelRod_clad_low = openmc.ZPlane(z0=-30.7, name='燃料包壳底部')
fuelRod_lower_graphite_low = openmc.ZPlane(z0=-29.25, name='燃料棒下侧石墨底部')
fuelRod_core_low = openmc.ZPlane(z0=-19.5, name='燃料芯底部')
fuelRod_core_upp = openmc.ZPlane(z0=19.5, name='燃料芯顶部')
fuelRod_upper_graphite_upp = openmc.ZPlane(z0=29.1, name='燃料棒上侧石墨顶部')
fuelRod_clad_upp = openmc.ZPlane(z0=30.7, name='燃料包壳顶部')

#燃料棒栅元
f_Zr_core = openmc.Cell(name='Zr芯', fill=Zr, region=-fuelRod_Zr_out & +fuelRod_core_low & -fuelRod_core_upp)
f_fuel_core = openmc.Cell(name='燃料芯', fill=UHZr, region=+fuelRod_Zr_out & -fuelRod_core_out & +fuelRod_core_low & -fuelRod_core_upp)
f_He = openmc.Cell(name='He气隙', fill=He, region=+fuelRod_core_out & -fuelRod_He_out & +fuelRod_core_low & -fuelRod_core_upp)
f_graphite_upp = openmc.Cell(name='上石墨', fill=Graphite, region=-fuelRod_He_out & +fuelRod_core_upp & -fuelRod_upper_graphite_upp)
f_graphite_low = openmc.Cell(name='下石墨', fill=Graphite, region=-fuelRod_He_out & +fuelRod_lower_graphite_low & -fuelRod_core_low)
f_SS_side = openmc.Cell(name='包壳侧', fill=SS, region=+fuelRod_He_out & -fuelRod_clad_out & +fuelRod_lower_graphite_low & -fuelRod_upper_graphite_upp)
f_SS_upp = openmc.Cell(name='包壳上', fill=SS, region=-fuelRod_clad_out & +fuelRod_upper_graphite_upp & -fuelRod_clad_upp)
f_SS_low = openmc.Cell(name='包壳下', fill=SS, region=-fuelRod_clad_out & +fuelRod_clad_low & -fuelRod_lower_graphite_low)
f_H2O_around = openmc.Cell(name='外侧水', fill=H2O, region= +fuelRod_clad_out | -fuelRod_clad_low | +fuelRod_clad_upp)  # TODO Check it!

#燃料棒Universe
fuelUni = openmc.Universe(name="燃料棒", cells=[f_Zr_core, f_fuel_core, f_He, f_graphite_upp, f_graphite_low, f_SS_side, f_SS_upp, f_SS_low, f_H2O_around])


############################################################################
#不锈钢栅元曲面
#和燃料棒栅元曲面复用

#不锈钢栅元
s_SS_core = openmc.Cell(name='不锈钢芯', fill=SS, region=-fuelRod_core_out & +fuelRod_core_low & -fuelRod_core_upp)
s_He = openmc.Cell(name='He气隙', fill=He, region=+fuelRod_core_out & -fuelRod_He_out & +fuelRod_core_low & -fuelRod_core_upp)
s_upper_Al = openmc.Cell(name='上Al', fill=Al, region=-fuelRod_He_out & +fuelRod_core_upp & -fuelRod_upper_graphite_upp)
s_lower_Al = openmc.Cell(name='下Al', fill=Al, region=-fuelRod_He_out & +fuelRod_lower_graphite_low & -fuelRod_core_low)
s_side_clad = openmc.Cell(name='包壳侧', fill=SS, region=+fuelRod_He_out & -fuelRod_clad_out & +fuelRod_lower_graphite_low & -fuelRod_upper_graphite_upp)
s_upper_clad = openmc.Cell(name='包壳上', fill=SS, region=-fuelRod_clad_out & +fuelRod_upper_graphite_upp & -fuelRod_clad_upp)
s_lower_clad = openmc.Cell(name='包壳下', fill=SS, region=-fuelRod_clad_out & +fuelRod_clad_low & -fuelRod_lower_graphite_low)
s_H2O_around = openmc.Cell(name='外侧水', fill=H2O, region= +fuelRod_clad_out | -fuelRod_clad_low | +fuelRod_clad_upp)

#不锈钢棒Universe
SSUni = openmc.Universe(name="不锈钢棒", cells=[s_SS_core, s_He, s_upper_Al, s_lower_Al, s_side_clad, s_upper_clad, s_lower_clad, s_H2O_around])


############################################################################
#石墨栅元曲面
graphiteRod_graphite_out = openmc.ZCylinder(r=1.7, name='石墨芯外径')
graphiteRod_He_out = openmc.ZCylinder(r=1.75, name='石墨棒He气外径')
graphiteRod_clad_out = openmc.ZCylinder(r=1.85, name='石墨棒包壳外径')

graphiteRod_clad_low = openmc.ZPlane(z0=-30.7, name='石墨棒包壳底部')
graphiteRod_graphite_low = openmc.ZPlane(z0=-29.25, name='石墨棒下侧石墨底部')
graphiteRod_graphite_upp = openmc.ZPlane(z0=29.25, name='石墨棒上侧石墨顶部')
graphiteRod_clad_upp = openmc.ZPlane(z0=30.7, name='石墨棒包壳顶部')

#石墨栅元
g_graphite_core = openmc.Cell(name='石墨芯', fill=Graphite, region=-graphiteRod_graphite_out & +graphiteRod_graphite_low & -graphiteRod_graphite_upp)
g_He = openmc.Cell(name='He气隙', fill=He, region=+graphiteRod_graphite_out & -graphiteRod_He_out & +graphiteRod_graphite_low & -graphiteRod_graphite_upp)
g_Al_side = openmc.Cell(name='Al包壳侧', fill=Al, region=+graphiteRod_He_out & -graphiteRod_clad_out & +graphiteRod_graphite_low & -graphiteRod_graphite_upp)
g_Al_upp = openmc.Cell(name='Al包壳顶部', fill=Al, region=-graphiteRod_clad_out & +graphiteRod_graphite_upp & -graphiteRod_clad_upp)
g_Al_low = openmc.Cell(name='Al包壳底部', fill=Al, region=-graphiteRod_clad_out & +graphiteRod_clad_low & -graphiteRod_graphite_low)
g_H2O_around = openmc.Cell(name='外侧水', fill=H2O, region=+graphiteRod_clad_out | -graphiteRod_clad_low | +graphiteRod_clad_upp)

#石墨栅元Universe
graphiteUni = openmc.Universe(name="石墨棒", cells=[g_graphite_core, g_He, g_Al_side, g_Al_upp, g_Al_low, g_H2O_around])


############################################################################
#带燃料跟随体的控制棒栅元曲面
controlRod_Zr_out= fuelRod_Zr_out.clone()
controlRod_core_out= fuelRod_core_out.clone()
controlRod_He_out= fuelRod_He_out.clone()
controlRod_clad_out=fuelRod_clad_out.clone()
controlRod_B4C_out = openmc.ZCylinder(r=1.785, name='控制棒B4C芯外径')

controlRod_clad_low = openmc.ZPlane(z0=-74.75, name='控制棒包壳底部')
controlRod_lower_graphite_low = openmc.ZPlane(z0=-72.5, name='控制棒下侧石墨底部')
controlRod_fuelCore_low = openmc.ZPlane(z0=-58.5, name='控制棒燃料芯底部')
controlRod_B4C_low = openmc.ZPlane(z0=-19.5, name='控制棒B4C底部')
controlRod_upper_graphite_low = openmc.ZPlane(z0=19.5, name='控制棒上侧石墨底部')
controlRod_upper_graphite_upp = openmc.ZPlane(z0=35.5, name='控制棒上侧石墨顶部')
controlRod_clad_upp = openmc.ZPlane(z0=37.75, name='控制棒包壳顶部')

#带燃料跟随体的控制棒栅元
c_Zr_core = openmc.Cell(name='Zr芯', fill=Zr, region=-controlRod_Zr_out & +controlRod_fuelCore_low & -controlRod_B4C_low)
c_fuel_core = openmc.Cell(name='燃料芯', fill=UHZr, region=+controlRod_Zr_out & -controlRod_core_out & +controlRod_fuelCore_low & -controlRod_B4C_low)
c_He_UHZr = openmc.Cell(name='UHZr周围He气隙', fill=He, region=+controlRod_core_out & -controlRod_He_out & +controlRod_fuelCore_low & -controlRod_B4C_low)
c_B4C = openmc.Cell(name='B4C', fill=B4C, region=-controlRod_B4C_out & +controlRod_B4C_low & -controlRod_upper_graphite_low)
c_He_B4C = openmc.Cell(name='B4C周围He气隙', fill=He, region=+controlRod_B4C_out & -controlRod_He_out & +controlRod_B4C_low & -controlRod_upper_graphite_low)
c_graphite_upp = openmc.Cell(name='上石墨', fill=Graphite, region=-controlRod_He_out & +controlRod_upper_graphite_low & -controlRod_upper_graphite_upp)
c_graphite_low = openmc.Cell(name='下石墨', fill=Graphite, region=-controlRod_He_out & +controlRod_lower_graphite_low & -controlRod_fuelCore_low)
c_SS_side = openmc.Cell(name='包壳侧', fill=SS, region=+controlRod_He_out & -controlRod_clad_out & +controlRod_lower_graphite_low & -controlRod_upper_graphite_upp)
c_SS_upp = openmc.Cell(name='包壳上', fill=SS, region=-controlRod_clad_out & +controlRod_upper_graphite_upp & -controlRod_clad_upp)
c_SS_low = openmc.Cell(name='包壳下', fill=SS, region=-controlRod_clad_out & +controlRod_clad_low & -controlRod_lower_graphite_low)
c_H2O_around = openmc.Cell(name='外侧水', fill=H2O, region= +controlRod_clad_out | -controlRod_clad_low | +controlRod_clad_upp)

#带燃料跟随体的控制棒Universe
controlUni = openmc.Universe(name="控制棒", cells=[c_Zr_core, c_fuel_core, c_He_UHZr, c_B4C, c_He_B4C, c_graphite_upp, c_graphite_low, c_SS_side, c_SS_upp, c_SS_low, c_H2O_around])


############################################################################
#脉冲棒栅元曲面
pulseRod_B4C_out = openmc.ZCylinder(r=1.485, name='脉冲棒B4C芯外径')
pulseRod_Air_out = openmc.ZCylinder(r=1.51, name='脉冲棒Air外径')
pulseRod_clad_out = openmc.ZCylinder(r=1.56, name='脉冲棒包壳外径')

pulseRod_clad_low = openmc.ZPlane(z0=-76.05, name='脉冲棒包壳底部')
pulseRod_lower_air_low = openmc.ZPlane(z0=-74.1, name='脉冲棒下侧空气底部')
pulseRod_B4C_low = openmc.ZPlane(z0=-19.5, name='脉冲棒B4C芯底部')
pulseRod_B4C_upp = openmc.ZPlane(z0=19.5, name='脉冲棒B4C芯顶部')
pulseRod_upper_air_upp = openmc.ZPlane(z0=34.5, name='脉冲棒上侧空气顶部')
pulseRod_clad_upp = openmc.ZPlane(z0=36.45, name='脉冲棒包壳顶部')

#脉冲棒栅元
p_B4C_core = openmc.Cell(name='B4C芯', fill=B4C, region=-pulseRod_B4C_out & +pulseRod_B4C_low & -pulseRod_B4C_upp)
p_Air_side = openmc.Cell(name='Air侧', fill=Air, region=+pulseRod_B4C_out & -pulseRod_Air_out & +pulseRod_B4C_low & -pulseRod_B4C_upp)
p_Air_upp = openmc.Cell(name='Air上', fill=Air, region=-pulseRod_Air_out& +pulseRod_B4C_upp & -pulseRod_upper_air_upp)
p_Air_low = openmc.Cell(name='Air下', fill=Air, region=-pulseRod_Air_out& +pulseRod_lower_air_low & -pulseRod_B4C_low)
p_SS_side = openmc.Cell(name='包壳侧', fill=SS, region=+pulseRod_Air_out & -pulseRod_clad_out & +pulseRod_lower_air_low & -pulseRod_upper_air_upp)
p_SS_upp = openmc.Cell(name='包壳顶部', fill=SS, region=-pulseRod_clad_out & +pulseRod_upper_air_upp & -pulseRod_clad_upp)
p_SS_low = openmc.Cell(name='包壳底部', fill=SS, region=-pulseRod_clad_out & +pulseRod_clad_low & -pulseRod_lower_air_low)
p_H2O_around = openmc.Cell(name='外侧水', fill=H2O, region=+pulseRod_clad_out | -pulseRod_clad_low | +pulseRod_clad_upp)

#脉冲棒栅元Universe
pulseRodUni = openmc.Universe(name="脉冲棒", cells=[p_B4C_core, p_Air_side, p_Air_upp, p_Air_low, p_SS_side, p_SS_upp, p_SS_low, p_H2O_around])


############################################################################
#A1 A2 B1 B2 D M 控制棒Universe
controlRod_unit = openmc.ZCylinder(r=4, name='控制棒构造单元')
A1_Rod = openmc.Cell(name='A1 Rod', fill=controlUni, region=-controlRod_unit)
A1_Rod._translation=[0,0,39]#A k~1 position
#A1_Rod._translation=[0,0,10]#Test position
A1Uni = openmc.Universe(name="A1棒", cells=[A1_Rod])
A2_Rod = openmc.Cell(name='A2 Rod', fill=controlUni, region=-controlRod_unit)
A2_Rod._translation=[0,0,39]#A k~1 position
#A2_Rod._translation=[0,0,10]#Test position
A2Uni = openmc.Universe(name="A2棒", cells=[A2_Rod])
B1_Rod = openmc.Cell(name='B1 Rod', fill=controlUni, region=-controlRod_unit)
B1_Rod._translation=[0,0,10]
B1Uni = openmc.Universe(name="B1棒", cells=[B1_Rod])
B2_Rod = openmc.Cell(name='B2 Rod', fill=controlUni, region=-controlRod_unit)
B2_Rod._translation=[0,0,10]
B2Uni = openmc.Universe(name="B2棒", cells=[B2_Rod])
D_Rod = openmc.Cell(name='D Rod', fill=controlUni, region=-controlRod_unit)
D_Rod._translation=[0,0,15]
DUni = openmc.Universe(name="D棒", cells=[D_Rod])
M_Rod = openmc.Cell(name='M Rod', fill=pulseRodUni, region=-controlRod_unit)
M_Rod._translation=[0,0,0]
MUni = openmc.Universe(name="M棒", cells=[M_Rod])


############################################################################
#AmO2-Be中子源栅元曲面
neuSource_source_out = openmc.ZCylinder(r=0.8, name='中子源源外径')
neuSource_source_packing_out = openmc.ZCylinder(r=1.55, name='中子源源包装外径')
neuSource_clad_out = openmc.ZCylinder(r=1.8, name='中子源包壳外径')

neuSource_clad_low = openmc.ZPlane(z0=-36.03, name='中子源包壳底部')
neuSource_lower_air_low = openmc.ZPlane(z0=-29.4, name='中子源下侧空气底部')
neuSource_source_packing_low = openmc.ZPlane(z0=-2.55, name='中子源源包装底部')
neuSource_source_low = openmc.ZPlane(z0=-1.35, name='中子源源底部')
neuSource_source_upp = openmc.ZPlane(z0=1.65, name='中子源源顶部')
neuSource_source_packing_upp = openmc.ZPlane(z0=2.55, name='中子源源包装顶部')
neuSource_upper_air_upp = openmc.ZPlane(z0=29.4, name='中子源上侧空气顶部')
neuSource_clad_upp = openmc.ZPlane(z0=36.03, name='中子源包壳顶部')

#中子源栅元
n_AmO2_Be = openmc.Cell(name='中子源', fill=AmO2_Be, region=-neuSource_source_out & +neuSource_source_low & -neuSource_source_upp)
n_packing_side = openmc.Cell(name='源外包装侧', fill=SS, region=+neuSource_source_out & -neuSource_source_packing_out & +neuSource_source_low & -neuSource_source_upp)
n_packing_upp = openmc.Cell(name='源外包装上', fill=SS, region=-neuSource_source_packing_out & +neuSource_source_upp & -neuSource_source_packing_upp)
n_packing_low = openmc.Cell(name='源外包装下', fill=SS, region=-neuSource_source_packing_out & +neuSource_source_packing_low & -neuSource_source_low)
n_Air_upp = openmc.Cell(name='Air上', fill=Air, region=-neuSource_source_packing_out & +neuSource_source_packing_upp & -neuSource_upper_air_upp)
n_Air_low = openmc.Cell(name='Air下', fill=Air, region=-neuSource_source_packing_out & +neuSource_lower_air_low & -neuSource_source_packing_low)
n_SS_side = openmc.Cell(name='包壳侧', fill=SS, region=+neuSource_source_packing_out & -neuSource_clad_out & +neuSource_lower_air_low & -neuSource_upper_air_upp)
n_SS_upp = openmc.Cell(name='包壳顶部', fill=SS, region=-neuSource_clad_out & +neuSource_upper_air_upp & -neuSource_clad_upp)
n_SS_low = openmc.Cell(name='包壳底部', fill=SS, region=-neuSource_clad_out & +neuSource_clad_low & -neuSource_lower_air_low)
n_H2O_around = openmc.Cell(name='外侧水', fill=H2O, region=+neuSource_clad_out | -neuSource_clad_low | +neuSource_clad_upp)

#中子源Universe
neuSourceUni = openmc.Universe(name="中子源", cells=[n_AmO2_Be, n_packing_side, n_packing_upp, n_packing_low, n_Air_upp, n_Air_low, n_SS_side, n_SS_upp, n_SS_low, n_H2O_around])


############################################################################
#原跑兔栅元曲面
runRabbit_pipe_ins = openmc.ZCylinder(r=1.75, name='跑兔管内径')
runRabbit_pipe_out = openmc.ZCylinder(r=1.8, name='跑兔管外径')

runRabbit_low = openmc.ZPlane(z0=-36.03, name='跑兔管底部')
runRabbit_upp = openmc.ZPlane(z0=36.03, name='跑兔管顶部')

#原跑兔栅元
r_Air = openmc.Cell(name='管内空气', fill=Air, region=-runRabbit_pipe_ins&+runRabbit_low&-runRabbit_upp)
r_SS = openmc.Cell(name='管', fill=SS, region=+runRabbit_pipe_ins&-runRabbit_pipe_out&+runRabbit_low&-runRabbit_upp)
r_H2O_around = openmc.Cell(name='外侧水', fill=H2O, region=+runRabbit_pipe_out|-runRabbit_low|+runRabbit_upp)

#原跑兔Universe
runRabbitUni= openmc.Universe(name="跑兔管", cells=[r_Air, r_SS, r_H2O_around])


############################################################################
#新中央跑兔栅元曲面
def update(p=[170,180,205,210,-700, -300, -275, -265, 200, 250, 2200, 2940, 3600], geodir='./', mat=None): # TODO 是否优化材料
    newRabbit_Air_out = openmc.ZCylinder(r=p[0]/100, name='跑兔管内空气半径')
    newRabbit_Cd_out = openmc.ZCylinder(r=p[1]/100, name='跑兔管内屏蔽层外径')
    newRabbit_fuel_out = openmc.ZCylinder(r=p[2]/100, name='跑兔管燃料外径')
    newRabbit_clad_out = openmc.ZCylinder(r=p[3]/100, name='跑兔管包壳外径')

    newRabbit_lower_clad_low = openmc.ZPlane(z0=p[4]/100, name='下clad底部')
    newRabbit_lower_clad_upp = openmc.ZPlane(z0=p[5]/100, name='下clad顶部')
    newRabbit_fuel_upp = openmc.ZPlane(z0=p[6]/100, name='U顶部')
    newRabbit_Cd_upp = openmc.ZPlane(z0=p[7]/100, name='Cd顶部')
    newRabbit_Cd_side_upp = openmc.ZPlane(z0=p[8]/100, name='周围Cd顶部')
    newRabbit_lid_upp = openmc.ZPlane(z0=p[9]/100, name='Cd盖顶部')
    newRabbit_Cd_clad_upp = openmc.ZPlane(z0=p[10]/100, name='Cd上包层顶部')
    newRabbit_upper_clad_low = openmc.ZPlane(z0=p[11]/100, name='上clad底部')
    newRabbit_upper_clad_upp = openmc.ZPlane(z0=p[12]/100, name='上clad顶部')

    #TEST GLOBAL !!!!!!!!!!!!
    global n_r_lower_Air
#新中央跑兔栅元
    mat1=SS
    n_r_side_clad = openmc.Cell(name="外部包壳", fill=mat1, region=+newRabbit_fuel_out & -newRabbit_clad_out & +newRabbit_lower_clad_upp & -newRabbit_upper_clad_low)
    n_r_upper_clad = openmc.Cell(name="上部包壳", fill=mat1, region=-newRabbit_clad_out & +newRabbit_upper_clad_low & -newRabbit_upper_clad_upp)
    n_r_lower_clad = openmc.Cell(name="下部包壳", fill=mat1, region=-newRabbit_clad_out & +newRabbit_lower_clad_low & -newRabbit_lower_clad_upp)
    mat2=Air
    n_r_upper_Air = openmc.Cell(name="上部Air", fill=mat2, region=-newRabbit_Air_out & +newRabbit_lid_upp & -newRabbit_upper_clad_low)
    n_r_lower_Air = openmc.Cell(name="下部Air", fill=mat2, region=-newRabbit_Air_out & +newRabbit_Cd_upp & -newRabbit_Cd_side_upp)
    mat3=Cd
    n_r_lid = openmc.Cell(name="盖", fill=Air, region=-newRabbit_Air_out & +newRabbit_Cd_side_upp &-newRabbit_lid_upp) # TODO CHECK这里把Cd盖改为了Air
    n_r_bottom_Cd = openmc.Cell(name="Cd包层底", fill=mat3, region=-newRabbit_Cd_out & +newRabbit_fuel_upp & -newRabbit_Cd_upp)
    n_r_side_Cd = openmc.Cell(name="Cd包层side", fill=mat3, region=+newRabbit_Air_out & -newRabbit_Cd_out & +newRabbit_Cd_upp & -newRabbit_Cd_side_upp)
    mat4=Cd
    n_r_upper_Cd = openmc.Cell(name="Cd上包层", fill=mat4, region=+newRabbit_Air_out & -newRabbit_fuel_out & +newRabbit_Cd_side_upp & -newRabbit_Cd_clad_upp)
    mat5=UO2
    n_r_bottom_fuel = openmc.Cell(name="燃料底", fill=mat5, region=-newRabbit_fuel_out & +newRabbit_lower_clad_upp & -newRabbit_fuel_upp)
    n_r_side_fuel = openmc.Cell(name="燃料side", fill=mat5, region=+newRabbit_Cd_out & -newRabbit_fuel_out & +newRabbit_fuel_upp & -newRabbit_Cd_side_upp)
    mat6=SS
    n_r_upper_Al = openmc.Cell(name="Al上包层", fill=mat6, region=+newRabbit_Air_out & -newRabbit_fuel_out & +newRabbit_Cd_clad_upp & -newRabbit_upper_clad_low)
    n_r_H2O_around = openmc.Cell(name='外侧水', fill=H2O, region=+newRabbit_upper_clad_upp|-newRabbit_lower_clad_low|+newRabbit_clad_out)
    
    n_r_bottom_fuel.volume =pi*(p[2]/100)*(p[2]/100)*(p[6]/100-p[5]/100)
    n_r_side_fuel.volume =pi*((p[2]/100)*(p[2]/100)-(p[1]/100)*(p[1]/100))*(p[8]/100-p[6]/100)
    #Cd体积 =pi*(p[1]/100)*(p[1]/100)*(p[7]/100-p[6]/100)+pi*((p[1]/100)*(p[1]/100)-(p[0]/100)*(p[0]/100))*(p[8]/100-p[7]/100)
    print("UO2 Volume:", n_r_bottom_fuel.volume+n_r_side_fuel.volume, "cm3")
    print("UO2 Mass:", (n_r_bottom_fuel.volume+n_r_side_fuel.volume)*UO2.density, "g")
    # TODO More Exact
    mm = 235*0.1975+238*(1-0.1975)
    print("U238 Mass:", (n_r_bottom_fuel.volume+n_r_side_fuel.volume)*UO2.density*mm/(mm+32)*(1-0.1975))
    print("U235 Mass:", (n_r_bottom_fuel.volume+n_r_side_fuel.volume)*UO2.density*mm/(mm+32)*0.1975)
    
    #新中央跑兔Universe
    newRabbitUni= openmc.Universe(name="新跑兔管", cells=[n_r_side_clad, n_r_upper_clad, n_r_lower_clad, n_r_upper_Air, n_r_lower_Air, n_r_lid, n_r_bottom_Cd, n_r_side_Cd, n_r_upper_Cd, n_r_bottom_fuel, n_r_side_fuel, n_r_upper_Al, n_r_H2O_around])
    
    
    ###########################################################################
    #Define a hex_lattice 
    
    core_lattice = openmc.HexLattice()
    core_lattice.pitch = (4.3,)
    core_lattice.outer = H2OUni
    core_lattice.center = (0., 0.)
    core_lattice.orientation = 'x'
    core_lattice._num_rings = 9
    
    out_1 = [H2OUni]+[graphiteUni]*7+[H2OUni]+[graphiteUni]*2+[runRabbitUni]+[graphiteUni]+[runRabbitUni]+[graphiteUni]*2+([H2OUni]+[graphiteUni]*7)*4
    out_2 = [graphiteUni]*7*5+[neuSourceUni]+[graphiteUni]*6
    out_3 = [fuelUni]*5+[graphiteUni]*2+[fuelUni]*6*3+[fuelUni]*5+[graphiteUni]*2+[fuelUni]*4
    out_4 = [fuelUni]*30
    out_5 = [MUni]+[fuelUni]*23
    out_6 = [fuelUni]*3+[A1Uni]+[fuelUni]*2+[B1Uni]+[fuelUni]*2+[DUni]+[fuelUni]*2+[B2Uni]+[fuelUni]*2+[A2Uni]+[fuelUni]*2
    out_7 = [H2OUni]*2+[fuelUni]*3+[H2OUni]*3+[fuelUni]*3+[H2OUni]
    out_8 = [H2OUni]*6
    out_9 = [newRabbitUni]
    core_lattice._universes=[out_1, out_2, out_3, out_4, out_5, out_6, out_7, out_8, out_9]
    
    ins_reactor = openmc.Cell(name='堆芯筒体内', fill=core_lattice, region=-fir_Al_ins & +H2O_low & -H2O_upp)
    
    allUni = openmc.Universe(cells=[ins_reactor,fir_Al,sec_H2O,thi_Al,fou_Pb,fif_Al,six_H2O])
    geo = openmc.Geometry(allUni)
    geo.export_to_xml(path=geodir+"geometry.xml")


#TEST GLOBAL !!!!!!!!!!!!!!!!!!!!!

#update([165,175,205,210,-700, -300, -275, -265, 200, 250, 2200, 2940, 3600])
update([165,180,205,210,-700, -300, -275, -265, 200, 250, 2200, 2940, 3600])
#update([160,175,205,210,-700, -300, -275, -265, 200, 250, 2200, 2940, 3600])
n_r_lower_Air = n_r_lower_Air


if __name__ == '__main__':
    update()
    pass

