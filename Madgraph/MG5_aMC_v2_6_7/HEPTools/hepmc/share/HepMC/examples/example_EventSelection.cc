//////////////////////////////////////////////////////////////////////////
// Matt.Dobbs@Cern.CH, Feb 2000
// Example of applying an event selection to the events written to file
// using example_MyPythia.cxx
// Events containing a photon of pT > 25 GeV pass the selection and are
// written to "example_EventSelection.dat"
//////////////////////////////////////////////////////////////////////////
// To Compile: go to the HepMC directory and type:
// gmake examples/example_EventSelection.exe
//

#include "HepMC/IO_GenEvent.h"
#include "HepMC/GenEvent.h"

//! example class

/// \class  IsEventGood
/// event selection predicate. returns true if the event contains
/// a photon with pT > 50 GeV
class IsEventGood {
public:
    /// check this event for goodness
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

int main() { 
    // declare an input strategy to read the data produced with the 
    // example_MyPythia
    { // begin scope of ascii_in and ascii_out
	HepMC::IO_GenEvent ascii_in("example_MyPythia.dat",std::ios::in);
	// declare another IO_GenEvent for writing out the good events
	HepMC::IO_GenEvent ascii_out("example_EventSelection.dat",std::ios::out);
	// declare an instance of the event selection predicate
	IsEventGood is_good_event;
	//........................................EVENT LOOP
	int icount=0;
	int num_good_events=0;
	HepMC::GenEvent* evt = ascii_in.read_next_event();
	while ( evt ) {
	    icount++;
	    if ( icount%50==1 ) std::cout << "Processing Event Number " << icount
					  << " its # " << evt->event_number() 
					  << std::endl;
	    if ( is_good_event(evt) ) {
		ascii_out << evt;
		++num_good_events;
	    }
	    delete evt;
	    ascii_in >> evt;
	}
	//........................................PRINT RESULT
	std::cout << num_good_events << " out of " << icount 
		  << " processed events passed the cuts. Finished." << std::endl;
    } // end scope of ascii_in and ascii_out
    return 0;
}










