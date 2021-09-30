import coffea.hist as hist
import h5py
import matplotlib.pyplot as plt
import numpy as np

def fullprint(*args, **kwargs):
  from pprint import pprint
  import numpy
  opt = numpy.get_printoptions()
  numpy.set_printoptions(threshold=numpy.inf)
  pprint(*args, **kwargs)
  numpy.set_printoptions(**opt)


channel = 'ss'
part = 'neutralKaon'

f = h5py.File('h5_output/Z{0}_weighted_summed.h5'.format(channel), 'r')

'''
#Here we load the properties of the first jet into numpy arrays for plotting
px_0 = f['px'][:,0]
py_0 = f['py'][:,0]
pz_0 = f['pz'][:,0]
E_0 = f['E'][:,0]
pid_0 = f['pid'][:,0]

#Here we load the properties of the second jet
px_1 = f['px'][:,1]
py_1 = f['py'][:,1]
pz_1 = f['pz'][:,1]
E_1 = f['E'][:,1]
pid_1 = f['pid'][:,1]
'''


histos = f['histos_{0}'.format(part)][:]


f.close()

bins = np.linspace(-0.5,0.5,30)

'''
histo = hist.Hist("Counts",
                  ##hist.Cat("sample", "sample name"),
                  hist.Bin("x", "x value", 50, -10, 10),
                  hist.Bin("y", "y value", 50, -10, 10),
                  ##hist.Bin("z", "z value", 20, -10, 10),
                 )

h = hist.Hist("Counts",
                     #hist.Cat("ptype", "particle type"),
                     hist.Bin("phi", r"$\mathbf{\Delta \phi}$ (azimuthal angle in rad)", 40, -4, 4),
                     hist.Bin("theta", r"$\mathbf{\Delta \theta}$ (beam angle in rad)", 40, -4, 4),
                     )
'''
##plt.matshow(np.sum(histos[:,6], axis=0))
#plt.pcolormesh(bins, bins, np.sum(histos[:,1], axis=0))
plt.pcolormesh(bins, bins, histos)
plt.colorbar()
#fullprint(np.sum(histos[:,1], axis=0))
#plt.grid()
#plt.gca().set_xticks([x - 0.5 for x in plt.gca().get_xticks()][1:], minor='true')
#plt.gca().set_yticks([y - 0.5 for y in plt.gca().get_yticks()][1:], minor='true')
#plt.grid(which='minor')

print('//////////')
plt.savefig('test/pcolormesh_Z{0}_weighted_100k_{1}.pdf'.format(channel, part))


