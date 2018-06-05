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
            #print "1-> "+str(jetfix)
            for extra in corr_collection:
                dR = jet.p4().DeltaR(extra.p4())
                if dR < drMax :
                    jet_tmp = jet.p4() + extra.p4()
                    jetfix.p4().SetPtEtaPhiM(jet_tmp.Pt(),jet_tmp.Eta(),jet_tmp.Phi(),jet_tmp.M())
                    #print "2-> "+str(jetfix)+" , "+str(extra)

            output_jets.append(jetfix)
        
        setattr(event, self.cfg_ana.output, output_jets)
