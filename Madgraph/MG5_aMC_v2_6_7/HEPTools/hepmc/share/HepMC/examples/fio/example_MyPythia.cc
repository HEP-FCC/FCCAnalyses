//////////////////////////////////////////////////////////////////////////
// Matt.Dobbs@Cern.CH, December 1999
// November 2000, updated to use Pythia 6.1
// 
//////////////////////////////////////////////////////////////////////////
/// example of generating events with Pythia using HepMC/PythiaWrapper.h 
/// Events are read into the HepMC event record from the FORTRAN HEPEVT 
/// common block using the IO_HEPEVT strategy 
///
/// To Compile: go to the HepMC directory and type:
/// gmake examples/example_MyPythia.exe
///
/// In this example the precision and number of entries for the HEPEVT 
/// fortran common block are explicitly defined to correspond to those 
/// used in the Pythia version of the HEPEVT common block. 
///
/// If you get funny output from HEPEVT in your own code, probably you have
/// set these values incorrectly!
///
//////////////////////////////////////////////////////////////////////////
///
/// pythia_out():
/// Events are read into the HepMC event record from the FORTRAN HEPEVT
/// common block using the IO_HEPEVT strategy and then output to file in
/// ascii format using the IO_GenEvent strategy.
///
/// pythia_particle_out():
/// Events are read into the HepMC event record from the FORTRAN HEPEVT
/// common block using the IO_HEPEVT strategy and then output to file in
/// ascii format using the IO_AsciiParticles strategy.  
/// This is identical to pythia_out() except for the choice of output format.
///
/// event_selection():
/// Events are read into the HepMC event record from the FORTRAN HEPEVT 
/// common block using the IO_HEPEVT strategy and then a very simple event
/// selection is performed.
///
/// pythia_in():
/// Read the file created by pythia_out().
///
/// pythia_in_out():
/// generate events with Pythia, write a file, and read the resulting output
/// Notice that we use scope to explicitly close the ouput files.
/// The two output files should be identical.
///


#include <iostream>
#include "HepMC/PythiaWrapper.h"
#include "HepMC/IO_HEPEVT.h"
#include "HepMC/IO_GenEvent.h"
#include "HepMC/IO_AsciiParticles.h"
#include "HepMC/GenEvent.h"
#include "PythiaHelper.h"

//! example class

/// \class  IsGoodEventMyPythia
/// event selection predicate. returns true if the event contains
/// a photon with pT > 25 GeV
class IsGoodEventMyPythia {
public:
    /// returns true if event is "good"
    bool operator()( const HepMC::GenEvent* evt ) { 
	for ( HepMC::GenEvent::particle_const_iterator p 
		  = evt->particles_begin(); p != evt->particles_end(); ++p ){
	    if ( (*p)->pdg_id() == 22 && (*p)->momentum().perp() > 25. ) {
		//std::cout << "Event " << evt->event_number()
		//     << " is a good event." << std::endl;
		//(*p)->print();
		return 1;
	    }
	}
	return 0;
    }
};
    

void pythia_out();
void pythia_in();
void pythia_in_out();
void event_selection();
void pythia_particle_out();

int main() { 
    // example to generate events and write output
    pythia_out();
    // example to generate events and perform simple event selection
    event_selection();
    // example to read the file written by pythia_out
    pythia_in();
    // example to generate events, write them, and read them back
    pythia_in_out();

    return 0;
}


