import math
import itertools

#############################################
# example usage :
# ----------------
# weight_1tagex=0.
# weight_2tagex=0.
# ipdg=0
# jet=[]
# if (len(jets_pf04)>1):
#   for i in range(len(jets_pf04)):
#     ipdg = jets_pf04_pdg[i].flavour
#     jet.append([jets_pf04[i],ipdg])
#   weight_1tagex=getNbTagEx(1,jet,2)
#   weight_2tagex=getNbTagEx(2,jet,2)
# weight_1tagin=weight_1tagex+weight_2tagex
# ----------------
# gen_particles = 'skimmedGenParticles',
# ...
# from heppy.FCChhAnalyses.analyzers.FlavourTagger import FlavourTagger
# jets_pf04_1000_pdg = cfg.Analyzer(
#     FlavourTagger,
#     'jets_pf04_1000_pdg',
#     input_jets = 'jets_pf04_1000',
#     input_genparticles = 'gen_particles',
#     output_jets = 'jets_pf04_1000_pdg',
#     dr_match = 0.4,
#     pdg_tags = [5, 4, 0],
#     ptr_min = 0.1,
# )
#############################################

#_______________________________________________
def getbTagEff_degrade1(pt, eta, pdg):
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
      if abs(eta) <= 2.5 and pt > 500.      and pt <= 12500.                 : return 0.85*(1.-pt/12500.)
      if abs(eta) <= 2.5 and pt > 12500.                                     : return 0.
      if abs(eta)  > 2.5 and abs(eta) <= 4. and pt > 10.     and pt <= 500.  : return 0.64
      if abs(eta)  > 2.5 and abs(eta) <= 4. and pt > 500.    and pt <= 12500.: return 0.64*(1.-pt/12500.)
      if abs(eta)  < 2.5 and abs(eta) <= 4. and pt > 12500.                  : return 0.
      if abs(eta)  > 4.                                                      : return 0.
    else: print "Not supported jet pdg="+str(pdg)+" -> CHECK!!!!!!!!!!!"


#_______________________________________________
def getbTagEff_degrade2(pt, eta, pdg):
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
      if abs(eta) <= 2.5 and pt > 500.      and pt <= 10000.                 : return 0.85*(1.-pt/10000.)
      if abs(eta) <= 2.5 and pt > 10000.                                     : return 0.
      if abs(eta)  > 2.5 and abs(eta) <= 4. and pt > 10.     and pt <= 500.  : return 0.64
      if abs(eta)  > 2.5 and abs(eta) <= 4. and pt > 500.    and pt <= 10000.: return 0.64*(1.-pt/10000.)
      if abs(eta)  < 2.5 and abs(eta) <= 4. and pt > 10000.                  : return 0.
      if abs(eta)  > 4.                                                      : return 0.
    else: print "Not supported jet pdg="+str(pdg)+" -> CHECK!!!!!!!!!!!"

#_______________________________________________
def getbTagEff_degrade3(pt, eta, pdg):
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
      if abs(eta) <= 2.5 and pt > 500.      and pt <= 7500.                  : return 0.85*(1.-pt/7500.)
      if abs(eta) <= 2.5 and pt > 7500.                                      : return 0.
      if abs(eta)  > 2.5 and abs(eta) <= 4. and pt > 10.     and pt <= 500.  : return 0.64
      if abs(eta)  > 2.5 and abs(eta) <= 4. and pt > 500.    and pt <= 7500. : return 0.64*(1.-pt/7500.)
      if abs(eta)  < 2.5 and abs(eta) <= 4. and pt > 7500.                   : return 0.
      if abs(eta)  > 4.                                                      : return 0.
    else: print "Not supported jet pdg="+str(pdg)+" -> CHECK!!!!!!!!!!!"



#############################################
# eff tables taken from here :
# https://github.com/delphes/delphes/blob/master/cards/FCC/FCChh.tcl#L1018

#_______________________________________________
def getbTagEff_degrade1(pt, eta, pdg):
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
      if abs(eta) <= 2.5 and pt > 500.      and pt <= 12500.                 : return 0.85*(1.-pt/12500.)
      if abs(eta) <= 2.5 and pt > 12500.                                     : return 0.
      if abs(eta)  > 2.5 and abs(eta) <= 4. and pt > 10.     and pt <= 500.  : return 0.64
      if abs(eta)  > 2.5 and abs(eta) <= 4. and pt > 500.    and pt <= 12500.: return 0.64*(1.-pt/12500.)
      if abs(eta)  < 2.5 and abs(eta) <= 4. and pt > 12500.                  : return 0.
      if abs(eta)  > 4.                                                      : return 0.
    else: print "Not supported jet pdg="+str(pdg)+" -> CHECK!!!!!!!!!!!"


#_______________________________________________
def getbTagEff_degrade2(pt, eta, pdg):
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
      if abs(eta) <= 2.5 and pt > 500.      and pt <= 10000.                 : return 0.85*(1.-pt/10000.)
      if abs(eta) <= 2.5 and pt > 10000.                                     : return 0.
      if abs(eta)  > 2.5 and abs(eta) <= 4. and pt > 10.     and pt <= 500.  : return 0.64
      if abs(eta)  > 2.5 and abs(eta) <= 4. and pt > 500.    and pt <= 10000.: return 0.64*(1.-pt/10000.)
      if abs(eta)  < 2.5 and abs(eta) <= 4. and pt > 10000.                  : return 0.
      if abs(eta)  > 4.                                                      : return 0.
    else: print "Not supported jet pdg="+str(pdg)+" -> CHECK!!!!!!!!!!!"

