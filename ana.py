import openmc
import matplotlib.pyplot as plt
import panda as pd

sp = openmc.StatePoint('statepoint.2500.h5')
t1 = sp.get_tally(name='跑兔腔中子谱 手动')
t1_mean = t1.mean.ravel()
t1_unc = t1.std_dev.ravel()

t2 = sp.get_tally(name='跑兔腔中子谱 SHEM-361')
t2_mean = t2.mean.ravel()
t2_unc = t2.std_dev.ravel()

#How to show plt in linux ?
#How to slice energy or plot different colors for each energy

fig, ax = plt.subplots()
ax.step = matplotlib.(energies[:-1])