void pythia_out()
{
    std::cout << std::endl;
    std::cout << "Begin pythia_out()" << std::endl;
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

    //........................................HepMC INITIALIZATIONS
    //
    // Instantiate an IO strategy for reading from HEPEVT.
    HepMC::IO_HEPEVT hepevtio;
    //
    { // begin scope of ascii_io
	// Instantiate an IO strategy to write the data to file 
	HepMC::IO_GenEvent ascii_io("example_MyPythia.dat",std::ios::out);
	//
	//........................................EVENT LOOP
	for ( int i = 1; i <= 100; i++ ) {
	    if ( i%50==1 ) std::cout << "Processing Event Number " 
				     << i << std::endl;
	    call_pyevnt();      // generate one event with Pythia
	    // pythia pyhepc routine converts common PYJETS in common HEPEVT
	    call_pyhepc( 1 );
	    HepMC::GenEvent* evt = hepevtio.read_next_event();
	    // define the units (Pythia uses GeV and mm)
	    evt->use_units(HepMC::Units::GEV, HepMC::Units::MM);
	    // add some information to the event
	    evt->set_event_number(i);
	    evt->set_signal_process_id(20);
	    // set number of multi parton interactions
	    evt->set_mpi( pypars.msti[31-1] );
	    // set cross section information
	    evt->set_cross_section( HepMC::getPythiaCrossSection() );
	    // write the event out to the ascii files
	    ascii_io << evt;
	    // we also need to delete the created event from memory
	    delete evt;
	}
	//........................................TERMINATION
	// write out some information from Pythia to the screen
	call_pystat( 1 );    
    } // end scope of ascii_io
}

 
void event_selection()
{
    std::cout << std::endl;
    std::cout << "Begin event_selection()" << std::endl;
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
    // Instantiate an IO strategy for reading from HEPEVT.
    HepMC::IO_HEPEVT hepevtio;
    // declare an instance of the event selection predicate
    IsGoodEventMyPythia is_good_event;
    //........................................EVENT LOOP
    int icount=0;
    int num_good_events=0;
    for ( int i = 1; i <= 100; i++ ) {
	icount++;
	if ( i%50==1 ) std::cout << "Processing Event Number " 
				 << i << std::endl;
	call_pyevnt(); // generate one event with Pythia
	// pythia pyhepc routine convert common PYJETS in common HEPEVT
	call_pyhepc( 1 );
	HepMC::GenEvent* evt = hepevtio.read_next_event();
	// define the units (Pythia uses GeV and mm)
	evt->use_units(HepMC::Units::GEV, HepMC::Units::MM);
	// set number of multi parton interactions
	evt->set_mpi( pypars.msti[31-1] );
	// set cross section information
	evt->set_cross_section( HepMC::getPythiaCrossSection() );
	// do event selection
	if ( is_good_event(evt) ) {
	    std::cout << "Good Event Number " << i << std::endl;
	    ++num_good_events;
	}
	// we also need to delete the created event from memory
	delete evt;
    }
    //........................................TERMINATION
    // write out some information from Pythia to the screen
    call_pystat( 1 );    
    //........................................PRINT RESULTS
    std::cout << num_good_events << " out of " << icount 
	      << " processed events passed the cuts. Finished." << std::endl;
}

void pythia_in()
{
    std::cout << std::endl;
    std::cout << "Begin pythia_in()" << std::endl;
    std::cout << "reading example_MyPythia.dat" << std::endl;
    //........................................define an input scope
    {
        // open input stream
	std::ifstream istr( "example_MyPythia.dat" );
	if( !istr ) {
	  std::cerr << "example_ReadMyPythia: cannot open example_MyPythia.dat" << std::endl;
	  exit(-1);
	}
	HepMC::IO_GenEvent ascii_in(istr);
        // open output stream (alternate method)
	HepMC::IO_GenEvent ascii_out("example_MyPythia2.dat",std::ios::out);
	// now read the file
	int icount=0;
	HepMC::GenEvent* evt = ascii_in.read_next_event();
	while ( evt ) {
            icount++;
            if ( icount%50==1 ) std::cout << "Processing Event Number " << icount
                                	  << " its # " << evt->event_number() 
                                	  << std::endl;
	    // write the event out to the ascii file
	    ascii_out << evt;
            delete evt;
            ascii_in >> evt;
	}
	//........................................PRINT RESULT
	std::cout << icount << " events found. Finished." << std::endl;
    } // ascii_out and istr destructors are called here
}

