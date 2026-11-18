"""Read reconstructed particles, muon subset indices and jets without cuts."""


class Analysis:
    def __init__(self, _):
        pass

    def analyzers(self, df):
        return (
            df.Alias('MuonIndex', 'Muon_objIdx.index')
            .Define('muons',
                    'FCCAnalyses::ReconstructedParticle::get('
                    'MuonIndex, ReconstructedParticles)')
            .Define('n_reconstructed',
                    'FCCAnalyses::ReconstructedParticle::get_n(ReconstructedParticles)')
            .Define('n_muons', 'FCCAnalyses::ReconstructedParticle::get_n(muons)')
            .Define('muon_momentum', 'FCCAnalyses::ReconstructedParticle::get_p(muons)')
            .Define('n_jets', 'FCCAnalyses::ReconstructedParticle::get_n(Jet)')
            .Define('jet_momentum', 'FCCAnalyses::ReconstructedParticle::get_p(Jet)')
        )

    def output(self):
        return ['n_reconstructed', 'n_muons', 'muon_momentum',
                'n_jets', 'jet_momentum']
