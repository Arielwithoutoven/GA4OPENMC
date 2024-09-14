import openmc
from mat_no_tem import *
from geo import *
import numpy as np
import matplotlib.pyplot as plt

colors = {H2O:"blue", U:"silver", UHZr:"orange", UO2:"red", Al:"darkblue", Al_pure:"darkblue", Air:"white", Zr:"silver", Graphite:"black", He:"white", SS:"silver", B4C:"brown", Pb:"black", AmO2_Be:"orange", Cd:"green"}  # RGB tuple (255, 255, 255) or SVG color "#FFFFFF"?
#colors[H2O] = )
colors[Al] = (180, 180, 180)
colors[Al_pure] = (200, 223, 227)
#colors[Graphite] = (87, 33, 77)
colors[SS] = (128, 128, 126)


def upPlots():
    pl = openmc.Plot(name="整个堆芯xy")
    pl._basis='xy'
    pl._color_by='material'
    pl._colors=colors
    pl._filename='core_xy'
    pl._origin=(0, 0, 0)
    pl._pixels=[5000, 5000]
    pl._width=[80., 80.]
    
    pl2 = openmc.Plot(name="整个堆芯xz")
    pl2._basis='xz'
    pl2._color_by='material'
    pl2._colors=colors
    pl2._filename='core_xz'
    pl2._origin=(0, 0, -10)
    pl2._pixels=[8500, 14000]
    pl2._width=[85., 140.]

    pl4 = openmc.Plot(name="跑兔腔xy")
    pl4._basis='xy'
    pl4._color_by='material'
    pl4._colors=colors
    pl4._filename='rab_xy'
    pl4._origin=(0, 0, 0)
    pl4._pixels=[2800, 2800]
    pl4._width=[4.5, 4.5]
    
    pl3 = openmc.Plot(name="跑兔腔xz")
    pl3._basis='xz'
    pl3._color_by='material'
    pl3._colors=colors
    pl3._filename='rab_xz'
    pl3._origin=(0, 0, 15)
    pl3._pixels=[500, 5000]
    pl3._width=[5., 50.]
    
    pls = openmc.Plots([pl, pl2, pl3, pl4])
    pls.export_to_xml()


def upSettings():
    space = openmc.stats.Box(lower_left=[-11.9, 0., -19.5], upper_right=[13.9, 0., 19.5], only_fissionable=True) # spatial sites should only be accepted if they occur in fissionable materials
    source = openmc.IndependentSource(space=space,particle='neutron',strength=1.0)
    
    settings = openmc.Settings(run_mode="eigenvalue", batches=2500, particles=20000, inactive=200, source=source)
    settings.export_to_xml()


def upTallies():
    mesh = openmc.RegularMesh(name='Core Mesh')
    mesh.dimension=[50, 50] #网格数，也可以是三维的
    mesh.upper_right=[35, 35]
    mesh.lower_left=[-35,-35]
    
    meshFil = openmc.MeshFilter(mesh) # 基于网格的Filter
    
    cellFil = openmc.CellFilter(n_r_lower_Air)
    global energies
    energies = np.logspace(np.log10(1e-5), np.log10(20.0e6), 1001) # 1000个能量网格
    energyFil = openmc.EnergyFilter(energies)
    
    tal1 = openmc.Tally(name='跑兔腔中子谱 手动')
    tal1.filters=[cellFil, energyFil]
    tal1.scores=['flux']
    
    tal2 = openmc.Tally(name='堆芯中子通量和裂变')
    tal2.filters=[meshFil, energyFil]
    tal2.scores=['flux','fission']
    
    # print(openmc.mgxs.GROUP_STRUCTURES.keys()) # 可用的能群计算方式
    global energies_shem
    energies_shem = openmc.mgxs.GROUP_STRUCTURES['SHEM-361']
    shem_fil = openmc.EnergyFilter(energies_shem)
    tal_shem = openmc.Tally(name='跑兔腔中子谱 SHEM-361')
    tal_shem.filters=[cellFil, shem_fil]
    tal_shem.scores=['flux']
    
    trigger = openmc.Trigger(trigger_type='std_dev', threshold=5e-5)
    trigger.scores=['absorption']
    
    tallies = openmc.Tallies([tal1, tal_shem])
    tallies.export_to_xml()

def analisis():
    sp = openmc.StatePoint('statepoint.2500.h5')
    t1 = sp.get_tally(name='跑兔腔中子谱 手动')
    t1_mean = t1.mean.ravel()
    t1_unc = t1.std_dev.ravel()
    rrate = 0
    for i in range(len(t1_mean)):
        rrate += t1_mean[i] if energies[i]>0.1e6 else 0 
    print('Fast Neutron rate:', rrate/t1_mean.sum()*100, '%')
    print('Average Energy:', np.array([t1_mean[i]*energies[i] for i in range(len(t1_mean))]).sum()/t1_mean.sum(), 'eV')
    
    t2 = sp.get_tally(name='跑兔腔中子谱 SHEM-361')
    t2_mean = t2.mean.ravel()
    t2_unc = t2.std_dev.ravel()
    
    fig, ax = plt.subplots()
    ax.step(energies[:-1], t1_mean/np.diff(energies), where='post', label='1000 group')
    ax.step(energies_shem[:-1], t2_mean/np.diff(energies_shem), where='post', label='SHEM-361')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('Energy [eV]')
    ax.set_ylabel('Flux [n-cm/eV-src]')
    ax.grid()
    ax.legend()
    plt.savefig('Energy-Flux')
    

if __name__ == '__main__':
    upPlots()
    upSettings()
    upTallies()
    

    openmc.plot_geometry() # the same as `openmc -p` # TODO How to plot to a specific dir?
    #openmc.run()
    
    analisis()
    pass