void pythia_in_out()
{
    std::cout << std::endl;
    std::cout << "Begin pythia_in_out()" << std::endl;
    //........................................HEPEVT
    // Pythia 6.3 uses HEPEVT with 4000 entries and 8-byte floating point
    //  numbers. We need to explicitly pass this information to the 
    //  HEPEVT_Wrapper.
    //
    HepMC::HEPEVT_Wrapper::set_max_number_entries(4000);
    HepMC::HEPEVT_Wrapper::set_sizeof_real(8);
    //
    //........................................PYTHIA INITIALIZATIONS
    initPythia();

    //........................................HepMC INITIALIZATIONS
    //
    // Instantiate an IO strategy for reading from HEPEVT.
    HepMC::IO_HEPEVT hepevtio;
    //
    //........................................define the output scope
    {
	// Instantial an IO strategy to write the data to file
	HepMC::IO_GenEvent ascii_io("example_MyPythiaRead.dat",std::ios::out);
	//
	//........................................EVENT LOOP
	for ( int i = 1; i <= 100; i++ ) {
	    if ( i%50==1 ) std::cout << "Processing Event Number " 
				     << i << std::endl;
	    call_pyevnt();      // generate one event with Pythia
	    // pythia pyhepc routine converts common PYJETS in common HEPEVT
	    call_pyhepc( 1 );
	    HepMC::GenEvent* evt = hepevtio.read_next_event();
	    // define the units (Pythia uses GeV and mm)
	    evt->use_units(HepMC::Units::GEV, HepMC::Units::MM);
	    // set cross section information
	    evt->set_cross_section( HepMC::getPythiaCrossSection() );
	    // add some information to the event
	    evt->set_event_number(i);
	    evt->set_signal_process_id(20);
	    // write the event out to the ascii file
	    ascii_io << evt;
	    // we also need to delete the created event from memory
	    delete evt;
	}
	//........................................TERMINATION
	// write out some information from Pythia to the screen
	call_pystat( 1 );    
    }  // ascii_io destructor is called here
    //
    //........................................define an input scope
    {
	// now read the file we wrote
	HepMC::IO_GenEvent ascii_in("example_MyPythiaRead.dat",std::ios::in);
	HepMC::IO_GenEvent ascii_io2("example_MyPythiaRead2.dat",std::ios::out);
	int icount=0;
	HepMC::GenEvent* evt = ascii_in.read_next_event();
	while ( evt ) {
            icount++;
            if ( icount%50==1 ) std::cout << "Processing Event Number " << icount
                                	  << " its # " << evt->event_number() 
                                	  << std::endl;
	    // write the event out to the ascii file
	    ascii_io2 << evt;
            delete evt;
            ascii_in >> evt;
	}
	//........................................PRINT RESULT
	std::cout << icount << " events found. Finished." << std::endl;
    } // ascii_io2 and ascii_in destructors are called here
}

void pythia_particle_out()
{
    std::cout << std::endl;
    std::cout << "Begin pythia_particle_out()" << std::endl;
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

    //........................................HepMC INITIALIZATIONS
    //
    // Instantiate an IO strategy for reading from HEPEVT.
    HepMC::IO_HEPEVT hepevtio;
    //
    { // begin scope of ascii_io
	// Instantiate an IO strategy to write the data to file 
	HepMC::IO_AsciiParticles ascii_io("example_PythiaParticle.dat",std::ios::out);
	//
	//........................................EVENT LOOP
	for ( int i = 1; i <= 100; i++ ) {
	    if ( i%50==1 ) std::cout << "Processing Event Number " 
				     << i << std::endl;
	    call_pyevnt();      // generate one event with Pythia
	    // pythia pyhepc routine converts common PYJETS in common HEPEVT
	    call_pyhepc( 1 );
	    HepMC::GenEvent* evt = hepevtio.read_next_event();
	    // define the units (Pythia uses GeV and mm)
	    evt->use_units(HepMC::Units::GEV, HepMC::Units::MM);
	    // set cross section information
	    evt->set_cross_section( HepMC::getPythiaCrossSection() );
	    // add some information to the event
	    evt->set_event_number(i);
	    evt->set_signal_process_id(20);
	    // write the event out to the ascii file
	    ascii_io << evt;
	    // we also need to delete the created event from memory
	    delete evt;
	}
	//........................................TERMINATION
	// write out some information from Pythia to the screen
	call_pystat( 1 );    
    } // end scope of ascii_io
}

