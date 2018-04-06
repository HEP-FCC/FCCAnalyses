def getTauTagEff(pt, eta, pdgid):
    if pdgid==0:
        if pt <= 10.0:                                                           return 0.
        elif abs(eta) < 2.5 and pt > 10.0 and pt < 5000.0:                       return 0.01
        elif abs(eta) < 2.5 and pt > 5000.0 and pt < 34000.0:                    return 0.01*(8./9. - pt/30000.)
        elif abs(eta) < 2.5 and pt > 34000.0:                                    return 0.
        elif abs(eta) > 2.5 and abs(eta) < 4.0 and pt > 10.0 and pt < 5000.0:    return 0.0075
        elif abs(eta) > 2.5 and abs(eta) < 4.0 and pt > 5000.0 and pt < 34000.0: return 0.0075*(8./9. - pt/30000.)
        elif abs(eta) > 2.5 and abs(eta) < 4.0 and pt > 34000.0:                 return 0.
        elif abs(eta) > 4.0:                                                     return 0.
        return 0.


    elif pdgid==11:
        if pt <= 10.0:                                                           return 0.
        elif abs(eta) < 2.5 and pt > 10.0 and pt < 5000.0:                       return 0.005
        elif abs(eta) < 2.5 and pt > 5000.0 and pt < 34000.0:                    return 0.005*(8./9. - pt/30000.)
        elif abs(eta) < 2.5 and pt > 34000.0:                                    return 0.0
        elif abs(eta) > 2.5 and abs(eta) < 4.0 and pt > 10.0 and pt < 5000.0:    return 0.00375
        elif abs(eta) > 2.5 and abs(eta) < 4.0 and pt > 5000.0 and pt < 34000.0: return 0.00375*(8./9. - pt/30000.)
        elif abs(eta) > 2.5 and abs(eta) < 4.0 and pt > 34000.0:                 return 0.0
        elif abs(eta) > 4.0:                                                     return 0.
        return 0.

    elif pdgid==15:
        if pt <= 10.0:                                                           return 0.
        elif abs(eta) < 2.5 and pt > 10.0 and pt < 5000.0:                       return 0.6
        elif abs(eta) < 2.5 and pt > 5000.0 and pt < 34000.0:                    return 0.6*(8./9. - pt/30000.)
        elif abs(eta) < 2.5 and pt > 34000.0:                                    return 0.
        elif abs(eta) > 2.5 and abs(eta) < 4.0 and pt > 10.0 and pt < 5000.0:    return 0.45
        elif abs(eta) > 2.5 and abs(eta) < 4.0 and pt > 5000.0 and pt < 34000.0: return 0.45*(8./9. - pt/30000.)
        elif abs(eta) > 2.5 and abs(eta) < 4.0 and pt > 34000.0:                 return 0.0
        elif abs(eta) > 4.0:                                                     return 0.
        return 0

def getOneTagEx(jet1, jet2):
    eff1=getTauTagEff(jet1.pt(), jet1.eta(), jet1.flavour)
    eff2=getTauTagEff(jet2.pt(), jet2.eta(), jet2.flavour)
    return eff1*(1-eff2)+eff2*(1-eff1)

def getTwoTagEx(jet1, jet2):
    eff1=getTauTagEff(jet1.pt(), jet1.eta(), jet1.flavour)
    eff2=getTauTagEff(jet2.pt(), jet2.eta(), jet2.flavour)
    return eff1*eff2
