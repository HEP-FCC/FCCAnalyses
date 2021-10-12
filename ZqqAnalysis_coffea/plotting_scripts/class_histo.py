import numpy as np
import h5py
import matplotlib.pyplot as plt

#f = h5py.File('uproot_file.h5', 'r')
#f = h5py.File('h5_Zjets_2104_cut/QG_comb.h5', 'r')
f = np.load('../ConvNet/eval_filesplitter.npz')

pid = f['arr_1']
CNN = f['arr_0'][:,2]
p4 = f['arr_2']

print(pid)
print(CNN)
print(p4)

#quark_mask = (pid==2)|(pid==1)|(pid==3)
#gluon_mask = (pid==21)

strange_mask = (pid==2)
others_mask = (pid!=2)


p4_s = p4[strange_mask]
p4_o = p4[others_mask]


CNN_s = CNN[strange_mask]
CNN_o = CNN[others_mask]



bins = np.linspace(0.05,0.75,20)
#bins = np.linspace(0.2,0.75,20)
plt.hist(CNN_s, facecolor='b', edgecolor='b', histtype='step', label='strange jets', density=False, bins=bins)
plt.hist(CNN_o, facecolor='r', edgecolor='r', histtype='step', label='down+up jets', density=False, bins=bins)
#plt.yscale('log')
plt.ylabel('Number of Jets')
plt.xlabel(r'Classifier Score ($\mathit{strange}$ $\mathit{node}$)')
plt.title('Jet {} Distribution'.format('CNN'))
plt.title(r'$\mathbf{FCCee}$ Delphes Sim. - (LodeNet $\mathbf{Zuds}$ Jet Distribution), $\sqrt{s}$ = 91 GeV')
plt.legend(loc='upper right')
plt.savefig('../plots/class_histo.pdf')

