#cython: embedsignature=True, c_string_type=str, c_string_encoding=utf8

cimport clhapdf as c
from clhapdf cimport FlavorScheme
from libcpp.string cimport string
from libcpp.vector cimport vector
try:
    from itertools import izip as zip
except ImportError: # python 3.x version
    pass

# For some reason this has to be declared again in order for everything to work...
ctypedef enum FlavorScheme:
    FIXED, VARIABLE

def text_encode(text):
    if isinstance(text, unicode):
        return text.encode('utf8')
    elif isinstance(text, bytes):
        return text
    else:
        raise ValueError("Requires text input")



cdef class PDF:
    """\
    A parton density function for in general several parton flavours,
    i.e. one member of a PDF set.
    """
    cdef c.PDF* _ptr
    cdef set_ptr(self, c.PDF* ptr):
        self._ptr = ptr

    def __dealloc__(self):
        del self._ptr

    @property
    def memberID(self):
        "The PDF set member number of this PDF."
        return self._ptr.memberID()

    @property
    def lhapdfID(self):
        "The LHAPDF ID number of this PDF member."
        return self._ptr.lhapdfID()

    @property
    def type(self):
        "The type of PDF member, e.g. central, error."
        return self._ptr.type()

    @property
    def description(self):
        "Description of this PDF member."
        return self._ptr.description()

    @property
    def orderQCD(self):
        "Max number of loops involved in this PDF's evolution."
        return self._ptr.orderQCD()
    # Alias
    #qcdOrder = orderQCD

    @property
    def xMin(self):
        "Minimum valid value of x to be used with this PDF"
        return self._ptr.xMin()

    @property
    def xMax(self):
        "Maximum valid value of x to be used with this PDF"
        return self._ptr.xMax()

    @property
    def q2Min(self):
        "Minimum valid value of x to be used with this PDF"
        return self._ptr.q2Min()

    @property
    def q2Max(self):
        "Maximum valid value of x to be used with this PDF"
        return self._ptr.q2Max()

    # def alphaS(self):
    #     "Get the AlphaS object used to calculate alpha_s(q)"
    #     cdef c.AlphaS* ptr = &self._ptr.alphaS()
    #     cdef AlphaS obj = AlphaS.__new__(AlphaS)
    #     obj.set_ptr(ptr)
    #     return obj

    def alphasQ(self, q):
        "Return alpha_s at q"
        return self._ptr.alphasQ(q)

    def alphasQ2(self, q2):
        "Return alpha_s at q2"
        return self._ptr.alphasQ2(q2)

    def xfxQ(self, *args):
        """Return the PDF xf(x,Q2) value for the given parton ID, x, and Q values.

        Two forms of arguments are allowed:
        3-args: (pid, x, q)
          If all are scalars, a scalar is returned; if pid is a sequence, a list is
          returned; if x and q are sequences of the same length, they will be zipped
          and a (maybe nested) list of the return values as for scalar x/q will be returned.
          If pid is None, behave like the 2-arg version.
        2-args: (x, q)
          As for 3 args, but always returning results for all PIDs, as a dict. The return
          will be many such dicts in a zipped list if x/q are sequences.
        """
        # TODO: Is this the most efficient way?
        # TODO: Reduce duplication between Q and Q2 variants?
        # If only we'd used PID as the final arg rather than the first, then we could have made it optional/default None...
        if len(args) == 3:
            pid, x, q = args
            if pid is None:
                return self.xfxQ(x, q)
            try:
                try:
                    return [[self._ptr.xfxQ(eachpid, eachx, eachq) for eachpid in pid] for eachx, eachq in zip(x, q)]
                except TypeError:
                    return [self._ptr.xfxQ(pid, eachx, eachq) for eachx, eachq in zip(x, q)]
            except TypeError:
                try:
                    return [self._ptr.xfxQ(eachpid, x, q) for eachpid in pid]
                except TypeError:
                    return self._ptr.xfxQ(pid, x, q)
        elif len(args) == 2:
            x, q = args
            try:
                return [{pid : self._ptr.xfxQ(pid, eachx, eachq) for pid in self.flavors()} for eachx, eachq in zip(x, q)]
            except TypeError:
                return {pid : self._ptr.xfxQ(pid, x, q) for pid in self.flavors()}
        else:
            raise Exception("Wrong number of arguments given to xfxQ: 2 or 3 required, %d provided" % len(args))

    def xfxQ2(self, *args):
        """Return the PDF xf(x,Q2) value for the given parton ID, x, and Q2 values.

        Two forms of arguments are allowed:
        3-args: (pid, x, q2)
          If all are scalars, a scalar is returned; if pid is a sequence, a list is
          returned; if x and q2 are sequences of the same length, they will be zipped
          and a (maybe nested) list of the return values as for scalar x/q2 will be returned.
          If pid is None, behave like the 2-arg version.
        2-args: (x, q2)
          As for 3 args, but always returning results for all PIDs, as a dict. The return
          will be many such dicts in a zipped list if x/q2 are sequences.
        """
        # TODO: Is this the most efficient way?
        # TODO: Reduce duplication between Q and Q2 variants?
        # If only we'd used PID as the final arg rather than the first, then we could have made it optional/default None...
        if len(args) == 3:
            pid, x, q2 = args
            if pid is None:
                return self.xfxQ2(x, q2)
            try:
                try:
                    return [[self._ptr.xfxQ2(eachpid, eachx, eachq2) for eachpid in pid] for eachx, eachq2 in zip(x, q2)]
                except TypeError:
                    return [self._ptr.xfxQ2(pid, eachx, eachq2) for eachx, eachq2 in zip(x, q2)]
            except TypeError:
                try:
                    return [self._ptr.xfxQ2(eachpid, x, q2) for eachpid in pid]
                except TypeError:
                    return self._ptr.xfxQ2(pid, x, q2)
        elif len(args) == 2:
            x, q2 = args
            try:
                return [{pid : self._ptr.xfxQ2(pid, eachx, eachq2) for pid in self.flavors()} for eachx, eachq2 in zip(x, q2)]
            except TypeError:
                return {pid : self._ptr.xfxQ2(pid, x, q2) for pid in self.flavors()}
        else:
            raise Exception("Wrong number of arguments given to xfxQ2: 2 or 3 required, %d provided" % len(args))

    def inRangeQ(self, q):
        "Check if the specified Q value is in the unextrapolated range of this PDF."
        return self._ptr.inRangeQ(q)

    def inRangeQ2(self, q2):
        "Check if the specified Q2 value is in the unextrapolated range of this PDF."
        return self._ptr.inRangeQ2(q2)

    def inRangeX(self, x):
        "Check if the specified x value is in the unextrapolated range of this PDF."
        return self._ptr.inRangeX(x)

    def inRangeXQ(self, x, q):
        "Check if the specified x and Q values are in the unextrapolated range of this PDF."
        return self._ptr.inRangeXQ(x, q)

    def inRangeXQ2(self, x, q2):
        "Check if the specified x and Q2 values are in the unextrapolated range of this PDF."
        return self._ptr.inRangeXQ2(x, q2)

    def flavors(self):
        "Return the list of parton IDs supported by this PDF."
        # TODO: Use Cython >= 0.17 STL type coercion when available
        cdef vector[int] flavs = self._ptr.flavors()
        return [flavs[i] for i in xrange(flavs.size())]

    def hasFlavor(self, pid):
        "Check if the specified parton ID is contained in this PDF."
        return self._ptr.hasFlavor(pid)

    def quarkMass(self, int id):
        "Get mass of quark with PID code id"
        return self._ptr.quarkMass(id)

    def quarkThreshold(self, int id):
        "Get activation threshold of quark with PID code id"
        return self._ptr.quarkThreshold(id)

    cdef _set(self):
        cdef PDFSet obj = PDFSet.__new__(PDFSet)
        obj.set_ptr(&self._ptr.set())
        return obj

    def set(self):
        "Return the corresponding PDFSet"
        return self._set()

    cdef _info(self):
        cdef PDFInfo obj = PDFInfo.__new__(PDFInfo)
        obj.set_ptr(&self._ptr.info())
        return obj

    def info(self):
        "Return the corresponding PDFInfo"
        return self._info()

    def _print(self):
        "Print a short summary to stdout"
        self._ptr._print()


