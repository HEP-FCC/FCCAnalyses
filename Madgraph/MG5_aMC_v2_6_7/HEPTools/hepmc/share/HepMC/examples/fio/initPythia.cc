//////////////////////////////////////////////////////////////////////////
// garren@fnal.gov, April 2007
//
// Initialize pythia
// Using a separate cc file allows us to test issues with PythiaWrapper.h
//
//////////////////////////////////////////////////////////////////////////

#include "HepMC/PythiaWrapper.h"
#include "PythiaHelper.h"

void initPythia()
{
    // (Some platforms may require the initialization of pythia PYDATA block 
    //  data as external - if you get pythia initialization errors try 
    //  commenting in/out the below call to initpydata() )
    // initpydata();
    //
    // Select W+gamma process (process number 20) 
    // (here we have to be careful of C/F77 differences: arrays in C 
    //  start at 0, F77 at 1, so we need to subtract 1 from the process #)
    pysubs.msel=0;
    pysubs.msub[20-1] = 1;
    // set random number seed (mandatory!)
    pydatr.mrpy[0]=55122 ;
    // Tell Pythia not to write multiple copies of particles in event record.
    pypars.mstp[128-1] = 2;
    // Example of setting a Pythia parameter: set the top mass 
    pydat2.pmas[1-1][6-1]= 175;  
    //
    // Call pythia initialization
    call_pyinit( "CMS", "p", "p", 14000. );
}