#_______________________________________________
def getbTagEff_degrade3(pt, eta, pdg):
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
      if abs(eta) <= 2.5 and pt > 500.      and pt <= 7500.                  : return 0.85*(1.-pt/7500.)
      if abs(eta) <= 2.5 and pt > 7500.                                      : return 0.
      if abs(eta)  > 2.5 and abs(eta) <= 4. and pt > 10.     and pt <= 500.  : return 0.64
      if abs(eta)  > 2.5 and abs(eta) <= 4. and pt > 500.    and pt <= 7500. : return 0.64*(1.-pt/7500.)
      if abs(eta)  < 2.5 and abs(eta) <= 4. and pt > 7500.                   : return 0.
      if abs(eta)  > 4.                                                      : return 0.
    else: print "Not supported jet pdg="+str(pdg)+" -> CHECK!!!!!!!!!!!"




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


def getNbTagEx(Nbtag, jet, njets_used, jet_to_use=None):

    # ensure sorting in jet pT
    jet.sort(key=lambda x: x[0].pt(), reverse = True)

    #-----------------------------
    # init
    #-----------------------------
    nj=len(jet)
    if njets_used>0 and njets_used<nj: nj=njets_used
    wj=[]
    wj_idx=[]
    # security
    if Nbtag>len(jet) or len(jet)==0: return 0.
    # security again : for example when user ask to compute 1 btag on the second jet of an event with only 1 jet
    if jet_to_use is not None and jet_to_use>=len(jet): return 0.

    #-----------------------------
    # form eff table
    #-----------------------------
    degrade=0
    #degrade=1
    #degrade=2
    #degrade=3
    #
    for i in range(nj):
      if degrade==0: wj.append( getbTagEff(jet[i][0].pt(), jet[i][0].eta(), jet[i][1]) )
      if degrade==1: wj.append( getbTagEff_degrade1(jet[i][0].pt(), jet[i][0].eta(), jet[i][1]) )
      if degrade==2: wj.append( getbTagEff_degrade2(jet[i][0].pt(), jet[i][0].eta(), jet[i][1]) )
      if degrade==3: wj.append( getbTagEff_degrade3(jet[i][0].pt(), jet[i][0].eta(), jet[i][1]) )
      wj_idx.append(i)
      #print "len(jet)="+str(len(jet))+", nj="+str(nj)+" , Nbtag="+str(Nbtag)+" -> jpt="+str(jet[i][0].pt())+" , jeta="+str(jet[i][0].eta())+" , jpdg="+str(jet[i][1])+" -----> wj="+str(wj[i])

    #-----------------------------
    # compute permutations list
    #-----------------------------
    perm_list=list(itertools.combinations(wj_idx,Nbtag))

    # check
    #-----------------------------
    cnk=math.factorial(nj)/(math.factorial(Nbtag)*math.factorial(nj-Nbtag))
    if len(perm_list)!=cnk: print "WARNING : TRFbtag found wrong number of permutation combinations :"+str(len(perm_list))+" , expect cnk="+str(cnk)+" for nj="+str(nj)+" and Nbtag="+str(Nbtag)

    #-----------------------------
    # compute weight of a permutation
    #-----------------------------
    wtag=[]

    # check if we are in the 0tag case
    case_tag0 = False
    if len(perm_list)==1 and len(perm_list[0])==0: case_tag0 = True

    # >=1 tag cases
    #-----------------------------
    if case_tag0 == False :
      for i_perm in perm_list:
        # loop on jets
        p_wtag=1.
        for j_idx in wj_idx:
          j = wj[j_idx]
          TRF=False
          # check if TRF or 1-TRF
          for i in i_perm:
            if i==j_idx: TRF=True
          # compute
          if TRF: p_wtag*=j
          else  : p_wtag*=1.-j
        wtag.append(p_wtag)

    # 0 tag case perm_list has only 1 empty item
    #-----------------------------
    else :
      p_wtag=1.
      for j in wj:
        p_wtag*=1.-j
      wtag.append(p_wtag)
      
    # check again
    #-----------------------------
    if len(wtag)!=cnk: print "WARNING : TRFbtag found wrong number of permutation combinations after filling proper weigths:"+str(len(wtag))+" , expect cnk="+str(cnk)+" for nj="+str(nj)+" and Nbtag="+str(Nbtag)

    #-----------------------------
    # compute TRF weight of this tag level
    #-----------------------------
    final_wtag=0.
    if jet_to_use is None :
      for i_wtag in range(len(wtag)): final_wtag+=wtag[i_wtag]
    else :
      final_wtag=wtag[jet_to_use]
    #print "\n---------------- wtags computed (",Nbtag,"btag) ---------------------"
    #if jet_to_use is not None : print "-> computed only on jet",jet_to_use
    #print "wj="+str(wj)
    #print "wtag="+str(wtag)
    #print "final_wtag="+str(final_wtag)
    return final_wtag
