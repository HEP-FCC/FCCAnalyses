# Optional test file
testFile = "/eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/p8_ee_Zbb_ecm91_EvtGen_Bs2DsK/events_017659734.root"

import ROOT


# Mandatory: RDFanalysis class where the use defines the operations on the TTree
class RDFanalysis:

    # __________________________________________________________
    # Mandatory: analysers funtion to define the analysers to process, please make sure you return the last dataframe, in this example it is df2
    def analysers(df):
        df2 = (
            df.Alias("Particle1", "Particle#1.index")
            .Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
            .Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
            # matching between the RecoParticles and the MCParticles:
            .Define(
                "RP_MC_index",
                "ReconstructedParticle2MC::getRP2MC_index(MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles)",
            )
            # Generate a new set of tracks, re-scaling the covariance matrix
            # order of the scaling factors : smear_d0, smear_phi, smear_omega, smear_z0, smear_tlambda
            # the boolean flag is for debugging
            .Define(
                "SmearedTracks",
                ROOT.SmearObjects.SmearedTracks(2.0, 2.0, 2.0, 2.0, 2.0, True),
                ["ReconstructedParticles", "EFlowTrack_1", "RP_MC_index", "Particle"],
            )
            # What follows is only needed for validation.
            # Validation is made over the 1st track in each event
            .Define(
                "mcTrackParameters",
                "SmearObjects::mcTrackParameters( ReconstructedParticles, EFlowTrack_1, RP_MC_index, Particle)",
            )
            .Define("atrack_omega", "return EFlowTrack_1[0].omega ;")
            .Define("atrack_omega_cov", "return EFlowTrack_1[0].covMatrix[5] ;")
            .Define("smearTrack_omega", "return SmearedTracks[0].omega; ")
            .Define("mcTrack_omega", "return mcTrackParameters[0].omega; ")
            # events->Draw("(smearTrack_omega-mcTrack_omega)/TMath::Sqrt(atrack_omega_cov)" : should be gaussian with sigma = 2
            # events->Draw("(atrack_omega-mcTrack_omega)/TMath::Sqrt(atrack_omega_cov)") : should be gaussian with sigma = 1
        )
        return df2

    # __________________________________________________________
    # Mandatory: output function, please make sure you return the branchlist as a python list
    def output():
        branchList = ["atrack_omega", "atrack_omega_cov", "smearTrack_omega", "mcTrack_omega"]
        branchList += ["SmearedTracks", "EFlowTrack_1", "ReconstructedParticles"]

        return branchList
