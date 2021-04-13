#include "ExternalRecombiner.hh"

void ExternalRecombiner::recombine(const fastjet::PseudoJet & pa, const fastjet::PseudoJet & pb, fastjet::PseudoJet & pab) const {

  switch(m_extra) {
  case 10:
    pab.reset(pa.px()+pb.px(),
	      pa.py()+pb.py(),
	      pa.pz()+pb.pz(),
	      pa.E ()+pb.E ());
    return;
  case 11:
    pab.reset(pa.px()+pb.px(),
              pa.py()+pb.py(),
              pa.pz()+pb.pz(),
              pa.E ()+pb.E ());
    return;
  case 12:
    pab.reset(pa.px()+pb.px(),
              pa.py()+pb.py(),
              pa.pz()+pb.pz(),
              pa.E ()+pb.E ());
    return;
    //default return E-scheme
  default:
    pab.reset(pa.px()+pb.px(),
              pa.py()+pb.py(),
              pa.pz()+pb.pz(),
              pa.E ()+pb.E ());
  }
  return;
}
