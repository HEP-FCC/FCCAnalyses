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


def permute(num):
    if len(num) == 2:
        # get the permutations of the last 2 numbers by swapping them
        yield num
        num[0], num[1] = num[1], num[0]
        yield num
    else:
        for i in range(0, len(num)):
            # fix the first number and get the permutations of the rest of numbers
            for perm in permute(num[0:i] + num[i+1:len(num)]):
                yield [num[i]] + perm

def getNbTagEx(Nbtag, jet, njets_used):
    nj=len(jet)
    if njets_used>0 and njets_used<nj: nj=njets_used
    wj=[]
    # security
    if Nbtag>len(jet) :
      print "ERROR : Nbtag>njets"
      return -1
    # form eff table
    for i in range(nj):
      jpt= jet[i][0].pt()
      jeta=jet[i][0].eta()
      jpdg=jet[i][1]
      wj.append(getbTagEff(jpt,jeta,jpdg))
      #print "len(jet)="+str(len(jet))+", nj="+str(nj)+" , Nbtag="+str(Nbtag)+" -> jpt="+str(jpt)+" , jeta="+str(jeta)+" , jpdg="+str(jpdg)+" -----> wj="+str(wj[i])
    # check unicity of TRFs
    for i in range(len(wj)):
     for j in range(len(wj)):
      if i<j and wj[i]==wj[j]: print "DANGER : 2 jets have same TRF and destroy the method to compute btag TRF weight"

    final_wtag=[]
    # loop on Nbtag to handle every exclusive btag level cases
    for ntag in range(Nbtag+1):
      # compute permutations
      wtag=[]
      for p in permute(wj):
        # tag weight of a permutation
        p_wtag=1.
        for j in range(len(p)):
          if j<ntag: p_wtag*=p[j]
          else     : p_wtag*=1.-p[j]
        found=False
        # avoid double counting due to the way of forming permutations
        # not valid if 2 jets have exactly same TRF value -> check done above
        if len(wtag)>0:
          for i_wtag in range(len(wtag)):
            if abs(wtag[i_wtag]-p_wtag)<1E-10 : found=True
        if found==False: wtag.append(p_wtag)
      # compute TRF weight if this tag level
      wtag_level=0.
      for i_wtag in range(len(wtag)): wtag_level+=wtag[i_wtag]
      # and store it in final list of exclusive level tag weight
      final_wtag.append([ntag,wtag_level])
    for i in final_wtag:
      if i[0]==Nbtag: return i[1]
