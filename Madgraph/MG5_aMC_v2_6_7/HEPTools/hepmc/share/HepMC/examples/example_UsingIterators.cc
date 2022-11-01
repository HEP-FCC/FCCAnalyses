//////////////////////////////////////////////////////////////////////////
// Matt.Dobbs@Cern.CH, Feb 2000
// This example shows low to use the particle and vertex iterators
//////////////////////////////////////////////////////////////////////////
// To Compile: go to the HepMC directory and type:
// gmake examples/example_UsingIterators.exe
//

#include "HepMC/IO_GenEvent.h"
#include "HepMC/GenEvent.h"
#include <math.h>
#include <algorithm>
#include <list>

//! example class

/// \class  IsPhoton
/// this predicate returns true if the input particle is a photon
/// in the central region (eta < 2.5) with pT > 10 GeV
class IsPhoton {
public:
    /// returns true if the GenParticle is a photon with more than 10 GeV transverse momentum
    bool operator()( const HepMC::GenParticle* p ) { 
	if ( p->pdg_id() == 22 
	     && p->momentum().perp() > 10. ) return 1;
	return 0;
    }
};

//! example class

/// \class  IsW_Boson
/// this predicate returns true if the input particle is a W+/W-
class IsW_Boson {
public:
    /// returns true if the GenParticle is a W
    bool operator()( const HepMC::GenParticle* p ) { 
	if ( abs(p->pdg_id()) == 24 ) return 1;
	return 0;
    }
};

//! example class

/// \class  IsStateFinal
/// this predicate returns true if the input has no decay vertex
class IsStateFinal {
public:
    /// returns true if the GenParticle does not decay
    bool operator()( const HepMC::GenParticle* p ) { 
	if ( !p->end_vertex() && p->status()==1 ) return 1;
	return 0;
    }
};

int main() {
    { // begin scope of ascii_in
	// an event has been prepared in advance for this example, read it
	// into memory using the IO_GenEvent input strategy
	HepMC::IO_GenEvent ascii_in("example_UsingIterators.txt",std::ios::in);
	if ( ascii_in.rdstate() == std::ios::failbit ) {
	    std::cerr << "ERROR input file example_UsingIterators.txt is needed "
		      << "and does not exist. "
		      << "\n Look for it in HepMC/examples, Exit." << std::endl;
	    return 1;
	}

	HepMC::GenEvent* evt = ascii_in.read_next_event();

	// if you wish to have a look at the event, then use evt->print();

	// use GenEvent::vertex_iterator to fill a list of all 
	// vertices in the event
	std::list<HepMC::GenVertex*> allvertices;
	for ( HepMC::GenEvent::vertex_iterator v = evt->vertices_begin();
	      v != evt->vertices_end(); ++v ) {
	    allvertices.push_back(*v);
	}

	// we could do the same thing with the STL algorithm copy
	std::list<HepMC::GenVertex*> allvertices2;
	copy( evt->vertices_begin(), evt->vertices_end(), 
	      back_inserter(allvertices2) );

	// fill a list of all final state particles in the event, by requiring
	// that each particle satisfyies the IsStateFinal predicate
	IsStateFinal isfinal;
	std::list<HepMC::GenParticle*> finalstateparticles;
	for ( HepMC::GenEvent::particle_iterator p = evt->particles_begin();
	      p != evt->particles_end(); ++p ) {
	    if ( isfinal(*p) ) finalstateparticles.push_back(*p);
	}

	// an STL-like algorithm called HepMC::copy_if is provided in the
	// GenEvent.h header to do this sort of operation more easily,
	// you could get the identical results as above by using:
	std::list<HepMC::GenParticle*> finalstateparticles2;
	HepMC::copy_if( evt->particles_begin(), evt->particles_end(), 
			back_inserter(finalstateparticles2), IsStateFinal() );

	// lets print all photons in the event that satisfy the IsPhoton criteria
	IsPhoton isphoton;
	for ( HepMC::GenEvent::particle_iterator p = evt->particles_begin();
	      p != evt->particles_end(); ++p ) {
	    if ( isphoton(*p) ) (*p)->print();
	}

	// the GenVertex::particle_iterator and GenVertex::vertex_iterator
	// are slightly different from the GenEvent:: versions, in that
	// the iterator starts at the given vertex, and walks through the attached 
	// vertex returning particles/vertices.
	// Thus only particles/vertices which are in the same graph as the given
	// vertex will be returned. A range is specified with these iterators,
	// the choices are:
	//    parents, children, family, ancestors, descendants, relatives 
	// here are some examples.

	// use GenEvent::particle_iterator to find all W's in the event,
	// then 
	// (1) for each W user the GenVertex::particle_iterator with a range of
	//     parents to return and print the immediate mothers of these W's.
	// (2) for each W user the GenVertex::particle_iterator with a range of
	//     descendants to return and print all descendants of these W's.
	IsW_Boson isw;
	for ( HepMC::GenEvent::particle_iterator p = evt->particles_begin();
	      p != evt->particles_end(); ++p ) {
	    if ( isw(*p) ) {
		std::cout << "A W boson has been found: " << std::endl;
		(*p)->print();
		// return all parents
		// we do this by pointing to the production vertex of the W 
		// particle and asking for all particle parents of that vertex
		std::cout << "\t Its parents are: " << std::endl;
		if ( (*p)->production_vertex() ) {
		    for ( HepMC::GenVertex::particle_iterator mother 
			      = (*p)->production_vertex()->
			      particles_begin(HepMC::parents);
			  mother != (*p)->production_vertex()->
			      particles_end(HepMC::parents); 
			  ++mother ) {
			std::cout << "\t";
			(*mother)->print();
		    }
		}
		// return all descendants
		// we do this by pointing to the end vertex of the W 
		// particle and asking for all particle descendants of that vertex
		std::cout << "\t\t Its descendants are: " << std::endl;
		if ( (*p)->end_vertex() ) {
		    for ( HepMC::GenVertex::particle_iterator des 
			      =(*p)->end_vertex()->
			      particles_begin(HepMC::descendants);
			  des != (*p)->end_vertex()->
			      particles_end(HepMC::descendants);
			  ++des ) {
			std::cout << "\t\t";
			(*des)->print();
		    }
		}
	    }
	}
	// cleanup
        delete evt;
	// in analogy to the above, similar use can be made of the
	// HepMC::GenVertex::vertex_iterator, which also accepts a range.
    } // end scope of ascii_in

    return 0;
}
