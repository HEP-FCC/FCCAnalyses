//////////////////////////////////////////////////////////////////////////
// Matt.Dobbs@Cern.CH, Feb 2000
// Example of building an event and a particle data table from scratch
// This is meant to be of use for persons implementing HepMC inside a MC 
// event generator
//////////////////////////////////////////////////////////////////////////
// To Compile: go to the HepMC directory and type:
// gmake examples/example_BuildEventFromScratch.exe
//

#include <iostream>

#include "VectorConversion.h"
#include "HepMC/GenEvent.h"
#include "CLHEP/Vector/LorentzVector.h"

// in this example we use the HepMC namespace, so that we do not have to 
// precede all HepMC classes with HepMC::

// This example also shows how to use the CLHEP Lorentz vector with HepMC2

using namespace HepMC;
using namespace CLHEP;

int main() {
    //
    // In this example we will place the following event into HepMC "by hand"
    //
    //     name status pdg_id  parent Px       Py    Pz       Energy      Mass
    //  1  !p+!    3   2212    0,0    0.000    0.000 7000.000 7000.000    0.938
    //  2  !p+!    3   2212    0,0    0.000    0.000-7000.000 7000.000    0.938
    //=========================================================================
    //  3  !d!     3      1    1,1    0.750   -1.569   32.191   32.238    0.000
    //  4  !u~!    3     -2    2,2   -3.047  -19.000  -54.629   57.920    0.000
    //  5  !W-!    3    -24    1,2    1.517   -20.68  -20.605   85.925   80.799
    //  6  !gamma! 1     22    1,2   -3.813    0.113   -1.833    4.233    0.000
    //  7  !d!     1      1    5,5   -2.445   28.816    6.082   29.552    0.010
    //  8  !u~!    1     -2    5,5    3.962  -49.498  -26.687   56.373    0.006

    // now we build the graph, which will look like
    //                       p7                         #
    // p1                   /                           #
    //   \v1__p3      p5---v4                           #
    //         \_v3_/       \                           #
    //         /    \        p8                         #
    //    v2__p4     \                                  #
    //   /            p6                                #
    // p2                                               #
    //                                                  #

    // First create the event container, with Signal Process 20, event number 1
    //
    // Note that the HepLorentzVectors will be automatically converted to 
    // HepMC::FourVector within GenParticle and GenVertex
    GenEvent* evt = new GenEvent( 20, 1 );
    // define the units
    evt->use_units(HepMC::Units::GEV, HepMC::Units::MM);
    //
    // create vertex 1 and vertex 2, together with their inparticles
    GenVertex* v1 = new GenVertex();
    evt->add_vertex( v1 );
    v1->add_particle_in( new GenParticle( HepLorentzVector(0,0,7000,7000),
				       2212, 3 ) );
    GenVertex* v2 = new GenVertex();
    evt->add_vertex( v2 );
    v2->add_particle_in( new GenParticle( HepLorentzVector(0,0,-7000,7000),
				       2212, 3 ) );
    //
    // create the outgoing particles of v1 and v2
    GenParticle* p3 = 
	new GenParticle( HepLorentzVector(.750,-1.569,32.191,32.238), 1, 3 );
    v1->add_particle_out( p3 );
    GenParticle* p4 = 
	new GenParticle( HepLorentzVector(-3.047,-19.,-54.629,57.920), -2, 3 );
    v2->add_particle_out( p4 );
    //
    // create v3
    GenVertex* v3 = new GenVertex();
    evt->add_vertex( v3 );
    v3->add_particle_in( p3 );
    v3->add_particle_in( p4 );
    v3->add_particle_out( 
	new GenParticle( HepLorentzVector(-3.813,0.113,-1.833,4.233 ), 22, 1 )
	);
    GenParticle* p5 = 
	new GenParticle( HepLorentzVector(1.517,-20.68,-20.605,85.925), -24,3);
    v3->add_particle_out( p5 );
    //
    // create v4
    GenVertex* v4 = new GenVertex(HepLorentzVector(0.12,-0.3,0.05,0.004));
    evt->add_vertex( v4 );
    v4->add_particle_in( p5 );
    v4->add_particle_out( 
	new GenParticle( HepLorentzVector(-2.445,28.816,6.082,29.552), 1,1 )
	);
    v4->add_particle_out( 
	new GenParticle( HepLorentzVector(3.962,-49.498,-26.687,56.373), -2,1 )
	);
    //    
    // tell the event which vertex is the signal process vertex
    evt->set_signal_process_vertex( v3 );
    // the event is complete, we now print it out to the screen
    evt->print();
    
    // example conversion back to Lorentz vector
    // add all outgoing momenta
    std::cout << std::endl;
    std::cout << " Add output momenta " << std::endl;
    HepLorentzVector sum;
    for ( GenEvent::particle_const_iterator p = evt->particles_begin(); 
	      p != evt->particles_end(); ++p ){
	if( (*p)->status() == 1 ) {
	    sum += convertTo( (*p)->momentum() );
	    (*p)->print();
	}
    }
    std::cout << "Vector Sum: " << sum << std::endl;

    // now clean-up by deleteing all objects from memory
    //
    // deleting the event deletes all contained vertices, and all particles
    // contained in those vertices
    delete evt;

    return 0;
}