cdef class Info:
    """\
    Class that handles the parsing of PDF set metadata in the .info file.
    """
    cdef c.Info* _ptr
    cdef set_ptr(self, c.Info* ptr):
        self._ptr = ptr

    # def metadata(self):
    #     "Return the metadata in the .info file"
    #     return self._ptr.metadata()

    def has_key(self, key):
        "Return whether or not metadata for this key exists"
        return self._ptr.has_key(text_encode(key))

    def has_key_local(self, key):
        "Returns whether or not metadata for this key exists at a local level (config/set/member)"
        return self._ptr.has_key_local(text_encode(key))

    # def get_entry(self, key):
    #     "Returns metadata entry for this key"
    #     return self._ptr.get_entry(key)

    def get_entry(self, key, fallback=None):
        "Returns metadata entry for this key if it exists, otherwise returns a fallback value"
        rtn = self._ptr.get_entry(text_encode(key), text_encode(str(fallback)))
        return rtn if str(rtn) != str(fallback) else fallback

    def set_entry(self, key, value):
        "Set a metadata key"
        self._ptr.set_entry(text_encode(key), text_encode(str(value)))


class PDFUncertainty:
    """\
    A simple struct containing components of a value with uncertainties calculated
    from a PDF set. Attributes are central, errplus, errminus, errsymm, and scale.
    Extra attributes to return the separate PDF and parameter errors for combined
    PDF+parameter sets are errplus_pdf, errminus_pdf, errsymm_pdf and err_par.
    """
    def __init__(self, central=0.0, errplus=0.0, errminus=0.0, errsymm=0.0, scale=0.0, errplus_pdf=0.0, errminus_pdf=0.0, errsymm_pdf=0.0, err_par=0.0):
        self.central  = central
        self.errplus  = errplus
        self.errminus = errminus
        self.errsymm  = errsymm
        self.scale    = scale
        self.errplus_pdf  = errplus_pdf
        self.errminus_pdf = errminus_pdf
        self.errsymm_pdf  = errsymm_pdf
        self.err_par       = err_par


