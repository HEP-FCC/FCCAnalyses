from heppy.framework.analyzer import Analyzer
from heppy.utils.deltar import deltaR

class JetCorrector(Analyzer):

    def process(self, event):

        output_jets = []
        jet_collection  = getattr(event, self.cfg_ana.input_jets)
        corr_collection = getattr(event, self.cfg_ana.input_extra)
        drMax = self.cfg_ana.dr_match

        for jet in jet_collection:
            jetfix = jet
            jet_tmp = jet.p4()
            #print "#################\nini-> "+str(jetfix)
            for extra in corr_collection:
                dR = jet.p4().DeltaR(extra.p4())
                #print "extra-> "+str(extra)+" , dR="+str(dR)
                if dR < drMax :
                    jet_tmp += extra.p4()
                    #print "extra dR-> "+str(extra)

            jetfix.p4().SetPtEtaPhiM(jet_tmp.Pt(),jet_tmp.Eta(),jet_tmp.Phi(),jet_tmp.M())
            output_jets.append(jetfix)
            #print "end-> "+str(jetfix)

        setattr(event, self.cfg_ana.output, output_jets)
