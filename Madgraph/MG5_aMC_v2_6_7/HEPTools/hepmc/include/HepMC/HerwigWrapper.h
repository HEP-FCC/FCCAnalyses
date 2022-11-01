//--------------------------------------------------------------------------
#ifndef HERWIG_WRAPPER_H
#define HERWIG_WRAPPER_H

//////////////////////////////////////////////////////////////////////////
// Matt.Dobbs@Cern.CH, November 200July 2002
// Wrapper for FORTRAN version of Herwig
// Wrapper written for Herwig 6.4
//////////////////////////////////////////////////////////////////////////

#include <ctype.h>

// This pre-compiler directive is included (2002-01-16) to allow compatibility
// with MS Visual C++, which interfaces to fortran in a different manner.
// For it to work you need to define the _WIN32 variable when compiling.
#ifdef _WIN32 // Platform: Windows MS Visual C++

//  Sorry, there is NO version currently available for Vusual C++.

#else // Generic version, tested on Linux ecgs/gcc

//--------------------------------------------------------------------------
// HERWIG Common Block Declarations

//        COMMON/HWPROC/EBEAM1,EBEAM2,PBEAM1,PBEAM2,IPROC,MAXEV
extern "C" {
    extern struct {
	double EBEAM1,EBEAM2,PBEAM1,PBEAM2;
        int IPROC,MAXEV;
    } hwproc_;
}
#define hwproc hwproc_

//      COMMON/HWBEAM/IPART1,IPART2
extern "C" {
    extern struct {
        int IPART1, IPART2;
    } hwbeam_;
}
#define hwbeam hwbeam_

//        CHARACTER*8 PART1,PART2
//        COMMON/HWBMCH/PART1,PART2
extern "C" {
    extern struct {
	char PART1[8],PART2[8];
    } hwbmch_;
}
#define hwbmch hwbmch_

//  COMMON/HWEVNT/AVWGT,EVWGT,GAMWT,TLOUT,WBIGST,WGTMAX,WGTSUM,WSQSUM,
//       & IDHW(NMXHEP),IERROR,ISTAT,LWEVT,MAXER,MAXPR,NOWGT,NRN(2),NUMER,
//       & NUMERU,NWGTS,GENSOF
const int herwig_hepevt_size = 4000;
extern "C" {
    extern struct hwgev {
	double AVWGT,EVWGT,GAMWT,TLOUT,WBIGST,WGTMAX,WGTSUM,WSQSUM;
	int IDHW[herwig_hepevt_size],IERROR,ISTAT,LWEVT,MAXER,MAXPR;
	int NOWGT,NRN[2],NUMER,NUMERU,NWGTS;
	int GENSOF; //Beware! in F77 this is logical
    } hwevnt_;
}
#define hwevnt hwevnt_

//  C Basic parameters (and quantities derived from them)
//        COMMON/HWPRAM/AFCH(16,2),ALPHEM,B1LIM,BETAF,BTCLM,CAFAC,CFFAC,
//       & CLMAX,CLPOW,CLSMR(2),CSPEED,ENSOF,ETAMIX,F0MIX,F1MIX,F2MIX,GAMH,
//       & GAMW,GAMZ,GAMZP,GEV2NB,H1MIX,PDIQK,PGSMX,PGSPL(4),PHIMIX,PIFAC,
//       & PRSOF,PSPLT(2),PTRMS,PXRMS,QCDL3,QCDL5,QCDLAM,QDIQK,QFCH(16),QG,
//       & QSPAC,QV,SCABI,SWEIN,TMTOP,VFCH(16,2),VCKM(3,3),VGCUT,VQCUT,
//       & VPCUT,ZBINM,EFFMIN,OMHMIX,ET2MIX,PH3MIX,GCUTME,
//       & IOPREM,IPRINT,ISPAC,LRSUD,LWSUD,MODPDF(2),NBTRY,NCOLO,NCTRY,
//       & NDTRY,NETRY,NFLAV,NGSPL,NSTRU,NSTRY,NZBIN,IOP4JT(2),NPRFMT,
//       & AZSOFT,AZSPIN,CLDIR(2),HARDME,NOSPAC,PRNDEC,PRVTX,SOFTME,ZPRIME,
//       & PRNDEF,PRNTEX,PRNWEB

