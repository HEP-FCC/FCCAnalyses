import ROOT as rt
# A little setup for drawing
#rt.gStyle.SetOptStat(0)
#cvs = rt.TCanvas()
#cvs.SetCanvasSize(800,600)

input_dir = "/eos/user/a/amagnan/FCC/iDMprod/Analysis/stage2/"
# Update the filenames with the new directory
fnameB = input_dir + "p8_ee_WW_ecm240.root"
fB = rt.TFile.Open(fnameB)
fB.ls()
treeB = fB.events

fnameB2 = input_dir + "p8_ee_ZZ_ecm240.root"
fB2 = rt.TFile.Open(fnameB2)
treeB2 = fB2.events

fnameB3 = input_dir + "wzp6_ee_ee_Mee_30_150_ecm240.root"
fB3 = rt.TFile.Open(fnameB3)
treeB3 = fB3.events

fnameB4 = input_dir + "wzp6_ee_mumu_ecm240.root"
fB4 = rt.TFile.Open(fnameB4)
treeB4 = fB4.events

fnameB5 = input_dir + "wzp6_ee_tautau_ecm240.root"
fB5 = rt.TFile.Open(fnameB5)
treeB5 = fB5.events

fnameB6 = input_dir + "wzp6_ee_nunuH_ecm240.root"
fB6 = rt.TFile.Open(fnameB6)
treeB6 = fB6.events


#fnameB = ("iDM/stage2/p8_ee_WW_ecm240.root")
#fB = rt.TFile.Open(fnameB)
#fB.ls()
#treeB = fB.events
#fnameB2 = ("iDM/stage2/p8_ee_ZZ_ecm240.root")
#fB2 = rt.TFile.Open(fnameB2)
#treeB2 = fB2.events
#fnameB3 = ("iDM/stage2/wzp6_ee_ee_Mee_30_150_ecm240.root")
#fB3 = rt.TFile.Open(fnameB3)
#treeB3 = fB3.events
#fnameB4 = ("iDM/stage2/wzp6_ee_mumu_ecm240.root")
#fB4 = rt.TFile.Open(fnameB4)
#treeB4 = fB4.events
#fnameB5 = ("iDM/stage2/wzp6_ee_tautau_ecm240.root")
#fB5 = rt.TFile.Open(fnameB5)
#treeB5 = fB5.events
#fnameB6 = ("iDM/stage2/wzp6_ee_nunuH_ecm240.root")
#fB6 = rt.TFile.Open(fnameB6)
#treeB6 = fB6.events

whhll = [0,0.0069/500000,0.005895/500000,0.004973/500000,0.007531/500000,0.006796/500000,0.002677/500000,0.001536/500000,0.001103/500000,0.0004448/500000,0.0008526/500000,4.716e-05/500000,0.0001749/500000,1.933e-07/500000,1.61e-07/500000,0,0,0,2.88e-05/500000,1.467e-07/500000,0.001014/500000]
whhllvv = [0,0.001303/500000,0.0009189/500000,0.005148/500000,2.634e-06/500000,1.769e-06/500000,1.615e-07/500000,3.531e-08/500000,2.433e-08/500000,1.218e-10/400002,5.058e-08/500000,2.346e-10/63,6.152e-11/200614,1.754e-11/500000,1.634e-11/500000,0,0,0,3.792e-09/500000,1.674e-11/500000,7.768e-09/400004]

