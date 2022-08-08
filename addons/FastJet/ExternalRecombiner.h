#ifndef FastJet_ExternalRecombiner_h
#define FastJet_ExternalRecombiner_h

#include "fastjet/JetDefinition.hh"

class ExternalRecombiner : public fastjet::JetDefinition::Recombiner {
public:
  ExternalRecombiner(int arg_extra) { m_extra = arg_extra; }

  std::string description() const override {
    switch (m_extra) {
      case 10:
        return "E0 scheme recombination";
      case 11:
        return "p scheme recombination";
      default:
        return "ExternalRecombiner: unrecognized recombination scheme ";
    }
  }

  /// recombine pa and pb and put result into pab
  void recombine(const fastjet::PseudoJet& pa, const fastjet::PseudoJet& pb, fastjet::PseudoJet& pab) const override;

private:
  int m_extra;
};

#endif