extern "C" {
    extern struct {
	double AFCH[2][16],ALPHEM,B1LIM,BETAF,BTCLM,CAFAC,CFFAC,
	    CLMAX,CLPOW,CLSMR[2],CSPEED,ENSOF,ETAMIX,F0MIX,F1MIX,F2MIX,GAMH,
	    GAMW,GAMZ,GAMZP,GEV2NB,H1MIX,PDIQK,PGSMX,PGSPL[4],PHIMIX,PIFAC,
	    PRSOF,PSPLT[2],PTRMS,PXRMS,QCDL3,QCDL5,QCDLAM,QDIQK,QFCH[16],QG,
	    QSPAC,QV,SCABI,SWEIN,TMTOP,VFCH[2][16],VCKM[3][3],VGCUT,VQCUT,
	    VPCUT,ZBINM,EFFMIN,OMHMIX,ET2MIX,PH3MIX,GCUTME;
	int IOPREM,IPRINT,ISPAC,LRSUD,LWSUD,MODPDF[2],NBTRY,NCOLO,NCTRY,
	    NDTRY,NETRY,NFLAV,NGSPL,NSTRU,NSTRY,NZBIN,IOP4JT[2],NPRFMT;
	int AZSOFT,AZSPIN,CLDIR[2],HARDME,NOSPAC,PRNDEC,PRVTX,SOFTME,
	    ZPRIME,PRNDEF,PRNTEX,PRNWEB; //Beware! in F77 these are logical
    } hwpram_;
}
#define hwpram hwpram_

//--------------------------------------------------------------------------
// HERWIG routines declaration

#define hwigin hwigin_  // initialise other common blocks
#define hwigup hwigup_  // initialise HepUP run common block
#define hwuinc hwuinc_  // compute parameter-dependent constants
#define hwusta hwusta_  // call hwusta to make any particle stable
#define hweini hweini_  // initialise elementary process
#define hwuine hwuine_  // initialise event
#define hwepro hwepro_  // generate HERWIG hard subprocess
#define hwupro hwupro_  // read USER hard subprocess from HepUP event common
#define hwbgen hwbgen_  // generate parton cascades
#define hwdhob hwdhob_  // do heavy object decays
#define hwcfor hwcfor_  // do cluster hadronization
#define hwcdec hwcdec_  // do cluster decay
#define hwdhad hwdhad_  // do unstable particle decays
#define hwdhvy hwdhvy_  // do heavy flavour decays
#define hwmevt hwmevt_  // add soft underlying event if needed 
#define hwufne hwufne_  // event generation completed, wrap up event .... 
#define hwefin hwefin_  // terminate elementary process

#define hwudpr hwudpr_  // prints out particle/decay properties
#define hwuepr hwuepr_  // prints out event data
#define hwupup hwupup_  // prints out HepEUP user common block event data
#define hwegup hwegup_  // terminal calculations to replace HWEFIN for HepUP
    extern "C" {
        void hwigin(void);
        void hwigup(void);
        void hwuinc(void);
        void hwusta(const char*,int);
        void hweini(void);
        void hwuine(void);
        void hwepro(void);
        void hwupro(void);
        void hwbgen(void);
        void hwdhob(void);
        void hwcfor(void);
        void hwcdec(void);
        void hwdhad(void);
        void hwdhvy(void);
        void hwmevt(void);
        void hwufne(void);
        void hwefin(void);
        void hwudpr(void);
        void hwuepr(void);
	void hwupup(void);
	void hwegup(void);
    }

//--------------------------------------------------------------------------
// HERWIG block data
// ( with gcc it works to initialize the block data by calling 
//   "hwudat();" at beginning. )

#define hwudat hwudat_
extern "C" {
    void hwudat(void);
}


#include "HepMC/GenCrossSection.h"

namespace HepMC {

/// calculate the Herwig cross section and statistical error
GenCrossSection getHerwigCrossSection(int ngen);

} // HepMC

#endif // Platform

#endif  // HERWIG_WRAPPER_H

//--------------------------------------------------------------------------