cdef class PDFSet:
    """\
    A collection of PDFs with related fits, most typically a central PDF and a
    set of extra ones representing different aspects of systematic errors in the
    fit.
    """
    cdef c.PDFSet* _ptr
    cdef set_ptr(self, c.PDFSet* ptr):
        self._ptr = ptr

    def __dealloc__(self):
        pass

    def __len__(self):
        "The total number of members in this set."
        return self._ptr.size()

    @property
    def size(self):
        "The total number of members in this set."
        return self._ptr.size()

    @property
    def name(self):
        "Name of this PDF's containing set."
        return self._ptr.name()

    @property
    def description(self):
        "Description of this PDF's set."
        return self._ptr.description()

    @property
    def lhapdfID(self):
        "First LHAPDF global index in this PDF set."
        return self._ptr.lhapdfID()

    @property
    def dataversion(self):
        "Version of this PDF set's data files."
        return self._ptr.dataversion()

    @property
    def errorType(self):
        "Type of error treatment in this PDF set."
        return self._ptr.errorType()

    @property
    def errorConfLevel(self):
        "Confidence level of error treatment in percent, if one is defined for this set."
        return self._ptr.errorConfLevel()

    def mkPDF(self, mem):
        cdef c.PDF* ptr = self._ptr.mkPDF(mem)
        cdef PDF obj
        obj = PDF.__new__(PDF)
        obj.set_ptr(ptr)
        return obj

    def mkPDFs(self):
        cdef vector[c.PDF*] ptrs = self._ptr.mkPDFs()
        cdef PDF obj
        objs = []
        for ptr in ptrs:
            obj = PDF.__new__(PDF)
            obj.set_ptr(ptr)
            objs.append(obj)
        return objs

    # def metadata(self):
    #     "Return the metadata in the .info file"
    #     return self._ptr.metadata()

    def has_key(self, key):
        "Return whether or not metadata for this key exists"
        return self._ptr.has_key(text_encode(key))

    def has_key_local(self, key):
        "Returns whether or not metadata for this key exists at a local level (config/set/member)"
        return self._ptr.has_key_local(text_encode(key))

    # def get_entry(self, key):
    #     "Returns metadata entry for this key"
    #     return self._ptr.get_entry(key)

    def get_entry(self, key, fallback=None):
        "Returns metadata entry for this key if it exists, otherwise returns a fallback value"
        rtn = self._ptr.get_entry(text_encode(key), text_encode(str(fallback)))
        return rtn if str(rtn) != str(fallback) else fallback

    def _print(self):
        "Print a short summary to stdout"
        self._ptr._print()

    def uncertainty(self, vals, cl=68.268949, alternative=False):
        """\
	Return a PDFUncertainty object corresponding to central value and errors computed
        from the vals list. If unspecified (as a percentage), the confidence level cl defaults
        to 1-sigma. For replicas, by default (alternative=False) the central value is given by
        the mean and the uncertainty by the standard deviation (possibly rescaled to cl), but
        setting alternative=True will instead construct a confidence interval from the
        probability distribution of replicas, with the central value given by the median.
        For a combined PDF+parameter set, the parameter variation uncertainties are computed
        from the last 2*npar set members, where npar is the number of parameters, and a
        breakdown of the separate PDF and parameter variation uncertainties is available.
	"""
        cdef c.PDFUncertainty unc = self._ptr.uncertainty(vals, cl, alternative)
        return PDFUncertainty(unc.central, unc.errplus, unc.errminus, unc.errsymm, unc.scale, unc.errplus_pdf, unc.errminus_pdf, unc.errsymm_pdf, unc.err_par)

    def correlation(self, valsA, valsB):
        """Return the PDF correlation between valsA and valsB using appropriate formulae for this set."""
        return self._ptr.correlation(valsA, valsB)

    def randomValueFromHessian(self, vals, randoms, symmetrise=True):
        """Return a random value from Hessian vals and Gaussian random numbers."""
        return self._ptr.randomValueFromHessian(vals, randoms, symmetrise)

    def _checkPdfType(self, pdftypes):
        """Check that the PdfType of each member matches the ErrorType of the set."""
        self._ptr._checkPdfType(pdftypes)



