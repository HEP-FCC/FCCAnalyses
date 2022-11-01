from libcpp.string cimport string
from libcpp.map cimport map
from libcpp.vector cimport vector
from libcpp cimport bool


cdef extern from "../../include/LHAPDF/Version.h" namespace "LHAPDF":
    cdef string version()

cdef extern from "../../include/LHAPDF/Paths.h" namespace "LHAPDF":
    cdef vector[string] paths()
    cdef void setPaths(vector[string])
    cdef void pathsPrepend(string)
    cdef void pathsAppend(string)
    cdef vector[string] availablePDFSets()

cdef extern from "../../include/LHAPDF/PDF.h" namespace "LHAPDF":
    cdef cppclass PDF:
        double xfxQ(int, double, double) except +
        double xfxQ2(int, double, double) except +
        map[int,double] xfxQ(double, double) except +
        map[int,double] xfxQ2(double, double) except +
        double alphasQ(double) except +
        double alphasQ2(double) except +
        double xMin()
        double xMax()
        double q2Min()
        double q2Max()
        bool inRangeX(double) except +
        bool inRangeQ(double) except +
        bool inRangeQ2(double) except +
        bool inRangeXQ(double, double) except +
        bool inRangeXQ2(double, double) except +
        bool hasFlavor(int) except +
        vector[int] flavors()
        int memberID() except +
        int lhapdfID() except +
        string description() except +
        string type() except +
        int orderQCD() except +
        double quarkMass(int) except +
        double quarkThreshold(int) except +
        void _print "print" () except + # TODO: add the second (verbosity) argument
        PDFSet& set() # TODO: add exception when bug in ref rtn fns is gone
        PDFInfo& info() # TODO: add exception when bug in ref rtn fns is gone
        const AlphaS& alphaS() # TODO: add exception when bug in ref rtn fns is gone

cdef extern from "../../include/LHAPDF/Info.h" namespace "LHAPDF":
    cdef cppclass Info:
        bool has_key(string)
        bool has_key_local(string)
        string get_entry(string) except +
        string get_entry(string, string) except +
        void set_entry(string, string)

cdef extern from "../../include/LHAPDF/Config.h" namespace "LHAPDF":
    cdef cppclass Config(Info.Info):
        pass
    cdef int verbosity()
    cdef void setVerbosity(int)

cdef extern from "../../include/LHAPDF/PDFSet.h" namespace "LHAPDF":
    cdef cppclass PDFSet(Info.Info):
        vector[PDF*] mkPDFs()
        PDF* mkPDF(int)
        size_t size() except +
        string name() except +
        string description()
        int lhapdfID() except +
        int dataversion() except +
        void _print "print" () except + # TODO: map the second (verbosity) argument
        string errorType() except +
        double errorConfLevel() except +
        PDFUncertainty uncertainty(vector[double]&, double, bool) except +
        #void uncertainty(PDFUncertainty&, vector[double]&, double, bool) except +
        double correlation(vector[double]&, vector[double]&) except +
        double randomValueFromHessian(vector[double]&, vector[double]&, bool) except +
        void _checkPdfType(vector[string]&) except +

cdef extern from "../../include/LHAPDF/AlphaS.h" namespace "LHAPDF::AlphaS":
    ctypedef enum FlavorScheme:
        FIXED
        VARIABLE

cdef extern from "../../include/LHAPDF/AlphaS.h" namespace "LHAPDF":
    cdef cppclass AlphaS:
        string type() except +
        double alphasQ(double q) except +
        double alphasQ2(double q2) except +
        int numFlavorsQ(double q) except +
        int numFlavorsQ2(double q2) except +
        double quarkMass(int id) except +
        void setQuarkMass(int id, double value) except +
        double quarkThreshold(int id) except +
        void setQuarkThreshold(int id, double val) except +
        int orderQCD() except +
        void setOrderQCD(int order) except +
        void setMZ(double mz) except +
        void setAlphaSMZ(double alphas) except +
        void setLambda(unsigned int, double) except +
        void setFlavorScheme(FlavorScheme scheme, int nf) except +
        FlavorScheme flavorScheme() except +

cdef extern from "../../include/LHAPDF/PDFSet.h" namespace "LHAPDF":
    cdef struct PDFUncertainty:
        double central
        double errplus
        double errminus
        double errsymm
        double scale
        double errplus_pdf
        double errminus_pdf
        double errsymm_pdf
        double err_par

cdef extern from "../../include/LHAPDF/PDFInfo.h" namespace "LHAPDF":
    cdef cppclass PDFInfo(Info.Info):
        pass #bool has_key(string)

cdef extern from "../../include/LHAPDF/Factories.h" namespace "LHAPDF":
    cdef Info& getConfig() #except +  # TODO: re-enable when Cython refs+exceptions has been bugfixed
    cdef PDFSet& getPDFSet(string) #except +  # TODO: re-enable when Cython refs+exceptions has been bugfixed
    cdef vector[PDF*] mkPDFs(string) except +
    cdef PDF* mkPDF(string) except +
    cdef PDF* mkPDF(string, int) except +
    cdef PDF* mkPDF(int) except +
    cdef AlphaS* mkAlphaS(string) except +
    cdef AlphaS* mkAlphaS(int) except +
    cdef AlphaS* mkAlphaS(string, int) except +
    cdef AlphaS* mkBareAlphaS(string) except +

cdef extern from "../../include/LHAPDF/Reweighting.h" namespace "LHAPDF":
    cdef double weightxQ2(int id, double x, double Q2, PDF& basepdf, PDF& newpdf, double aschk)
    cdef double weightxQ(int id, double x, double Q, const PDF& basepdf, const PDF& newpdf, double aschk)
    cdef double weightxxQ2(int id1, int id2, double x1, double x2, double Q2, const PDF& basepdf, const PDF& newpdf, double aschk)
    cdef double weightxxQ(int id1, int id2, double x1, double x2, double Q, const PDF& basepdf, const PDF& newpdf, double aschk)
