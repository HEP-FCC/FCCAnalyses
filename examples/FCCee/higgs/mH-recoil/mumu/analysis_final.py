'''
Final stage of the example Z(mumu)H recoil mass analysis.
'''

# Input directory where the files produced in the pre-selection stages are
# stored
inputDir = "outputs/FCCee/higgs/mH-recoil/mumu/stage2/"

# Output directory where the resulting files will be stored
outputDir = "outputs/FCCee/higgs/mH-recoil/mumu/final/"

processList = {
    # Run over the full statistics from stage2 input file
    # <inputDir>/p8_ee_ZZ_ecm240.root. Keep the same output name as input
    'p8_ee_ZZ_ecm240': {},
    # Run over the statistics from stage2 input files
    # <inputDir>/p8_ee_WW_ecm240_out/*.root. Keep the same output name as input
    'p8_ee_WW_ecm240': {},
    # Run over the full statistics from stage2 input file
    # <inputDir>/p8_ee_ZH_ecm240_out.root. Change the output name to
    # MySample_p8_ee_ZH_ecm240
    'MySample_p8_ee_ZH_ecm240': {}
}

# Link to the dictionary that contains all the cross section information etc...
procDict = "FCCee_procDict_spring2021_IDEA.json"

# Add MySample_p8_ee_ZH_ecm240 as it is not an offical process
procDictAdd = {"MySample_p8_ee_ZH_ecm240": {"numberOfEvents": 10000000,
                                            "sumOfWeights": 10000000,
                                            "crossSection": 0.201868,
                                            "kfactor": 1.0,
                                            "matchingEfficiency": 1.0}}

# Expected integrated luminosity
intLumi = 5.0e+06  # pb-1

# Whether to scale to expected integrated luminosity
doScale = True

# Number of threads to use
nCPUS = 2

# Whether to produce ROOT TTrees, default is False
doTree = True

# Save cut yields and efficiencies in LaTeX table
saveTabular = True

# Save cut yields and efficiencies in JSON file
saveJSON = True

# Dictionary with the list of cuts. The key is the name of the selection that
# will be added to the output file
cutList = {"sel0": "Zcand_q == 0",
           "sel1": "Zcand_q == -1 || Zcand_q == 1",
           "sel2": "Zcand_m > 80 && Zcand_m < 100",
           "sel3": "MyFilter==true && (Zcand_m < 80 || Zcand_m > 100)"}


# Dictionary for the output variables/histograms. The key is the name of the
# variable in the output files. "name" is the name of the variable in the input
# file, "title" is the x-axis label of the histogram, "bin" the number of bins
# of the histogram, "xmin" the minimum x-axis value and "xmax" the maximum
# x-axis value.
histoList = {
    "mz": {"name": "Zcand_m",
           "title": "m_{Z} [GeV]",
           "bin": 125, "xmin": 0, "xmax": 250},
    "mz_zoom": {"name": "Zcand_m",
                "title": "m_{Z} [GeV]",
                "bin": 40, "xmin": 80, "xmax": 100},
    "leptonic_recoil_m": {"name": "Zcand_recoil_m",
                          "title": "Z leptonic recoil [GeV]",
                          "bin": 100, "xmin": 0, "xmax": 200},
    "leptonic_recoil_m_zoom": {"name": "Zcand_recoil_m",
                               "title": "Z leptonic recoil [GeV]",
                               "bin": 200, "xmin": 80, "xmax": 160},
    "leptonic_recoil_m_zoom1": {"name": "Zcand_recoil_m",
                                "title": "Z leptonic recoil [GeV]",
                                "bin": 100, "xmin": 120, "xmax": 140},
    "leptonic_recoil_m_zoom2": {"name": "Zcand_recoil_m",
                                "title": "Z leptonic recoil [GeV]",
                                "bin": 200, "xmin": 120, "xmax": 140},
    "leptonic_recoil_m_zoom3": {"name": "Zcand_recoil_m",
                                "title": "Z leptonic recoil [GeV]",
                                "bin": 400, "xmin": 120, "xmax": 140},
    "leptonic_recoil_m_zoom4": {"name": "Zcand_recoil_m",
                                "title": "Z leptonic recoil [GeV]",
                                "bin": 800, "xmin": 120, "xmax": 140},
    "leptonic_recoil_m_zoom5": {"name": "Zcand_recoil_m",
                                "title": "Z leptonic recoil [GeV]",
                                "bin": 2000, "xmin": 120, "xmax": 140},
    "leptonic_recoil_m_zoom6": {"name": "Zcand_recoil_m",
                                "title": "Z leptonic recoil [GeV]",
                                "bin": 100, "xmin": 130.3, "xmax": 132.5},
    # 1D histogram (alternative syntax)
    "mz_1D": {"cols": ["Zcand_m"],
              "title": "m_{Z} [GeV]",
              "bins": [(40, 80, 100)]},
    # 2D histogram
    "mz_recoil_2D": {"cols": ["Zcand_m", "Zcand_recoil_m"],
                     "title": "m_{Z} - leptonic recoil [GeV]",
                     "bins": [(40, 80, 100), (100, 120, 140)]},
    # 3D histogram
    "mz_recoil_3D": {
        "cols": ["Zcand_m", "Zcand_recoil_m", "Zcand_recoil_m"],
        "title": "m_{Z} - leptonic recoil - leptonic recoil [GeV]",
        "bins": [(40, 80, 100), (100, 120, 140), (100, 120, 140)]},
}