cdef class PDFInfo:
    """\
    A class handling the metadata that defines a given PDF.
    """

    cdef c.PDFInfo* _ptr
    cdef set_ptr(self, c.PDFInfo* ptr):
        self._ptr = ptr

    # def metadata(self):
    #     "Return the metadata in the .info file"
    #     return self._ptr.metadata()

    def has_key(self, key):
        "Return whether or not metadata for this key exists"
        return self._ptr.has_key(text_encode(key))

    def has_key_local(self, key):
        "Returns whether or not metadata for this key exists at a local level (config/set/member)"
        return self._ptr.has_key_local(text_encode(key))

    # def get_entry(self, key):
    #     "Returns metadata entry for this key"
    #     return self._ptr.get_entry(key)

    def get_entry(self, key, fallback=None):
        "Returns metadata entry for this key if it exists, otherwise returns a fallback value"
        rtn = self._ptr.get_entry(text_encode(key), text_encode(str(fallback)))
        return rtn if str(rtn) != str(fallback) else fallback



cdef class AlphaS:
     """\
     Interface to alpha_s calculations using various schemes.
     """
     cdef c.AlphaS* _ptr
     cdef set_ptr(self, c.AlphaS* ptr):
         self._ptr = ptr

     def __dealloc__(self):
         del self._ptr
         #pass

     @property
     def type(self):
         "Get the method of alpha_s calculation as a string"
         return self._ptr.type()

     def alphasQ(self, double q):
         "Get alpha_s value at scale q"
         return self._ptr.alphasQ(q)

     def alphasQ2(self, double q2):
         "Get alpha_s value at scale q"
         return self._ptr.alphasQ2(q2)

     def numFlavorsQ(self, double q):
         "Get number of active flavors at scale q"
         return self._ptr.numFlavorsQ(q)

     def numFlavorsQ2(self, double q2):
         "Get number of active flavors at scale q"
         return self._ptr.numFlavorsQ2(q2)

     def quarkMass(self, int id):
         "Get mass of quark with PID code id"
         return self._ptr.quarkMass(id)

     def setQuarkMass(self, int id, double value):
         "Set mass of quark with PID code id"
         self._ptr.setQuarkMass(id, value)

     def quarkThreshold(self, int id):
         "Get activation threshold of quark with PID code id"
         return self._ptr.quarkThreshold(id)

     def setQuarkThreshold(self, int id, double value):
         "Set activation threshold of quark with PID code id"
         self._ptr.setQuarkThreshold(id, value)

     def orderQCD(self):
         "Get the QCD running order (max num loops) for this alphaS"
         return self._ptr.orderQCD()

     def setOrderQCD(self, int order):
         "Set the QCD running order (max num loops) for this alphaS"
         self._ptr.setOrderQCD(order)

     def setMZ(self, double mz):
         "Set the Z mass (used in ODE solver)"
         self._ptr.setMZ(mz)

     def setAlphaSMZ(self, double alphas):
         "Set alpha_s at the Z mass (used in ODE solver)"
         self._ptr.setAlphaSMZ(alphas)

     def setLambda(self, int id, double val):
         "Set the id'th LambdaQCD value (used in analytic solver)"
         self._ptr.setLambda(id, val)

     def setFlavorScheme(self, scheme, int nf):
         "Set the flavor scheme. nf is the fixed number (if FIXED)"
         "or the max number (if VARIABLE)"
         cdef FlavorScheme s
         if scheme == "VARIABLE":
           s = VARIABLE
         elif scheme == "FIXED":
           s = FIXED
         else:
           print "You can only set the flavor scheme to FIXED or VARIABLE"
           return
         self._ptr.setFlavorScheme(s,nf)
     def flavorScheme(self):
         cdef FlavorScheme s = self._ptr.flavorScheme()
         if int(s) == 0:
           print "FIXED"
         if int(s) == 1:
           print "VARIABLE"


