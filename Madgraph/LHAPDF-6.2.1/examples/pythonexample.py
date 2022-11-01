#! /usr/bin/env python

## Python LHAPDF6 usage example

import lhapdf

## Getting a PDF member object
p = lhapdf.mkPDF("CT10", 0)
p = lhapdf.mkPDF("CT10/0")

## Gluon PDF querying at x=0.001, Q2=10000
print(p.xfxQ2(21, 1e-3, 1e4))

## Basic all-flavour PDF querying at x=0.01, Q=M_Z
for pid in p.flavors():
    print(p.xfxQ(pid, 0.01, 91.2))

# TODO: demonstrate looping over PDF set members
pset = lhapdf.getPDFSet("CT10nlo")
print(pset.description)
pcentral = pset.mkPDF(0)
pdfs1 = pset.mkPDFs()
pdfs2 = lhapdf.mkPDFs("CT10nlo") # a direct way to get all the set's PDFs

## Filling a numpy 2D array with xf(x,Q) samples
import numpy as np
xs = [x for x in np.logspace(-7, 0, 5)]
qs = [q for q in np.logspace(1, 4, 4)]
gluon_xfs = np.empty([len(xs), len(qs)])
for ix, x in enumerate(xs):
    for iq, q in enumerate(qs):
        gluon_xfs[ix,iq] = p.xfxQ(21, x, q)
print(gluon_xfs)

## Version info, search paths, and metadata
print(lhapdf.version())
print(lhapdf.__version__)
lhapdf.pathsPrepend("/path/to/extra/pdfsets")
print(lhapdf.paths())
# ...