for BP in range(11,21):
    print('BP ',BP)
    if (whhll[BP] == 0):
        print('skip')
    else:
        fnameS = input_dir + "e240_bp{}_h2h2ll.root".format(BP)
        fS = rt.TFile.Open(fnameS)
        fS.ls()
        treeS = fS.events
        
        fnameS2 = input_dir + "e240_bp{}_h2h2llvv.root".format(BP)
        fS2 = rt.TFile.Open(fnameS2)
        treeS2 = fS2.events

        #fnameS = "iDM/stage2/e240_bp{}_h2h2ll.root".format(BP)
        #fS = rt.TFile.Open(fnameS)
        #fS.ls()
        #treeS = fS.events
        #fnameS2 = "iDM/stage2/e240_bp{}_h2h2llvv.root".format(BP)
        #fS2 = rt.TFile.Open(fnameS2)
        #treeS2 = fS2.events
        
        
        # we can use this file later to analyse the results
        outputFile = rt.TFile.Open("TMVA_output_bp{}.root".format(BP), 'recreate')
        # we give it a name which it uses in the output, the outputfile, and
        # some options (for instance, remove ! in front of Silent to suppress
        # output)
        factory = rt.TMVA.Factory('TMVAClassification', outputFile,
                                  '!V:!Silent:Color:!DrawProgressBar:AnalysisType=Classification')
        # create a dataloader and tell it the tree it sould use for signal and background
        loader = rt.TMVA.DataLoader("dataset_{}".format(BP))
        # in our case, the same tree holds signal and background, we will tell
        # it later how to select the actual signal and background events we
        # could also optionally add weights if we had several trees for
        # e.g. different background processes
        loader.AddSignalTree(treeS,whhll[BP])
        loader.AddSignalTree(treeS2,whhllvv[BP])
        loader.AddBackgroundTree(treeB,16.4385/373375386)
        loader.AddBackgroundTree(treeB2,1.359/56162093)
        loader.AddBackgroundTree(treeB3,8.305/85400000)
        loader.AddBackgroundTree(treeB4,5.288/53400000)
        loader.AddBackgroundTree(treeB5,4.668/52400000)
        loader.AddBackgroundTree(treeB6,0.0462/3500000)
        # now we define the variables to be used in the analysis, do not give it a name...
        loader.AddVariable('Zcand_e')
        loader.AddVariable('Zcand_m')
        loader.AddVariable('Zcand_pt')
        loader.AddVariable('TMath::Abs(Zcand_pz)')
        loader.AddVariable('Zcand_costheta')
        loader.AddVariable('Zcand_povere')
        loader.AddVariable('Zcand_recoil_m')
        loader.AddVariable('cosThetaStar')
        loader.AddVariable('cosThetaR')
        loader.AddVariable('cosDphiLep')
        #loader.AddVariable('MET_pt[0]')#correlated with ZpT
        loader.AddVariable('lep1_pt')
        loader.AddVariable('lep2_pt')
        
        # finally tell it how to read signal and background and prepare the test/train
        
        preselCut="((n_electrons==0 && n_muons==2) ||(n_electrons==2 && n_muons==0)) &&  Zcand_m<120 && TMath::Abs(Zcand_pz)<70 && MET_pt[0]>5 && n_seljets<1 && n_photons==0 && lep1_pt<80 && lep2_pt<60 && Zcand_povere>0.1"
        
        loader.PrepareTrainingAndTestTree(preselCut, preselCut, # signal cut, then background cut
                                          "nTrain_Signal=100000:nTrain_Background=100000:SplitMode=Random:NormMode=NumEvents:!V")
        
        # Boosted Decision Trees
        factory.BookMethod(loader,rt.TMVA.Types.kBDT, "BDT",
                           "!V:NTrees=200:MinNodeSize=2.5%:MaxDepth=2:BoostType=AdaBoost:AdaBoostBeta=0.5:"+
                           "UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20")
        
        # Multi-Layer Perceptron (= Neural Network)
        #factory.BookMethod(loader, rt.TMVA.Types.kMLP, "MLP",
        #"!H:!V:NeuronType=tanh:VarTransform=N:NCycles=100:HiddenLayers=N+5:"+
        #"TestRate=5:!UseRegulator")
        # Train
        factory.TrainAllMethods()
        # Test
        factory.TestAllMethods()
        # Evaluate, these will compute various quantities of interest and output them into the output file
        factory.EvaluateAllMethods()
        # the output file will have the results of the training
        outputFile.Close()


#    def getReader():
#        reader = ROOT.TMVA.Reader()
#TMVAClassification_BDT.weights.xml
#reader.BookMVA("BDT","dataset/weights/TMVAClassification_BDT.weights.xml")
    
