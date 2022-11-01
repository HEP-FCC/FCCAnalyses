#! /usr/bin/env python

## Python LHAPDF6 usage example for PDF uncertainty code (G. Watt, 24/04/2014).
## Extended in July 2015 for ErrorType values ending in "+as".
## Modified in September 2015 for more general ErrorType values:
## number of parameter variations determined by counting "+" symbols.

from __future__ import print_function
import lhapdf

x = 0.1
q = 100.0
pset = lhapdf.getPDFSet("CT10nnlo") # ErrorType: hessian
#pset = lhapdf.getPDFSet("abm12lhc_5_nnlo") # ErrorType: symmhessian
#pset = lhapdf.getPDFSet("NNPDF30_nnlo_as_0118") # ErrorType: replicas
#pset = lhapdf.getPDFSet("NNPDF30_nnlo_nf_5_pdfas") # ErrorType: replicas+as
pdfs = pset.mkPDFs()
nmem = pset.size - 1

print()
print("Error type = ", pset.errorType)
print("Error conf level = ", pset.errorConfLevel)
print()

npar = pset.errorType.count("+") # number of parameter variations (alphaS, etc.)
if npar > 0:
    print("Last %d members are parameter variations\n" % (2*npar))

## Fill vectors xgAll and xuAll using all PDF members.
xgAll = [0.0 for i in range(pset.size)]
xuAll = [0.0 for i in range(pset.size)]
pdftypes = ["" for i in range(pset.size)]
for imem in range(pset.size):
    xgAll[imem] = pdfs[imem].xfxQ(21, x, q)
    xuAll[imem] = pdfs[imem].xfxQ(2, x, q)
    pdftypes[imem] =  pdfs[imem].type
    #print(imem, xgAll[imem], xuAll[imem], pdftypes[imem])

## Check that the PdfType of each member matches the ErrorType of the set.
## NB. "Hidden" expert-only functionality -- API may change
pset._checkPdfType(pdftypes)

## Calculate 1-sigma PDF uncertainty on gluon distribution.
unc = pset.uncertainty(xgAll)
print("xg = %.4g + %.4g - %.4g (+- %.4g)" % (unc.central, unc.errplus, unc.errminus, unc.errsymm))
print("Scale = %.4g" % (unc.scale))
if npar > 0:
    ## The last 2*npar members correspond to parameter variations (such as alphaS, etc.).
    ## In this case, the errors above are combined PDF+parameter uncertainties, obtained by
    ## adding in quadrature the PDF and parameter uncertainties, shown separately below.
    print("xg(PDF) = %.4g + %.4g - %.4g (+- %.4g)" % (unc.central, unc.errplus_pdf, unc.errminus_pdf, unc.errsymm_pdf))
    print("xg(par) = %.4g +- %.4g" % (unc.central, unc.err_par))
print

## Calculate 1-sigma PDF uncertainty on up-quark distribution.
unc = pset.uncertainty(xuAll)
print("xu = %.4g + %.4g - %.4g (+- %.4g)" % (unc.central, unc.errplus, unc.errminus, unc.errsymm))
print("Scale = %.4g" % unc.scale)
if npar > 0:
    print("xu(PDF) = %.4g + %.4g - %.4g (+- %.4g)" % (unc.central, unc.errplus_pdf, unc.errminus_pdf, unc.errsymm_pdf))
    print("xu(par) = %.4g +- %.4g" % (unc.central, unc.err_par))
print()

## Calculate PDF correlation between gluon and up-quark.
## (This is the PDF-only correlation if npar > 0.)
corr = pset.correlation(xgAll, xuAll)
print("Correlation = %.4g\n" % corr)

## Generate random values from Hessian best-fit and eigenvector values.
if pset.errorType.startswith("hessian") or pset.errorType.startswith("symmhessian"):
    ## If npar > 0 exclude the last 2*npar members (parameter variations).
    npdfmem = nmem - 2*npar
    neigen = npdfmem/2 if pset.errorType.startswith("hessian") else npdfmem
    ## Random numbers are just set to zero here for testing purposes.
    randoms = [0.0 for ir in range(neigen)]
    xgrand = pset.randomValueFromHessian(xgAll, randoms)
    xurand = pset.randomValueFromHessian(xuAll, randoms)
    print("Random: xg = %.4g, xu = %.4g\n" % (xgrand, xurand))
