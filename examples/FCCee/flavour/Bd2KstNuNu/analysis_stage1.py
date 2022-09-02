#Mandatory: List of processes
processList = {
    'p8_ee_Zbb_ecm91_EvtGen_Bd2KstNuNu':{}
}

#Mandatory: Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics
prodTag     = "FCCee/spring2021/IDEA/"

#Optional: output directory, default is local running directory
outputDir   = "outputs/FCCee/flavour/Bd2KstNuNu/stage1"

#Optional
nCPUS       = 8
runBatch    = False
#batchQueue = "longlunch"
#compGroup = "group_u_FCC.local_gen"

#Mandatory: RDFanalysis class where the use defines the operations on the TTree
class RDFanalysis():

    #__________________________________________________________
    #Mandatory: analysers funtion to define the analysers to process, please make sure you return the last dataframe, in this example it is df2
    def analysers(df):
        df2 = (df

               #############################################
               ##          Aliases for # in python        ##
               #############################################
               .Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
               .Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
               .Alias("Particle0", "Particle#0.index")
               .Alias("Particle1", "Particle#1.index")

               #############################################
               ##MC record to study the Z->bb events types##
               #############################################
               .Define("MC_PDG", "FCCAnalyses::MCParticle::get_pdg(Particle)")
               .Define("MC_n",   "int(MC_PDG.size())")
               .Define("MC_M1",  "myUtils::get_MCMother1(Particle,Particle0)")
               .Define("MC_M2",  "myUtils::get_MCMother2(Particle,Particle0)")
               .Define("MC_D1",  "myUtils::get_MCDaughter1(Particle,Particle1)")
               .Define("MC_D2",  "myUtils::get_MCDaughter2(Particle,Particle1)")
               .Define("MC_x",   "FCCAnalyses::MCParticle::get_vertex_x(Particle)")
               .Define("MC_y",   "FCCAnalyses::MCParticle::get_vertex_y(Particle)")
               .Define("MC_z",   "FCCAnalyses::MCParticle::get_vertex_z(Particle)")
               .Define("MC_e",   "FCCAnalyses::MCParticle::get_e(Particle)")
               .Define("MC_m",   "FCCAnalyses::MCParticle::get_mass(Particle)")

               #############################################
               ##               Build MC Vertex           ##
               #############################################
               .Define("MCVertexObject", "myUtils::get_MCVertexObject(Particle, Particle0)")
               .Define("MC_Vertex_x",    "myUtils::get_MCVertex_x(MCVertexObject)")
               .Define("MC_Vertex_y",    "myUtils::get_MCVertex_y(MCVertexObject)")
               .Define("MC_Vertex_z",    "myUtils::get_MCVertex_z(MCVertexObject)")
               .Define("MC_Vertex_ind",  "myUtils::get_MCindMCVertex(MCVertexObject)")
               .Define("MC_Vertex_ntrk", "myUtils::get_NTracksMCVertex(MCVertexObject)")
               .Define("MC_Vertex_n",    "int(MC_Vertex_x.size())")
               .Define("MC_Vertex_PDG",  "myUtils::get_MCpdgMCVertex(MCVertexObject, Particle)")
               .Define("MC_Vertex_PDGmother",  "myUtils::get_MCpdgMotherMCVertex(MCVertexObject, Particle)")
               .Define("MC_Vertex_PDGgmother", "myUtils::get_MCpdgGMotherMCVertex(MCVertexObject, Particle)")

               #############################################
               ##              Build Reco Vertex          ##
               #############################################
               .Define("VertexObject", "myUtils::get_VertexObject(MCVertexObject,ReconstructedParticles,EFlowTrack_1,MCRecoAssociations0,MCRecoAssociations1)")

               #############################################
               ##          Build PV var and filter        ##
               #############################################
               .Define("EVT_hasPV",    "myUtils::hasPV(VertexObject)")
               .Define("EVT_NtracksPV", "float(myUtils::get_PV_ntracks(VertexObject))")
               .Define("EVT_NVertex",   "float(VertexObject.size())")
               .Filter("EVT_hasPV==1")


               #############################################
               ##          Build RECO P with PID          ##
               #############################################
               .Define("RecoPartPID" ,"myUtils::PID(ReconstructedParticles, MCRecoAssociations0,MCRecoAssociations1,Particle)")

               #############################################
               ##    Build RECO P with PID at vertex      ##
               #############################################
               .Define("RecoPartPIDAtVertex" ,"myUtils::get_RP_atVertex(RecoPartPID, VertexObject)")

               #############################################
               ##         Build vertex variables          ##
               #############################################
               .Define("Vertex_x",        "myUtils::get_Vertex_x(VertexObject)")
               .Define("Vertex_y",        "myUtils::get_Vertex_y(VertexObject)")
               .Define("Vertex_z",        "myUtils::get_Vertex_z(VertexObject)")
               .Define("Vertex_xErr",     "myUtils::get_Vertex_xErr(VertexObject)")
               .Define("Vertex_yErr",     "myUtils::get_Vertex_yErr(VertexObject)")
               .Define("Vertex_zErr",     "myUtils::get_Vertex_zErr(VertexObject)")

               .Define("Vertex_chi2",     "myUtils::get_Vertex_chi2(VertexObject)")
               .Define("Vertex_mcind",    "myUtils::get_Vertex_indMC(VertexObject)")
               .Define("Vertex_ind",      "myUtils::get_Vertex_ind(VertexObject)")
               .Define("Vertex_isPV",     "myUtils::get_Vertex_isPV(VertexObject)")
               .Define("Vertex_ntrk",     "myUtils::get_Vertex_ntracks(VertexObject)")
               .Define("Vertex_n",        "int(Vertex_x.size())")
               .Define("Vertex_mass",     "myUtils::get_Vertex_mass(VertexObject,RecoPartPIDAtVertex)")

               .Define("Vertex_d2PV",     "myUtils::get_Vertex_d2PV(VertexObject,-1)")
               .Define("Vertex_d2PVx",    "myUtils::get_Vertex_d2PV(VertexObject,0)")
               .Define("Vertex_d2PVy",    "myUtils::get_Vertex_d2PV(VertexObject,1)")
               .Define("Vertex_d2PVz",    "myUtils::get_Vertex_d2PV(VertexObject,2)")

               .Define("Vertex_d2PVErr",  "myUtils::get_Vertex_d2PVError(VertexObject,-1)")
               .Define("Vertex_d2PVxErr", "myUtils::get_Vertex_d2PVError(VertexObject,0)")
               .Define("Vertex_d2PVyErr", "myUtils::get_Vertex_d2PVError(VertexObject,1)")
               .Define("Vertex_d2PVzErr", "myUtils::get_Vertex_d2PVError(VertexObject,2)")

               .Define("Vertex_d2PVSig",  "Vertex_d2PV/Vertex_d2PVErr")
               .Define("Vertex_d2PVxSig", "Vertex_d2PVx/Vertex_d2PVxErr")
               .Define("Vertex_d2PVySig", "Vertex_d2PVy/Vertex_d2PVyErr")
               .Define("Vertex_d2PVzSig", "Vertex_d2PVz/Vertex_d2PVzErr")

               .Define("Vertex_d2MC",     "myUtils::get_Vertex_d2MC(VertexObject,MCVertexObject,Vertex_mcind,-1)")
               .Define("Vertex_d2MCx",    "myUtils::get_Vertex_d2MC(VertexObject,MCVertexObject,Vertex_mcind,0)")
               .Define("Vertex_d2MCy",    "myUtils::get_Vertex_d2MC(VertexObject,MCVertexObject,Vertex_mcind,1)")
               .Define("Vertex_d2MCz",    "myUtils::get_Vertex_d2MC(VertexObject,MCVertexObject,Vertex_mcind,2)")

               .Define("EVT_dPV2DVmin",   "myUtils::get_dPV2DV_min(Vertex_d2PV)")
               .Define("EVT_dPV2DVmax",   "myUtils::get_dPV2DV_max(Vertex_d2PV)")
               .Define("EVT_dPV2DVave",   "myUtils::get_dPV2DV_ave(Vertex_d2PV)")

               #############################################
               ##        Build Kstz -> KPi  candidates      ##
               #############################################
               .Define("KPiCandidates",         "myUtils::build_Bd2KstNuNu(VertexObject,RecoPartPIDAtVertex)")

               #############################################
               ##       Filter Kstz -> KPi candidates      ##
               #############################################
               .Define("EVT_NKPi",              "float(myUtils::getFCCAnalysesComposite_N(KPiCandidates))")
               .Filter("EVT_NKPi>0")


               #############################################
               ##              Build the thrust           ##
               #############################################
               .Define("RP_e",          "ReconstructedParticle::get_e(RecoPartPIDAtVertex)")
               .Define("RP_px",         "ReconstructedParticle::get_px(RecoPartPIDAtVertex)")
               .Define("RP_py",         "ReconstructedParticle::get_py(RecoPartPIDAtVertex)")
               .Define("RP_pz",         "ReconstructedParticle::get_pz(RecoPartPIDAtVertex)")
               .Define("RP_charge",     "ReconstructedParticle::get_charge(RecoPartPIDAtVertex)")

               .Define("EVT_thrustNP",      'Algorithms::minimize_thrust("Minuit2","Migrad")(RP_px, RP_py, RP_pz)')
               .Define("RP_thrustangleNP",  'Algorithms::getAxisCosTheta(EVT_thrustNP, RP_px, RP_py, RP_pz)')
               .Define("EVT_thrust",        'Algorithms::getThrustPointing(RP_thrustangleNP, RP_e, EVT_thrustNP, 1.)')
               .Define("RP_thrustangle",    'Algorithms::getAxisCosTheta(EVT_thrust, RP_px, RP_py, RP_pz)')


               #############################################
               ##        Get thrust related values        ##
               #############################################
               ##hemis0 == negative angle == max energy hemisphere if pointing
               ##hemis1 == positive angle == min energy hemisphere if pointing
               .Define("EVT_thrusthemis0_n",    "Algorithms::getAxisN(0)(RP_thrustangle, RP_charge)")
               .Define("EVT_thrusthemis1_n",    "Algorithms::getAxisN(1)(RP_thrustangle, RP_charge)")
               .Define("EVT_thrusthemis0_e",    "Algorithms::getAxisEnergy(0)(RP_thrustangle, RP_charge, RP_e)")
               .Define("EVT_thrusthemis1_e",    "Algorithms::getAxisEnergy(1)(RP_thrustangle, RP_charge, RP_e)")

               .Define("EVT_ThrustEmax_E",         "EVT_thrusthemis0_e.at(0)")
               .Define("EVT_ThrustEmax_Echarged",  "EVT_thrusthemis0_e.at(1)")
               .Define("EVT_ThrustEmax_Eneutral",  "EVT_thrusthemis0_e.at(2)")
               .Define("EVT_ThrustEmax_N",         "float(EVT_thrusthemis0_n.at(0))")
               .Define("EVT_ThrustEmax_Ncharged",  "float(EVT_thrusthemis0_n.at(1))")
               .Define("EVT_ThrustEmax_Nneutral",  "float(EVT_thrusthemis0_n.at(2))")

               .Define("EVT_ThrustEmin_E",         "EVT_thrusthemis1_e.at(0)")
               .Define("EVT_ThrustEmin_Echarged",  "EVT_thrusthemis1_e.at(1)")
               .Define("EVT_ThrustEmin_Eneutral",  "EVT_thrusthemis1_e.at(2)")
               .Define("EVT_ThrustEmin_N",         "float(EVT_thrusthemis1_n.at(0))")
               .Define("EVT_ThrustEmin_Ncharged",  "float(EVT_thrusthemis1_n.at(1))")
               .Define("EVT_ThrustEmin_Nneutral",  "float(EVT_thrusthemis1_n.at(2))")


               .Define("Vertex_thrust_angle",   "myUtils::get_Vertex_thrusthemis_angle(VertexObject, RecoPartPIDAtVertex, EVT_thrust)")
               .Define("DVertex_thrust_angle",  "myUtils::get_DVertex_thrusthemis_angle(VertexObject, RecoPartPIDAtVertex, EVT_thrust)")
               ###0 == negative angle==max energy , 1 == positive angle == min energy
               .Define("Vertex_thrusthemis_emin",    "myUtils::get_Vertex_thrusthemis(Vertex_thrust_angle, 1)")
               .Define("Vertex_thrusthemis_emax",    "myUtils::get_Vertex_thrusthemis(Vertex_thrust_angle, 0)")

               .Define("EVT_ThrustEmin_NDV", "float(myUtils::get_Npos(DVertex_thrust_angle))")
               .Define("EVT_ThrustEmax_NDV", "float(myUtils::get_Nneg(DVertex_thrust_angle))")

               .Define("EVT_Thrust_Mag",  "EVT_thrust.at(0)")
               .Define("EVT_Thrust_X",    "EVT_thrust.at(1)")
               .Define("EVT_Thrust_XErr", "EVT_thrust.at(2)")
               .Define("EVT_Thrust_Y",    "EVT_thrust.at(3)")
               .Define("EVT_Thrust_YErr", "EVT_thrust.at(4)")
               .Define("EVT_Thrust_Z",    "EVT_thrust.at(5)")
               .Define("EVT_Thrust_ZErr", "EVT_thrust.at(6)")


               .Define("DV_tracks", "myUtils::get_pseudotrack(VertexObject,RecoPartPIDAtVertex)")

               .Define("DV_d0",            "myUtils::get_trackd0(DV_tracks)")
               .Define("DV_z0",            "myUtils::get_trackz0(DV_tracks)")

               .Define("KPiCandidates_mass",    "myUtils::getFCCAnalysesComposite_mass(KPiCandidates)")
               .Define("KPiCandidates_q",       "myUtils::getFCCAnalysesComposite_charge(KPiCandidates)")
               .Define("KPiCandidates_vertex",  "myUtils::getFCCAnalysesComposite_vertex(KPiCandidates)")
               .Define("KPiCandidates_mcvertex","myUtils::getFCCAnalysesComposite_mcvertex(KPiCandidates,VertexObject)")
               .Define("KPiCandidates_px",      "myUtils::getFCCAnalysesComposite_p(KPiCandidates,0)")
               .Define("KPiCandidates_py",      "myUtils::getFCCAnalysesComposite_p(KPiCandidates,1)")
               .Define("KPiCandidates_pz",      "myUtils::getFCCAnalysesComposite_p(KPiCandidates,2)")
               .Define("KPiCandidates_p",       "myUtils::getFCCAnalysesComposite_p(KPiCandidates,-1)")
               .Define("KPiCandidates_B",       "myUtils::getFCCAnalysesComposite_B(KPiCandidates, VertexObject, RecoPartPIDAtVertex)")

               .Define("KPiCandidates_track",   "myUtils::getFCCAnalysesComposite_track(KPiCandidates, VertexObject)")
               .Define("KPiCandidates_d0",      "myUtils::get_trackd0(KPiCandidates_track)")
               .Define("KPiCandidates_z0",      "myUtils::get_trackz0(KPiCandidates_track)")

               .Define("KPiCandidates_anglethrust", "myUtils::getFCCAnalysesComposite_anglethrust(KPiCandidates, EVT_thrust)")
               .Define("CUT_hasCandEmin",           "myUtils::has_anglethrust_emin(KPiCandidates_anglethrust)")
               .Filter("CUT_hasCandEmin>0")

               .Define("KPiCandidates_h1px",   "myUtils::getFCCAnalysesComposite_p(KPiCandidates, VertexObject, RecoPartPIDAtVertex, 0, 0)")
               .Define("KPiCandidates_h1py",   "myUtils::getFCCAnalysesComposite_p(KPiCandidates, VertexObject, RecoPartPIDAtVertex, 0, 1)")
               .Define("KPiCandidates_h1pz",   "myUtils::getFCCAnalysesComposite_p(KPiCandidates, VertexObject, RecoPartPIDAtVertex, 0, 2)")
               .Define("KPiCandidates_h1p",    "myUtils::getFCCAnalysesComposite_p(KPiCandidates, VertexObject, RecoPartPIDAtVertex, 0, -1)")
               .Define("KPiCandidates_h1q",    "myUtils::getFCCAnalysesComposite_q(KPiCandidates, VertexObject, RecoPartPIDAtVertex, 0)")
               .Define("KPiCandidates_h1m",    "myUtils::getFCCAnalysesComposite_mass(KPiCandidates, VertexObject, RecoPartPIDAtVertex, 0)")
               .Define("KPiCandidates_h1type", "myUtils::getFCCAnalysesComposite_type(KPiCandidates, VertexObject, RecoPartPIDAtVertex, 0)")
               .Define("KPiCandidates_h1d0",   "myUtils::getFCCAnalysesComposite_d0(KPiCandidates, VertexObject, 0)")
               .Define("KPiCandidates_h1z0",   "myUtils::getFCCAnalysesComposite_z0(KPiCandidates, VertexObject, 0)")

               .Define("KPiCandidates_h2px",   "myUtils::getFCCAnalysesComposite_p(KPiCandidates, VertexObject, RecoPartPIDAtVertex, 1, 0)")
               .Define("KPiCandidates_h2py",   "myUtils::getFCCAnalysesComposite_p(KPiCandidates, VertexObject, RecoPartPIDAtVertex, 1, 1)")
               .Define("KPiCandidates_h2pz",   "myUtils::getFCCAnalysesComposite_p(KPiCandidates, VertexObject, RecoPartPIDAtVertex, 1, 2)")
               .Define("KPiCandidates_h2p",    "myUtils::getFCCAnalysesComposite_p(KPiCandidates, VertexObject, RecoPartPIDAtVertex, 1, -1)")
               .Define("KPiCandidates_h2q",    "myUtils::getFCCAnalysesComposite_q(KPiCandidates, VertexObject, RecoPartPIDAtVertex, 1)")
               .Define("KPiCandidates_h2m",    "myUtils::getFCCAnalysesComposite_mass(KPiCandidates, VertexObject, RecoPartPIDAtVertex, 1)")
               .Define("KPiCandidates_h2type", "myUtils::getFCCAnalysesComposite_type(KPiCandidates, VertexObject, RecoPartPIDAtVertex, 1)")
               .Define("KPiCandidates_h2d0",   "myUtils::getFCCAnalysesComposite_d0(KPiCandidates, VertexObject, 1)")
               .Define("KPiCandidates_h2z0",   "myUtils::getFCCAnalysesComposite_z0(KPiCandidates, VertexObject, 1)")

               .Define("TrueKPiBd_vertex",        "myUtils::get_trueVertex(MCVertexObject,Particle,Particle0, 313, 511)")
               .Define("TrueKPiBd_track",         "myUtils::get_truetrack(TrueKPiBd_vertex, MCVertexObject, Particle)")
               .Define("TrueKPiBd_d0",            "myUtils::get_trackd0(TrueKPiBd_track)")
               .Define("TrueKPiBd_z0",            "myUtils::get_trackz0(TrueKPiBd_track)")

        )
        return df2

    #__________________________________________________________
    #Mandatory: output function, please make sure you return the branchlist as a python list
    def output():
        branchList = [

                "MC_PDG","MC_M1","MC_M2","MC_n","MC_D1","MC_D2",#"MC_D3",
                "MC_x","MC_y","MC_z","MC_e","MC_m",
                "EVT_ThrustEmin_E",          "EVT_ThrustEmax_E",
                "EVT_ThrustEmin_Echarged",   "EVT_ThrustEmax_Echarged",
                "EVT_ThrustEmin_Eneutral",   "EVT_ThrustEmax_Eneutral",
                "EVT_ThrustEmin_N",          "EVT_ThrustEmax_N",
                "EVT_ThrustEmin_Ncharged",   "EVT_ThrustEmax_Ncharged",
                "EVT_ThrustEmin_Nneutral",   "EVT_ThrustEmax_Nneutral",
                "EVT_ThrustEmin_NDV",        "EVT_ThrustEmax_NDV",
                "EVT_Thrust_Mag",
                "EVT_Thrust_X",  "EVT_Thrust_XErr",
                "EVT_Thrust_Y",  "EVT_Thrust_YErr",
                "EVT_Thrust_Z",  "EVT_Thrust_ZErr",

                "EVT_NtracksPV", "EVT_NVertex", "EVT_NKPi",

                "EVT_dPV2DVmin","EVT_dPV2DVmax","EVT_dPV2DVave",

                "MC_Vertex_x", "MC_Vertex_y", "MC_Vertex_z",
                "MC_Vertex_ntrk", "MC_Vertex_n",

                "MC_Vertex_PDG","MC_Vertex_PDGmother","MC_Vertex_PDGgmother",

                "Vertex_x", "Vertex_y", "Vertex_z",
                "Vertex_xErr", "Vertex_yErr", "Vertex_zErr",
                "Vertex_isPV", "Vertex_ntrk", "Vertex_chi2", "Vertex_n",
                "Vertex_thrust_angle", "Vertex_thrusthemis_emin", "Vertex_thrusthemis_emax",

                "Vertex_d2PV", "Vertex_d2PVx", "Vertex_d2PVy", "Vertex_d2PVz",
                "Vertex_d2PVErr", "Vertex_d2PVxErr", "Vertex_d2PVyErr", "Vertex_d2PVzErr",
                "Vertex_mass",
                "DV_d0","DV_z0",

                "TrueKPiBd_vertex", "TrueKPiBd_d0", "TrueKPiBd_z0",

                "KPiCandidates_mass", "KPiCandidates_vertex", "KPiCandidates_mcvertex", "KPiCandidates_B",
                "KPiCandidates_px", "KPiCandidates_py", "KPiCandidates_pz", "KPiCandidates_p", "KPiCandidates_q",
                "KPiCandidates_d0",  "KPiCandidates_z0","KPiCandidates_anglethrust",

                "KPiCandidates_h1px", "KPiCandidates_h1py", "KPiCandidates_h1pz",
                "KPiCandidates_h1p", "KPiCandidates_h1q", "KPiCandidates_h1m", "KPiCandidates_h1type",
                "KPiCandidates_h1d0", "KPiCandidates_h1z0",
                "KPiCandidates_h2px", "KPiCandidates_h2py", "KPiCandidates_h2pz",
                "KPiCandidates_h2p", "KPiCandidates_h2q", "KPiCandidates_h2m", "KPiCandidates_h2type",
                "KPiCandidates_h2d0", "KPiCandidates_h2z0",

                ]
        return branchList
