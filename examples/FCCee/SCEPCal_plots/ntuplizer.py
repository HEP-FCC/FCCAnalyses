#!/usr/bin/env python3
import ROOT
import argparse

ROOT.EnableImplicitMT()
print ("Load cxx analyzers ... ")
ROOT.gSystem.Load("libFCCAnalyses")

ROOT.gErrorIgnoreLevel = ROOT.kFatal
_fcc  = ROOT.dummyLoader
ROOT.gInterpreter.Declare("using namespace FCCAnalyses;")


parser = argparse.ArgumentParser()
parser.add_argument("-inputFilesName",  help = "name of the input rootfiles", type = str)
parser.add_argument("-baseFolder",help = "input folder", type = str)
parser.add_argument("-outFolder",help = "output folder", type = str)
args = parser.parse_args()
NBITS = 27

print('Create RDataFrame ...')
df = ROOT.RDataFrame('events', args.baseFolder + "/" + args.inputFilesName)
print('Apply selectors and define new branches ...')
df = (df
              .Define('SimCaloHit_cellID', 'CaloNtupleizer::getSimCellID (SimCalorimeterHits)')
              .Define('SimCaloHit_depth',  'CaloNtupleizer::getSimCaloHit_depth(SimCalorimeterHits, %i )'%NBITS)
              .Define('SimCaloHit_energy', 'CaloNtupleizer::getSimCaloHit_energy (SimCalorimeterHits)')
              .Define('SimCaloHit_r', 'CaloNtupleizer::getSimCaloHit_r(SimCalorimeterHits)')
              .Define('SimCaloHit_x', 'CaloNtupleizer::getSimCaloHit_x (SimCalorimeterHits)')
              .Define('SimCaloHit_y', 'CaloNtupleizer::getSimCaloHit_y (SimCalorimeterHits)')
              .Define('SimCaloHit_z', 'CaloNtupleizer::getSimCaloHit_z (SimCalorimeterHits)')
              .Define('SimCaloHit_eta', 'CaloNtupleizer::getSimCaloHit_eta (SimCalorimeterHits)')
              .Define('SimCaloHit_phi', 'CaloNtupleizer::getSimCaloHit_phi (SimCalorimeterHits)')


              .Define('SimCaloHitC_cellID', 'CaloNtupleizer::getSimCellID (SimCalorimeterHitsCherenkov)')
              .Define('SimCaloHitC_depth',   'CaloNtupleizer::getSimCaloHit_depth(SimCalorimeterHits, %i)'%NBITS)
              .Define('SimCaloHitC_energy', 'CaloNtupleizer::getSimCaloHit_energy (SimCalorimeterHitsCherenkov)')
              .Define('SimCaloHitC_r', 'CaloNtupleizer::getSimCaloHit_r (SimCalorimeterHitsCherenkov)')
              .Define('SimCaloHitC_x', 'CaloNtupleizer::getSimCaloHit_x (SimCalorimeterHitsCherenkov)')
              .Define('SimCaloHitC_y', 'CaloNtupleizer::getSimCaloHit_y (SimCalorimeterHitsCherenkov)')
              .Define('SimCaloHitC_z', 'CaloNtupleizer::getSimCaloHit_z (SimCalorimeterHitsCherenkov)')
              .Define('SimCaloHitC_eta', 'CaloNtupleizer::getSimCaloHit_eta (SimCalorimeterHitsCherenkov)')
              .Define('SimCaloHitC_phi', 'CaloNtupleizer::getSimCaloHit_phi (SimCalorimeterHitsCherenkov)')

              .Define('MCparticle_energy', 'MCParticle::get_e (GenParticles)')
              .Define('MCparticle_px', 'MCParticle::get_px (GenParticles)')
              .Define('MCparticle_py', 'MCParticle::get_py (GenParticles)')
              .Define('MCparticle_pz', 'MCParticle::get_pz (GenParticles)')

      )
       
outfilename = args.outFolder+'/flatNtupla_'+ args.inputFilesName
print(f'Writing snapshot to disk ... \t{outfilename}')

df.Snapshot('events', outfilename,
             [
              'SimCaloHit_cellID', 
              'SimCaloHit_depth', 
              'SimCaloHit_energy', 
              'SimCaloHit_r', 
              'SimCaloHit_x', 
              'SimCaloHit_y', 
              'SimCaloHit_z', 
              'SimCaloHit_eta', 
              'SimCaloHit_phi', 

              'SimCaloHitC_cellID', 
              'SimCaloHitC_depth', 
              'SimCaloHitC_energy', 
              'SimCaloHitC_r', 
              'SimCaloHitC_x', 
              'SimCaloHitC_y', 
              'SimCaloHitC_z', 
              'SimCaloHitC_eta', 
              'SimCaloHitC_phi',
           
              'MCparticle_energy',
              'MCparticle_px',
              'MCparticle_py',
              'MCparticle_pz',
             ]
            )
