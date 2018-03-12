def getbTagEff(pt, eta, pdg):
    if pdg==0:
      if pt <= 10.: return 0.
      if abs(eta) <= 2.5 and pt > 10.       and pt <= 500.                   : return 0.01
      if abs(eta) <= 2.5 and pt > 500.      and pt <= 15000.                 : return 0.01*(1.-pt/15000.)
      if abs(eta) <= 2.5 and pt > 15000.                                     : return 0.
      if abs(eta)  > 2.5 and abs(eta) <= 4. and pt > 10.     and pt <= 500.  : return 0.0075
      if abs(eta)  > 2.5 and abs(eta) <= 4. and pt > 500.    and pt <= 15000.: return 0.0075*(1.-pt/15000.)
      if abs(eta)  < 2.5 and abs(eta) <= 4. and pt > 15000.                  : return 0.
      if abs(eta)  > 4.                                                      : return 0.
    elif pdg==4:
      if pt <= 10.: return 0.
      if abs(eta) <= 2.5 and pt > 10.       and pt <= 500.                   : return 0.05
      if abs(eta) <= 2.5 and pt > 500.      and pt <= 15000.                 : return 0.05*(1.-pt/15000.)
      if abs(eta) <= 2.5 and pt > 15000.                                     : return 0.
      if abs(eta)  > 2.5 and abs(eta) <= 4. and pt > 10.     and pt <= 500.  : return 0.03
      if abs(eta)  > 2.5 and abs(eta) <= 4. and pt > 500.    and pt <= 15000.: return 0.03*(1.-pt/15000.)
      if abs(eta)  < 2.5 and abs(eta) <= 4. and pt > 15000.                  : return 0.
      if abs(eta)  > 4.                                                      : return 0.
    elif pdg==5:
      if pt <= 10.: return 0.
      if abs(eta) <= 2.5 and pt > 10.       and pt <= 500.                   : return 0.85
      if abs(eta) <= 2.5 and pt > 500.      and pt <= 15000.                 : return 0.85*(1.-pt/15000.)
      if abs(eta) <= 2.5 and pt > 15000.                                     : return 0.
      if abs(eta)  > 2.5 and abs(eta) <= 4. and pt > 10.     and pt <= 500.  : return 0.64
      if abs(eta)  > 2.5 and abs(eta) <= 4. and pt > 500.    and pt <= 15000.: return 0.64*(1.-pt/15000.)
      if abs(eta)  < 2.5 and abs(eta) <= 4. and pt > 15000.                  : return 0.
      if abs(eta)  > 4.                                                      : return 0.
    else: print "Not supported jet pdg="+str(pdg)+" -> CHECK!!!!!!!!!!!"


def getcTagEff(pt, eta, pdg):
    if pdg==0:
      if pt <= 10.                  : return 0.
      if abs(eta) <= 4. and pt > 10.: return 0.01
      if abs(eta)  > 4. and pt > 10.: return 0.
    if pdg==4:
      if pt <= 10.                  : return 0.
      if abs(eta) <= 4. and pt > 10.: return 0.25
      if abs(eta)  > 4. and pt > 10.: return 0.
    if pdg==5:
      if pt <= 10.                  : return 0.
      if abs(eta) <= 4. and pt > 10.: return 0.03
      if abs(eta)  > 4. and pt > 10.: return 0.
    else: print "Not supported jet pdg="+str(pdg)+" -> CHECK!!!!!!!!!!!"


def getOnebTagEx(jet1, jet1_pdg, jet2, jet2_pdg):
    eff1=getbTagEff(jet1.pt(), jet1.eta(), jet1_pdg)
    eff2=getbTagEff(jet2.pt(), jet2.eta(), jet2_pdg)
    return eff1*(1-eff2)+eff2*(1-eff1)


def getTwobTagEx(jet1, jet1_pdg, jet2, jet2_pdg):
    eff1=getbTagEff(jet1.pt(), jet1.eta(), jet1_pdg)
    eff2=getbTagEff(jet2.pt(), jet2.eta(), jet2_pdg)
    return eff1*eff2