def getConfig():
    """Factory function to get the global config object."""
    cdef c.Info* ptr = &c.getConfig()
    cdef Info obj = Info.__new__(Info)
    obj.set_ptr(ptr)
    return obj

def getPDFSet(setname):
    """Factory function to get the specified PDF set."""
    cdef c.PDFSet* ptr = &c.getPDFSet(text_encode(setname))
    cdef PDFSet obj = PDFSet.__new__(PDFSet)
    obj.set_ptr(ptr)
    return obj

def mkPDFs(setname):
    """Factory function to make all the PDF objects in the specified set."""
    cdef vector[c.PDF*] ptrs = c.mkPDFs(text_encode(setname))
    cdef PDF obj
    objs = []
    for ptr in ptrs:
        obj = PDF.__new__(PDF)
        obj.set_ptr(ptr)
        objs.append(obj)
    return objs


cdef mkPDF_setmem(string setname, int memid):
    "Factory function to make a PDF object from the set name and member number."
    cdef PDF obj = PDF.__new__(PDF)
    obj.set_ptr(c.mkPDF(setname, memid))
    return obj

cdef mkPDF_lhaid(int lhaid):
    "Factory function to make a PDF object from the LHAPDF ID number."
    cdef PDF obj = PDF.__new__(PDF)
    obj.set_ptr(c.mkPDF(lhaid))
    return obj

cdef mkPDF_setmemstr(string setname_nmem):
    "Factory function to make a PDF object from the set name and member number in SETNAME/NMEM string format."
    cdef PDF obj = PDF.__new__(PDF)
    obj.set_ptr(c.mkPDF(setname_nmem))
    return obj

cdef mkAlphaS_setmem(string setname, int memid):
    "Factory function to make a AlphaS object from the set name and member number."
    cdef AlphaS obj = AlphaS.__new__(AlphaS)
    obj.set_ptr(c.mkAlphaS(setname, memid))
    return obj

cdef mkAlphaS_lhaid(int lhaid):
    "Factory function to make a AlphaS object from the LHAPDF ID number."
    cdef AlphaS obj = AlphaS.__new__(AlphaS)
    obj.set_ptr(c.mkAlphaS(lhaid))
    return obj

cdef mkAlphaS_setmemstr(string setname_nmem):
    "Factory function to make a AlphaS object from the set name and member number in SETNAME/NMEM string format."
    cdef AlphaS obj = AlphaS.__new__(AlphaS)
    obj.set_ptr(c.mkAlphaS(setname_nmem))
    return obj

