import ROOT
from array import array
import math
import sys
import uproot
import os
import json

# Import the library
import argparse
# Create the parser
parser = argparse.ArgumentParser()
# Add an argument
parser.add_argument("--ID",  type = int , help="Chunk ID",required=True)


# Parse the argument
args = parser.parse_args()
ID = args.ID

print("Process ID: ",ID)
#print("Number of submitted jobs: ", JN)
 
#resonant signals only
file_name = [
            # 'mgp8_pp_Htohh_mH_300GeV_84TeV_hhbbaa', 'mgp8_pp_Htohh_mH_350GeV_84TeV_hhbbaa', 
            # 'mgp8_pp_Htohh_mH_400GeV_84TeV_hhbbaa', 'mgp8_pp_Htohh_mH_450GeV_84TeV_hhbbaa',
            # 'mgp8_pp_Htohh_mH_500GeV_84TeV_hhbbaa', 'mgp8_pp_Htohh_mH_550GeV_84TeV_hhbbaa',
            # 'mgp8_pp_Htohh_mH_600GeV_84TeV_hhbbaa', 'mgp8_pp_Htohh_mH_650GeV_84TeV_hhbbaa',
            # 'mgp8_pp_Htohh_mH_700GeV_84TeV_hhbbaa', 'mgp8_pp_Htohh_mH_750GeV_84TeV_hhbbaa',
            # 'mgp8_pp_Htohh_mH_800GeV_84TeV_hhbbaa', 'mgp8_pp_Htohh_mH_850GeV_84TeV_hhbbaa',
            # 'mgp8_pp_Htohh_mH_800GeV_84TeV_hhbbaa', 'mgp8_pp_Htohh_mH_850GeV_84TeV_hhbbaa',
            'mgp8_pp_Htohh_mH_900GeV_84TeV_hhbbaa', 'mgp8_pp_Htohh_mH_950GeV_84TeV_hhbbaa',
            # 'mgp8_pp_Htohh_mH_1000GeV_84TeV_hhbbaa', 
            'mgp8_pp_Htohh_mH_550GeV_84TeV_hhbbaa', 
]

# file_name = ['mgp8_pp_h012j_5f_haa', 'mgp8_pp_vh012j_5f_haa', 'mgp8_pp_vbf_h01j_5f_haa', 'mgp8_pp_tth01j_5f_haa','pwp8_pp_hh_lambda000_5f_hhbbaa', 'pwp8_pp_hh_lambda100_5f_hhbbaa', 'pwp8_pp_hh_lambda240_5f_hhbbaa','pwp8_pp_hh_lambda300_5f_hhbbaa', 'mgp8_pp_jjaa_5f']#,'mgp8_pp_tt012j_5f']

lumi = 30e+06

