#ifndef  VERTEXFITTERSIMPLE_ANALYZERS_H
#define  VERTEXFITTERSIMPLE_ANALYZERS_H

#include <cmath>
#include <vector>

#include "ROOT/RVec.hxx"
#include "edm4hep/ReconstructedParticleData.h"
#include "edm4hep/TrackState.h"

#include "TVectorD.h"
#include "TVector3.h"
#include "TMatrixDSym.h"
#include "TMath.h"
#include "TDecompChol.h"
#include "TMatrixD.h"

#include "ReconstructedParticle2Track.h"
#include "ReconstructedParticle2MC.h"
#include "VertexingUtils.h"

#include "edm4hep/VertexData.h"
#include "edm4hep/Vertex.h"

#include "TrackCovariance/VertexFit.h" // from Delphes - updates Franco, Jul 2022
#include "TrackCovariance/VertexMore.h"

/** Vertex interface using Franco Bedeshi's code.
This represents a set functions and utilities to perfom vertexing from a list of tracks.
*/
namespace FCCAnalyses{

namespace VertexFitterSimple{

/// Vertex (code from Franco Bedeschi): passing the recoparticles. Units for the
/// beamspot constraint: mum. See VertexFitter_Tk() below for what
/// ComputeMomentaAtVertex controls.
VertexingUtils::FCCAnalysesVertex VertexFitter(
    int Primary,
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> recoparticles,
    ROOT::VecOps::RVec<edm4hep::TrackState> alltracks,
    bool BeamSpotConstraint = false, double sigmax = 0., double sigmay = 0.,
    double sigmaz = 0., double bsc_x = 0., double bsc_y = 0., double bsc_z = 0.,
    bool ComputeMomentaAtVertex = true);

/// Vertex (code from Franco Bedeschi): passing the tracks. Units for the
/// beamspot constraint: mum. ComputeMomentaAtVertex controls whether
/// updated_track_momentum_at_vertex is filled: it requires building a Delphes
/// VertexMore object, whose cost scales as O(ntracks^3) and dominates the total
/// runtime for events with many tracks. Set to false when only the vertex
/// position/chi2 is needed (e.g. FCCAnalysesVertex::vertex via
/// VertexingUtils::get_VertexData) -- see
/// https://github.com/HEP-FCC/FCCAnalyses/issues/378.
/// startR: optional transverse radius [mm] at which the fit starts, i.e.
/// linearises the helices (Delphes VertexFit::SetStartR), measured from the
/// origin of the frame of the vertex position; <= 0 or NaN (default -1): keep
/// the previous start, at the points of closest approach to that origin. The
/// default start can converge to a wrong solution for vertices far from the
/// origin (the other crossing point of two transverse track circles). A
/// radius beyond the farthest transverse point of a track is reduced to it;
/// if the start is undefined for a track, the default start is used instead.
/// startR is the last argument, so all the preceding ones must be given, e.g.
/// VertexFitter_Tk(2, tracks, false, 0., 0., 0., 0., 0., 0., true, 350.);
/// a shorter call such as VertexFitter_Tk(2, tracks, 350.) compiles but sets
/// BeamSpotConstraint instead. For a track pair, VertexFitter_2Tk_seeded()
/// chooses the start radius itself.
VertexingUtils::FCCAnalysesVertex
VertexFitter_Tk(int Primary, ROOT::VecOps::RVec<edm4hep::TrackState> tracks,
                bool BeamSpotConstraint = false, double sigmax = 0.,
                double sigmay = 0., double sigmaz = 0., double bsc_x = 0.,
                double bsc_y = 0., double bsc_z = 0.,
                bool ComputeMomentaAtVertex = true, double startR = -1.);

VertexingUtils::FCCAnalysesVertex
VertexFitter_Tk(int Primary, ROOT::VecOps::RVec<edm4hep::TrackState> tracks,
                const ROOT::VecOps::RVec<edm4hep::TrackState> &alltracks,
                bool BeamSpotConstraint = false, double sigmax = 0.,
                double sigmay = 0., double sigmaz = 0., double bsc_x = 0.,
                double bsc_y = 0., double bsc_z = 0.,
                bool ComputeMomentaAtVertex = true, double startR = -1.);

/// Vertex fit of a track pair started at the crossing points of the two
/// transverse track circles (VertexingUtils::get_circleCrossingRadii): one fit
/// from each of the two crossing radii, or, if the circles do not cross, one
/// fit from the radius of their closest approach and one with the default
/// start; the fit with the lowest chi2 is returned (NaN counts as the highest).
/// Same output as VertexFitter_Tk (no beam-spot constraint), at about twice its
/// CPU cost (two fits). Not 2 tracks, or no crossing radius defined:
/// VertexFitter_Tk with the default start. Used by the V0 finders of
/// VertexFinderLCFIPlus (get_V0s, get_V0s_jet) unless seedFit = false.
VertexingUtils::FCCAnalysesVertex
VertexFitter_2Tk_seeded(int Primary,
                        ROOT::VecOps::RVec<edm4hep::TrackState> tracks,
                        bool ComputeMomentaAtVertex = true);

/// Return the tracks that are flagged as coming from the primary vertex
   ROOT::VecOps::RVec<edm4hep::TrackState> get_PrimaryTracks(           ROOT::VecOps::RVec<edm4hep::TrackState> tracks,
                                                                        bool BeamSpotConstraint,
                                                                        double bsc_sigmax, double bsc_sigmay, double bsc_sigmaz,
                                                                        double bsc_x, double bsc_y, double bsc_z ) ;


/// Return the tracks that are NOT flagged as coming from the primary vertex
  ROOT::VecOps::RVec<edm4hep::TrackState>  get_NonPrimaryTracks( ROOT::VecOps::RVec<edm4hep::TrackState> allTracks,
                                                                 ROOT::VecOps::RVec<edm4hep::TrackState> primaryTracks ) ;

/// for an input vector of tracks, return a  vector of bools that tell if the track  was identified as a primary track
   ROOT::VecOps::RVec<bool> IsPrimary_forTracks( ROOT::VecOps::RVec<edm4hep::TrackState> allTracks,
                                                                 ROOT::VecOps::RVec<edm4hep::TrackState> primaryTracks ) ;


/*
  Double_t FastRv(TVectorD p1, TVectorD p2) ;
  TMatrixDSym RegInv3(TMatrixDSym &Smat0) ;
  TMatrixD Fill_A(TVectorD par, Double_t phi) ;
  TVectorD Fill_a(TVectorD par, Double_t phi) ;
  TVectorD Fill_x0(TVectorD par) ;
  TVectorD Fill_x(TVectorD par, Double_t phi) ;

  TVectorD XPtoPar(TVector3 x, TVector3 p, Double_t Q);
  TVector3 ParToP(TVectorD Par);

  TVectorD XPtoPar(TVector3 x, TVector3 p, Double_t Q);
  TVector3 ParToP(TVectorD Par);
*/



}//end NS VertexFitterSimple

}//end NS FCCAnalyses
#endif
