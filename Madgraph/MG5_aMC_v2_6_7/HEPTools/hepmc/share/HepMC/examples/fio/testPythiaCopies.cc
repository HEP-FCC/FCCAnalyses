//////////////////////////////////////////////////////////////////////////
// testPythiaCopies.cc
//
// garren@fnal.gov, January 2008
// Multiple events in memory at the same time
//////////////////////////////////////////////////////////////////////////

#include <fstream>
#include <iostream>
#include "HepMC/PythiaWrapper.h"
#include "HepMC/IO_HEPEVT.h"
#include "HepMC/GenEvent.h"
#include "HepMC/CompareGenEvent.h"
#include "PythiaHelper.h"

int main() { 	
    //
    //........................................HEPEVT
    // Pythia 6.1 uses HEPEVT with 4000 entries and 8-byte floating point
    //  numbers. We need to explicitly pass this information to the 
    //  HEPEVT_Wrapper.
    //
    HepMC::HEPEVT_Wrapper::set_max_number_entries(4000);
    HepMC::HEPEVT_Wrapper::set_sizeof_real(8);
    //	
    //........................................PYTHIA INITIALIZATIONS
    initPythia();
    //
    //........................................HepMC INITIALIZATIONS
    //
    // Instantiate an IO strategy for reading from HEPEVT.
    HepMC::IO_HEPEVT hepevtio;
    //
    // open some output files
    std::ofstream out1( "testPythiaOriginals.dat" );
    std::ofstream out2( "testPythiaCopies1.dat" );
    std::ofstream out3( "testPythiaCopies2.dat" );
    //
    //........................................EVENT LOOP
    for ( int i = 1; i <= 50; i++ ) {
	if ( i%50==1 ) std::cout << "Processing Event Number " 
				 << i << std::endl;
	call_pyevnt();      // generate one event with Pythia
	// pythia pyhepc routine convert common PYJETS in common HEPEVT
	call_pyhepc( 1 );
	HepMC::GenEvent* evt = hepevtio.read_next_event();
	// pythia uses GeV and mm
	evt->use_units( HepMC::Units::GEV, HepMC::Units::MM);
	// set a couple of arbitrary weights
	evt->weights().push_back(0.456);
	evt->weights()["test2"] = 0.8956;
	// set number of multi parton interactions
	evt->set_mpi( pypars.msti[31-1] );
	// set cross section information
	evt->set_cross_section( HepMC::getPythiaCrossSection() );
	//
	//.......................make some copies
	evt->print(out1);
	HepMC::GenEvent ec = (*evt);
	ec.print(out2);
	HepMC::GenEvent* evt4 = new HepMC::GenEvent(*evt);
	evt4->print(out3);
 	if( !compareGenEvent(evt,evt4) ) { 
	   std::cerr << "testPythiaCopies: GenEvent comparison fails at event "
	             << evt->event_number() << std::endl;
	   return -1; 
	}
	//
	// now delete the created events from memory
	delete evt;
        delete evt4;
    }
    //........................................TERMINATION
    // write out some information from Pythia to the screen
    call_pystat( 1 );    
    std::cout << "testPythiaCopies: event comparison is successful" << std::endl;

    return 0;
}


 