for name in file_name:

        nameINPUT = "/eos/experiment/fcc/hh/analysis_ntuples/fcc_v07/II/bbyy_analysis/"+name+"/chunk"+str(ID)+".root"
        nameOUTPUT = "/eos/experiment/fcc/hh/analysis_ntuples/fcc_v07/II/bbyy_analysis/"+name+"/processed"+str(ID)+".root"

        # nameINPUT = "./FCCAnalysis_ntuples_forAnalysis_Mbtag/"+name+"/chunk"+str(ID)+".root"
        # nameOUTPUT = "./FCCAnalysis_ntuples_forAnalysis_Mbtag/"+name+"/processed"+str(ID)+".root"
        #input file
        if not os.path.isfile(nameINPUT):
           print("File do not exist")
           continue
        
        fin = ROOT.TFile.Open(nameINPUT)          
        fout = ROOT.TFile.Open(nameOUTPUT, "RECREATE")

        weight = array('f', [0])
        njets = array('i', [0])
        pTb1_o_m_bb = array('f', [0])
        pTb2_o_m_bb = array('f', [0])
        pTbb_o_m_HH = array('f', [0])
        pTg1_o_m_gg = array('f', [0])
        pTg2_o_m_gg = array('f', [0])
        pTgg_o_m_HH = array('f', [0])
        nLep = array('i', [0])
        pT_l1 = array('f', [0])
        pT_l2 = array('f', [0])
        sum_pt = array('f', [0])
        mindR_gb = array('f', [0])
        otherdR_gb = array('f', [0])
        GG_cosT_restHH = array('f', [0])
        B1_cosT_restBB = array('f', [0])
        G1_cosT_restGG = array('f', [0])
        DeltaPhi_gg = array('f', [0])
        DeltaEta_gg = array('f', [0])
        DeltaPhi_bb = array('f', [0])
        DeltaEta_bb = array('f', [0])
        DeltaPhi_HH = array('f', [0])
        DeltaEta_HH = array('f', [0])   
        a1_pt = array('f', [0])
        a1_e  = array('f', [0])
        a1_eta = array('f', [0])
        a1_phi = array('f', [0])
        b1_pt = array('f', [0])
        b1_e  = array('f', [0])
        b1_eta = array('f', [0])
        b1_phi = array('f', [0])
        a2_pt = array('f', [0])
        a2_e  = array('f', [0])
        a2_eta = array('f', [0])
        a2_phi = array('f', [0])
        b2_pt = array('f', [0])
        b2_e  = array('f', [0])
        b2_eta = array('f', [0])
        b2_phi = array('f', [0])
        haa_m = array('f', [0])
        hbb_m = array('f', [0])
        hh_m  = array('f', [0])

        #def of skimmed tree with needed branches
        tree = ROOT.TTree( "events", "events" )
        ##open json file for the weights

        json_file = open('/eos/experiment/fcc/hh/utils/FCCDicts/FCChh_procDict_fcc_v07_II.json', 'r')
        # json_file = open('FCC_bbyy_Ntuples_for_analysis/FCChh_procDict_v05_scenarioI.json', 'r')
        all_weights = json.loads(json_file.read())
        xsec_weight = all_weights[name]['crossSection']
        k_factor_weight = all_weights[name]['kfactor']
        sumofweights = all_weights[name]['sumOfWeights']
        matching_eff = all_weights[name]['matchingEfficiency']

        weight_xs = xsec_weight*lumi*k_factor_weight*matching_eff/sumofweights

        tree.Branch( "weight",weight, "weight/F" )
               
        tree.Branch( "a1_pt",a1_pt, "a1_pt/F" )
        tree.Branch( "a1_eta",a1_eta, "a1_eta/F" )
        tree.Branch( "a1_phi",a1_phi, "a1_phi/F" )
        tree.Branch( "a1_e",a1_e, "a1_e/F" )
        tree.Branch( "a2_pt",a2_pt, "a2_pt/F" )
        tree.Branch( "a2_eta",a2_eta, "a2_eta/F" )
        tree.Branch( "a2_phi",a2_phi, "a2_phi/F" )
        tree.Branch( "a2_e",a2_e, "a2_e/F" )

        tree.Branch( "b1_pt",b1_pt, "b1_pt/F" )
        tree.Branch( "b1_eta",b1_eta, "b1_eta/F" )
        tree.Branch( "b1_phi",b1_phi, "b1_phi/F" )
        tree.Branch( "b1_e",b1_e, "b1_e/F" )
        tree.Branch( "b2_pt",b2_pt, "b2_pt/F" )
        tree.Branch( "b2_eta",b2_eta, "b2_eta/F" )
        tree.Branch( "b2_phi",b2_phi, "b2_phi/F" )
        tree.Branch( "b2_e",b2_e, "b2_e/F" )

        tree.Branch( "haa_m",haa_m, "haa_m/F" )
        tree.Branch( "hbb_m",hbb_m, "hbb_m/F" )
        tree.Branch( "hh_m",hh_m, "hh_m/F" )

        tree.Branch( "njets",njets, "njets/I" )
        tree.Branch( "pTb1_o_m_bb", pTb1_o_m_bb, "pTb1_o_m_bb/F" ) 
        tree.Branch( "pTb2_o_m_bb", pTb2_o_m_bb, "pTb2_o_m_bb/F" )
        tree.Branch( "pTbb_o_m_HH", pTbb_o_m_HH, "pTbb_o_m_HH/F" )
        tree.Branch( "pTg1_o_m_gg", pTg1_o_m_gg, "pTg1_o_m_gg/F" )
        tree.Branch( "pTg2_o_m_gg", pTg2_o_m_gg, "pTg2_o_m_gg/F" )
        tree.Branch( "pTgg_o_m_HH", pTgg_o_m_HH, "pTgg_o_m_HH/F" )
        tree.Branch( "nLep" , nLep, "nLep/I" )
        tree.Branch( "pT_l1", pT_l1, "pT_l1/F" )
        tree.Branch( "pT_l2", pT_l2, "pT_l2/F" )
        tree.Branch( "sum_pt", sum_pt, "sum_pt/F" )
        tree.Branch( "mindR_gb", mindR_gb, "mindR_gb/F"  )
        tree.Branch( "otherdR_gb", otherdR_gb, "otherdR_gb/F" )
        tree.Branch( "GG_cosT_restHH", GG_cosT_restHH, "GG_cosT_restHH" )
        tree.Branch( "B1_cosT_restBB", B1_cosT_restBB, "B1_cosT_restBB" ) 
        tree.Branch( "G1_cosT_restGG", G1_cosT_restGG, "G1_cosT_restGG" ) 
        tree.Branch( "DeltaPhi_gg", DeltaPhi_gg, "DeltaPhi_gg" )
        tree.Branch( "DeltaEta_gg", DeltaEta_gg, "DeltaEta_gg" ) 
        tree.Branch( "DeltaPhi_bb", DeltaPhi_bb, "DeltaPhi_bb" )
        tree.Branch( "DeltaEta_bb", DeltaEta_bb, "DeltaEta_bb" )
        tree.Branch( "DeltaPhi_HH", DeltaPhi_HH, "DeltaPhi_HH" )
        tree.Branch( "DeltaEta_HH", DeltaEta_HH, "DeltaEta_HH" )

        g1 = ROOT.TLorentzVector()
        g2 = ROOT.TLorentzVector()
        b1 = ROOT.TLorentzVector()
        b2 = ROOT.TLorentzVector()

        hgg = ROOT.TLorentzVector()
        hbb = ROOT.TLorentzVector()
        Hhh = ROOT.TLorentzVector()
        
        print("--------------------")
        print("Sample: ",name)
        fup = uproot.open(nameINPUT)
        print(fup.keys())
        if len(fup.keys()) == 0 :
           #if "events" not in fup.keys()[0]:
              print("No tree in file")
              continue
        #elif "events" not in fup.keys()[0]:
        #      print("No events in file")
        #      continue
        fup.close()
        try:
                print("Number of events : ",(fin.events).GetEntries())
        except:
                continue
        iter=0
                   
        for event in fin.events:
                #print(event)
                #iter_ +=1
                #if iter_ % 1000 == 0 :
                #   print("Iteration number ",iter_)

                ################
                #if iter_ > 10000:
                #   break
                ################

                #print(event.njets)
                #print('event.weight ', event.weight[0])
                #print('event.weight ', float(event.weight[0]))
                #print('weight_xs ', weight_xs)
                weight[0] = event.weight[0]*weight_xs
                
                a1_pt[0] = event.g1_pt 
                a1_e[0]  = event.g1_e
                a1_eta[0] = event.g1_eta
                a1_phi[0] = event.g1_phi
                b1_pt[0] = event.b1_pt
                b1_e[0]  = event.b1_e
                b1_eta[0] = event.b1_eta
                b1_phi[0] = event.b1_phi
                a2_pt[0] = event.g2_pt
                a2_e[0]  = event.g2_e
                a2_eta[0] = event.g2_eta
                a2_phi[0] = event.g2_phi
                b2_pt[0] = event.g2_pt
                b2_e[0]  = event.g2_e
                b2_eta[0] = event.g2_eta
                b2_phi[0] = event.g2_phi
               
                njets[0] = int(event.njets)
                nLep[0]  = int(event.nele + event.nmu)

                leptonsPT = [event.e1_pt, event.e2_pt, event.m1_pt, event.m2_pt]
                leptonsPT.sort(reverse=True)
                pT_l1[0] = leptonsPT[0]
                pT_l2[0] = leptonsPT[1]

                sum_pt[0] = event.b1_pt +event.b2_pt
                #try: 
                g1.SetPtEtaPhiE(event.g1_pt, event.g1_eta, event.g1_phi, event.g1_e)
                g2.SetPtEtaPhiE(event.g2_pt, event.g2_eta, event.g2_phi, event.g2_e)
                b1.SetPtEtaPhiE(event.b1_pt, event.b1_eta, event.b1_phi, event.b1_e)
                b2.SetPtEtaPhiE(event.b2_pt, event.b2_eta, event.b2_phi, event.b2_e)     
                #except Exception as e: # work on python 3.x
                #logger.error('Failed to implement TLorentzVector : '+ str(e))
                # print(event.a1_phi)
                # print(event.a2_phi)
                # print(event.b1_phi)
                # print(event.b2_phi)

                hgg = g1 + g2
                hbb = b1 + b2

                Hhh = hgg + hbb

                #print("-----")
                #print("Inv mass ", hbb.M())
                #print("da ntupla ", event.hbb_m)

                haa_m[0] = hgg.M()
                hbb_m[0] = hbb.M()
                hh_m[0]  = Hhh.M()
                pTb1_o_m_bb[0] = (b1.Pt())/(hbb.M())
                pTb2_o_m_bb[0] = (b2.Pt())/(hbb.M())
                pTbb_o_m_HH[0] = (hbb.Pt())/(Hhh.M())
                pTg1_o_m_gg[0] = (g1.Pt())/(hgg.M())
                pTg2_o_m_gg[0] = (g2.Pt())/(hgg.M())
                pTgg_o_m_HH[0] = (hgg.Pt())/(Hhh.M())


                DeltaPhi_gg[0] = g1.DeltaPhi(g2)
                DeltaEta_gg[0] = abs(g1.Eta()-g2.Eta())
                DeltaPhi_bb[0] = b1.DeltaPhi(b2)
                DeltaEta_bb[0] = abs(b1.Eta()-b2.Eta())
                DeltaPhi_HH[0] = hgg.DeltaPhi(hbb)
                DeltaEta_HH[0] = abs(hgg.Eta()-hbb.Eta())


                b_HH_ToCM = -Hhh.BoostVector()    
                boosted_GG = hgg
                boosted_GG.Boost(b_HH_ToCM)
                GG_cosT_restHH[0] = abs(math.cos(boosted_GG.Theta()))

                b_BB_ToCM = hbb.BoostVector()
                boosted_B = b1
                boosted_B.Boost(b_BB_ToCM)
                B1_cosT_restBB[0] = abs(math.cos(boosted_B.Theta()))

                b_GG_ToCM = hgg.BoostVector()
                boosted_G = g1
                boosted_G.Boost(b_GG_ToCM)
                G1_cosT_restGG[0] = abs(math.cos(boosted_G.Theta()))

                #print(G1_cosT_restGG)
                deltaRs = []
                deltaRs.append(g1.DeltaR(b1))
                deltaRs.append(g1.DeltaR(b2))
                deltaRs.append(g2.DeltaR(b1))
                deltaRs.append(g2.DeltaR(b2))

                if any([math.isnan(x) for x in deltaRs]):
                   print(deltaRs)
                   print("g1: ",g1.Pt())   
                   print("g2: ",g2.Pt())
                   print("b1: ",b1.Pt())
                   print("b2: ",b2.Pt()) 
                   print("----Discard Event----")    
                   continue

                mindR_gb[0] = min(deltaRs)
                #print(mindR_gb[0])
                index_min = deltaRs.index(min(deltaRs))
                otherdR_gb[0] = deltaRs[(3-index_min)]
                    
                tree.Fill()


        tree.Print()
        tree.Write()
        fout.Close()
