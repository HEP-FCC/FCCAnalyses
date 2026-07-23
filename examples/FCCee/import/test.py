import FCCAnalyses
import ROOT

ROOT.gROOT.SetBatch(True)

def main():
    '''
    Example analysis entry point
    '''

    fccana = FCCAnalyses.Analysis('Test Analysis', 7)

    fccana.add_analyzers('examples/FCCee/import/AddAnalyzers.h')

    # fccana.add_files('examples/FCCee/import/test.root')

    dframe = fccana.get_dataframe()
    dframe2 = dframe.Define("particles", "gen_particles()")
    dframe3 = dframe2.Define("particles_pt", "MCParticle::get_pt(particles)")
    hist = dframe3.Histo1D("particles_pt")
    hist.Print()

    canvas = ROOT.TCanvas("canvas", "", 450, 450)
    hist.Draw()
    canvas.Print('test.pdf')

if __name__ == '__main__':
    main()
