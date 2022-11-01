//////////////////////////////////////////////////////////////////////////
// example_PythiaStreamIO.cc
//
// garren@fnal.gov, May 2009
// 
//////////////////////////////////////////////////////////////////////////
/// example of generating events with Pythia using HepMC/PythiaWrapper.h 
/// Events are read into the HepMC event record from the FORTRAN HEPEVT 
/// common block using the IO_HEPEVT strategy 
///
/// To Compile: go to the HepMC example directory and type:
/// make example_PythiaStreamIO.exe
///
/// This example uses streaming I/O 
/// writePythiaStreamIO() sets the cross section in GenRun
/// readPythiaStreamIO() reads the file written by writePythiaStreamIO()
///
//////////////////////////////////////////////////////////////////////////


#include <fstream>
#include <iostream>
#include "HepMC/PythiaWrapper.h"
#include "HepMC/IO_HEPEVT.h"
#include "HepMC/GenEvent.h"
#include "PythiaHelper.h"

void writePythiaStreamIO();
void readPythiaStreamIO();

int main() { 

    writePythiaStreamIO();
    readPythiaStreamIO();

    return 0;
}
   

void writePythiaStreamIO() {
    // example to generate events and write output
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
	// declare an output stream
	const char outfile[] = "example_PythiaStreamIO_write.dat";
	std::ofstream ascii_io( outfile );
	if( !ascii_io ) {
	  std::cerr << "cannot open " << outfile << std::endl;
	  exit(-1);
	}
	// use the default IO_GenEvent precision
	ascii_io.precision(16);
	// write the line that defines the beginning of a GenEvent block
	HepMC::write_HepMC_IO_block_begin( ascii_io );
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
	    ascii_io << (*evt);;
	    // we also need to delete the created event from memory
	    delete evt;
	}
	// write the line that defines the end of a GenEvent block
        HepMC::write_HepMC_IO_block_end( ascii_io );
	//........................................TERMINATION
	// write out some information from Pythia to the screen
	call_pystat( 1 );    
    } // end scope of ascii_io
}

void readPythiaStreamIO() {
    // example to read events written by writePythiaStreamIO
    // and write them back out
    std::cout << std::endl;
    // input units are GeV and mm
    const char infile[] = "example_PythiaStreamIO_write.dat";
    std::ifstream is( infile );
    if( !is ) {
      std::cerr << "cannot open " << infile << std::endl;
      exit(-1);
    }
    //
    { // begin scope of ascii_io
	// declare an output stream
	const char outfile[] = "example_PythiaStreamIO_read.dat";
	std::ofstream ascii_io( outfile );
	if( !ascii_io ) {
	  std::cerr << "cannot open " << outfile << std::endl;
	  exit(-1);
	}
	ascii_io.precision(16);
	HepMC::write_HepMC_IO_block_begin( ascii_io );
	//
	//........................................EVENT LOOP
	HepMC::GenEvent evt;
	int i = 0;
	while ( is ) {
            evt.read( is );
	    // make sure we have a valid event
	    if( evt.is_valid() ) {
	        ++i;
		if ( i%50==1 ) std::cout << "Processing Event Number " 
					 << i << std::endl;
		if ( i%25==2 ) {
		    // write the cross section if it exists
		    if( evt.cross_section() ) {
			std::cout << "cross section at event " << i << " is " 
        			  << evt.cross_section()->cross_section()
				  << std::endl;
		    }
		}
		// write the event out to the ascii files
		evt.write( ascii_io );
	    }
	}
	//........................................TERMINATION
        HepMC::write_HepMC_IO_block_end( ascii_io );
    } // end scope of ascii_io
}