cdef mkBareAlphaS_(string as_type):
    "Factory function to make an AlphaS object without a PDF reference."
    cdef AlphaS obj = AlphaS.__new__(AlphaS)
    obj.set_ptr(c.mkBareAlphaS(as_type))
    return obj

def mkPDF(*args):
    """Factory function to make a PDF object from the set name and member number
    (2 args), the unique LHAPDF ID number for that member (1 int arg), or the
    SETNAME/NMEM string format."""
    cdef string arg0_string
    if len(args) == 1:
        if type(args[0]) == int:
            return mkPDF_lhaid(args[0])
        if type(args[0]) == str:
            arg0_string = text_encode(args[0])
            return mkPDF_setmemstr(arg0_string)
    elif len(args) == 2 and type(args[0]) == str and type(args[1]) == int:
        arg0_string = text_encode(args[0])
        return mkPDF_setmem(arg0_string, args[1])
    else:
        raise Exception("Unknown call signature")

def mkAlphaS(*args):
    """Factory function to make a AlphaS object from the set name and member number
    (2 args), the unique LHAPDF ID number for that member (1 int arg), or the
    SETNAME/NMEM string format."""
    cdef string arg0_string
    if len(args) == 1:
        if type(args[0]) == int:
            return mkAlphaS_lhaid(args[0])
        if type(args[0]) == str:
            arg0_string = text_encode(args[0])
            return mkAlphaS_setmemstr(arg0_string)
    elif len(args) == 2 and type(args[0]) == str and type(args[1]) == int:
        arg0_string = text_encode(args[0])
        return mkAlphaS_setmem(arg0_string, args[1])
    else:
        raise Exception("Unknown call signature")

def mkBareAlphaS(as_type):
    "Factory function to make a bare AlphaS object."
    return mkBareAlphaS_(as_type)


def weightxQ(int id, double x, double Q, PDF basepdf, PDF newpdf, aschk=5e-2):
    """Reweight from basepdf to newpdf with flavour id and kinematics x and Q2."""
    from cython.operator import dereference
    return c.weightxQ(id, x, Q, dereference(basepdf._ptr), dereference(newpdf._ptr), aschk)

def weightxQ2(int id, double x, double Q2, PDF basepdf, PDF newpdf, aschk=5e-2):
    """Reweight from basepdf to newpdf with flavour id and kinematics x and Q2."""
    from cython.operator import dereference
    return c.weightxQ2(id, x, Q2, dereference(basepdf._ptr), dereference(newpdf._ptr), aschk)

def weightxxQ(int id1, int id2, double x1, double x2, double Q, PDF basepdf, PDF newpdf, aschk=5e-2):
    """Reweight from basepdf to newpdf with flavour id and kinematics x and Q2."""
    from cython.operator import dereference
    return c.weightxxQ(id1, id2, x1, x2, Q, dereference(basepdf._ptr), dereference(newpdf._ptr), aschk)

def weightxxQ2(int id1, int id2, double x1, double x2, double Q2, PDF basepdf, PDF newpdf, aschk=5e-2):
    """Reweight from basepdf to newpdf with flavour id and kinematics x and Q2."""
    from cython.operator import dereference
    return c.weightxxQ2(id1, id2, x1, x2, Q2, dereference(basepdf._ptr), dereference(newpdf._ptr), aschk)



def version():
    "Return the LHAPDF library version."
    return c.version()

__version__ = version()


def verbosity():
    "Get the main verbosity level of the LHAPDF system: 0 = quiet, 2 = loud"
    return c.verbosity()

def setVerbosity(vlevel):
    "Set the main verbosity level of the LHAPDF system: 0 = quiet, 2 = loud"
    c.setVerbosity(vlevel)


def availablePDFSets():
    "Get the names of all the available PDF sets on this system."
    return c.availablePDFSets()


def paths():
    "Return the list of current PDF data search paths."
    return c.paths()

def setPaths(newpaths):
    "Set the list of current PDF data search paths."
    c.setPaths([text_encode(path) for path in newpaths])

def pathsPrepend(newpath):
    "Prepend to the list of current PDF data search paths."
    c.pathsPrepend(text_encode(newpath))

def pathsAppend(newpath):
    "Append to the list of current PDF data search paths."
    c.pathsAppend(text_encode(newpath))
