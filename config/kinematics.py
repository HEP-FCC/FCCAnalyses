import awkward1 as ak
import numpy as np

#Momentum
def calc_p(array):
    return np.sqrt(array['px']**2 + array['py']**2 + array['pz']**2)

#Transverse momentum
def calc_pt(array):
    return np.sqrt(array['px']**2 + array['py']**2)

#Pseudorapidity
def calc_eta(array):
    return np.arcsinh(array['pz'] / calc_pt(array))

#Theta
def calc_theta(array):
    eta = calc_eta(array)
    return 2 * np.arctan(np.exp(-eta))

#Phi
def calc_phi(array):
    return np.arccos(array['px'] / calc_pt(array))

#Invariant mass for a list of particles, given a list of corresponding rest masses for each particle
def mass(particles, masses):
    for i in range(0,len(particles)):
        particles[i]['e'] = np.sqrt(particles[i]['p']**2 + masses[i]**2)

    tot_energy = particles[0]['e']
    tot_px = particles[0]['px']
    tot_py = particles[0]['py']
    tot_pz = particles[0]['pz']

    for i in range(1,len(particles)):
        tot_energy = tot_energy + particles[i]['e']
        tot_px = tot_px + particles[i]['px']
        tot_py = tot_py + particles[i]['py']
        tot_pz = tot_pz + particles[i]['pz']

    return np.sqrt(tot_energy**2 - tot_px**2 - tot_py**2 - tot_pz**2)

# Cosine of angle between two particles
def cos_angle(left, right):
    left_px_mag = left['px'] / left['p']
    left_py_mag = left['py'] / left['p']
    left_pz_mag = left['pz'] / left['p']

    right_px_mag = right['px'] / right['p']
    right_py_mag = right['py'] / right['p']
    right_pz_mag = right['pz'] / right['p']

    return left_px_mag*right_px_mag + left_py_mag*right_py_mag + left_pz_mag*right_pz_mag
