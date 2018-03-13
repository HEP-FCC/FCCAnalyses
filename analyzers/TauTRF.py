def getMisTagEff(pt, eta):
    if pt <= 10.0:                                                           return 0.
    elif abs(eta) < 2.5 and pt > 10.0 and pt < 5000.0:                       return 0.01
    elif abs(eta) < 2.5 and pt > 5000.0 and pt < 34000.0:                    return 0.01*(8./9. - pt/30000.)
    elif abs(eta) < 2.5 and pt > 34000.0:                                    return 0.
    elif abs(eta) > 2.5 and abs(eta) < 4.0 and pt > 10.0 and pt < 5000.0:    return 0.0075
    elif abs(eta) > 2.5 and abs(eta) < 4.0 and pt > 5000.0 and pt < 34000.0: return 0.0075*(8./9. - pt/30000.)
    elif abs(eta) > 2.5 and abs(eta) < 4.0 and pt > 34000.0:                 return 0.
    elif abs(eta) > 4.0:                                                     return 0.
    return 0.

def getOneTagEx(jet1, jet2):
    eff1=getMisTagEff(jet1.pt(), jet1.eta())
    eff2=getMisTagEff(jet2.pt(), jet2.eta())
    return eff1*(1-eff2)+eff2*(1-eff1)

def getTwoTagEx(jet1, jet2):
    eff1=getMisTagEff(jet1.pt(), jet1.eta())
    eff2=getMisTagEff(jet2.pt(), jet2.eta())
    return eff1*eff2
