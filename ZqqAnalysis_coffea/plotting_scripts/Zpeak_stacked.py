import numpy as np
import h5py
import matplotlib.pyplot as plt

#f = h5py.File('uproot_file.h5', 'r')
#f = h5py.File('h5_Zjets_2104_cut/QG_comb.h5', 'r')
f = np.load('../ConvNet/eval_filesplitter.npz')

pid = f['arr_1']
CNN = f['arr_0'][:,2]
p4 = f['arr_2']
print(np.unique(pid))
#print(pid)
#print(CNN)
#print(p4)

#quark_mask = (pid==2)|(pid==1)|(pid==3)
#gluon_mask = (pid==21)
'''
strange_mask = (pid==2)
#others_mask = (pid!=2)
down_mask = (pid==0)

p4_s = p4[strange_mask]
#p4_o = p4[others_mask]
p4_d = p4[down_mask]
'''

#1. compute invariant mass -> down select invariant mass via event mask, and down select pid via event mask (pid is double the length so consider only every second element, they are duplicates) -> cut the result into u,d,s event and plot...
# The plan for the Zpeak is to compute the Zpeak for doubly s-tagged events. To this end we should first make a mask for s tagged events.
# For now I require a classifier score of 0.55, though this is just a guess based on the classifier distribution.

inv_mass = np.sqrt((p4[::2,0]+p4[1::2,0])**2-((p4[::2,1]+p4[1::2,1])**2+(p4[::2,2]+p4[1::2,2])**2+(p4[::2,3]+p4[1::2,3])**2))
print(inv_mass)


firstJet_mask = (CNN[::2]>0.55)
secondJet_mask = (CNN[1::2]>0.55)
event_mask = firstJet_mask&secondJet_mask
print(len(inv_mass))
inv_mass = inv_mass[event_mask]
pid = pid[::2][event_mask]

strange_mask = (pid==2)
down_mask = (pid==0)
up_mask = (pid==1)

inv_mass_s = inv_mass[strange_mask]
inv_mass_d = inv_mass[down_mask]
inv_mass_u = inv_mass[up_mask]
print(len(inv_mass_s))
#print(event_mask)
#print(inv_mass)
#print(inv_mass_s)

bins = np.linspace(90.95,91.50,20)
#bins = np.linspace(0.2,0.75,20)
# Have a look into color scheme at some point
plt.hist([inv_mass_s, inv_mass_d, inv_mass_u], histtype='step', label=['strange jets','down jets','up jets'], density=False, bins=bins, stacked=True)
#plt.hist([inv_mass_s, inv_mass_o], facecolor='b', edgecolor='b', histtype='step', label='strange jets', density=False, bins=bins, stacked=True)
#plt.hist(inv_mass_o, facecolor='r', edgecolor='r', histtype='step', label='down+up jets', density=False, bins=bins, stacked=True)
#plt.yscale('log')
plt.ylabel('Number of Events')
plt.xlabel(r'$\mathbf{Z}$ invariant mass [GeV]')
#plt.title('Jet {} Distribution'.format('CNN'))
plt.title(r'$\mathbf{FCCee}$ Delphes Sim. - (s-tagged $\mathbf{Z}$ invariant mass), $\sqrt{s}$ = 91 GeV')
plt.legend(loc='upper right')
plt.savefig('../plots/Zpeak_stacked.pdf')

