/*
 *  Delphes: a framework for fast simulation of a generic collider experiment
 *  Copyright (C) 2012-2014  Universite catholique de Louvain (UCL), Belgium
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */


/** \class
 *
 *  Lists classes to be included in cint dicitonary
 *
 *  \author P. Demin - UCL, Louvain-la-Neuve
 *
 */

#include "modules/Delphes.h"

#include "modules/AngularSmearing.h"
#include "modules/PhotonConversions.h"
#include "modules/ParticlePropagator.h"
#include "modules/Efficiency.h"
#include "modules/IdentificationMap.h"
#include "modules/EnergySmearing.h"
#include "modules/MomentumSmearing.h"
#include "modules/TrackSmearing.h"
#include "modules/TrackCovariance.h"
#include "modules/ClusterCounting.h"
#include "modules/ImpactParameterSmearing.h"
#include "modules/TimeSmearing.h"
#include "modules/TimeOfFlight.h"
#include "modules/SimpleCalorimeter.h"
#include "modules/DenseTrackFilter.h"
#include "modules/Calorimeter.h"
#include "modules/DualReadoutCalorimeter.h"
#include "modules/OldCalorimeter.h"
#include "modules/Isolation.h"
#include "modules/EnergyScale.h"
#include "modules/UniqueObjectFinder.h"
#include "modules/TrackCountingBTagging.h"
#include "modules/BTagging.h"
#include "modules/TauTagging.h"
#include "modules/TrackCountingTauTagging.h"
#include "modules/TreeWriter.h"
#include "modules/Merger.h"
#include "modules/LeptonDressing.h"
#include "modules/PileUpMerger.h"
#include "modules/JetPileUpSubtractor.h"
#include "modules/TrackPileUpSubtractor.h"
#include "modules/TaggingParticlesSkimmer.h"
#include "modules/PileUpJetID.h"
#include "modules/PhotonID.h"
#include "modules/ConstituentFilter.h"
#include "modules/StatusPidFilter.h"
#include "modules/PdgCodeFilter.h"
#include "modules/BeamSpotFilter.h"
#include "modules/RecoPuFilter.h"
#include "modules/Cloner.h"
#include "modules/Weighter.h"
#include "modules/Hector.h"
#include "modules/JetFlavorAssociation.h"
#include "modules/JetFakeParticle.h"
#include "modules/VertexSorter.h"
#include "modules/VertexFinder.h"
#include "modules/VertexFinderDA4D.h"
#include "modules/DecayFilter.h"
#include "modules/ParticleDensity.h"
#include "modules/TruthVertexFinder.h"
#include "modules/ExampleModule.h"

#ifdef __CINT__

#pragma link off all globals;
#pragma link off all classes;
#pragma link off all functions;

#pragma link C++ class Delphes+;

#pragma link C++ class AngularSmearing+;
#pragma link C++ class PhotonConversions+;
#pragma link C++ class ParticlePropagator+;
#pragma link C++ class Efficiency+;
#pragma link C++ class IdentificationMap+;
#pragma link C++ class EnergySmearing+;
#pragma link C++ class MomentumSmearing+;
#pragma link C++ class TrackSmearing+;
#pragma link C++ class TrackCovariance+;
#pragma link C++ class ClusterCounting+;
#pragma link C++ class ImpactParameterSmearing+;
#pragma link C++ class TimeSmearing+;
#pragma link C++ class TimeOfFlight+;
#pragma link C++ class SimpleCalorimeter+;
#pragma link C++ class DenseTrackFilter+;
#pragma link C++ class Calorimeter+;
#pragma link C++ class DualReadoutCalorimeter+;
#pragma link C++ class OldCalorimeter+;
#pragma link C++ class Isolation+;
#pragma link C++ class EnergyScale+;
#pragma link C++ class UniqueObjectFinder+;
#pragma link C++ class TrackCountingBTagging+;
#pragma link C++ class BTagging+;
#pragma link C++ class TauTagging+;
#pragma link C++ class TrackCountingTauTagging+;
#pragma link C++ class TreeWriter+;
#pragma link C++ class Merger+;
#pragma link C++ class LeptonDressing+;
#pragma link C++ class PileUpMerger+;
#pragma link C++ class JetPileUpSubtractor+;
#pragma link C++ class TrackPileUpSubtractor+;
#pragma link C++ class TaggingParticlesSkimmer+;
#pragma link C++ class PileUpJetID+;
#pragma link C++ class PhotonID+;
#pragma link C++ class ConstituentFilter+;
#pragma link C++ class StatusPidFilter+;
#pragma link C++ class PdgCodeFilter+;
#pragma link C++ class BeamSpotFilter+;
#pragma link C++ class RecoPuFilter+;
#pragma link C++ class Cloner+;
#pragma link C++ class Weighter+;
#pragma link C++ class Hector+;
#pragma link C++ class JetFlavorAssociation+;
#pragma link C++ class JetFakeParticle+;
#pragma link C++ class VertexSorter+;
#pragma link C++ class VertexFinder+;
#pragma link C++ class VertexFinderDA4D+;
#pragma link C++ class DecayFilter+;
#pragma link C++ class ParticleDensity+;
#pragma link C++ class TruthVertexFinder+;
#pragma link C++ class ExampleModule+;

#endif
// Do NOT change. Changes will be lost next time file is generated

#define R__DICTIONARY_FILENAME tmpdImodulesdIModulesDict

/*******************************************************************/
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#define G__DICTIONARY
#include "RConfig.h"
#include "TClass.h"
#include "TDictAttributeMap.h"
#include "TInterpreter.h"
#include "TROOT.h"
#include "TBuffer.h"
#include "TMemberInspector.h"
#include "TInterpreter.h"
#include "TVirtualMutex.h"
#include "TError.h"

#ifndef G__ROOT
#define G__ROOT
#endif

#include "RtypesImp.h"
#include "TIsAProxy.h"
#include "TFileMergeInfo.h"
#include <algorithm>
#include "TCollectionProxyInfo.h"
/*******************************************************************/

#include "TDataMember.h"

// Since CINT ignores the std namespace, we need to do so in this file.
namespace std {} using namespace std;

// Header files passed as explicit arguments
#include "modules/Delphes.h"
#include "modules/AngularSmearing.h"
#include "modules/PhotonConversions.h"
#include "modules/ParticlePropagator.h"
#include "modules/Efficiency.h"
#include "modules/IdentificationMap.h"
#include "modules/EnergySmearing.h"
#include "modules/MomentumSmearing.h"
#include "modules/TrackSmearing.h"
#include "modules/TrackCovariance.h"
#include "modules/ClusterCounting.h"
#include "modules/ImpactParameterSmearing.h"
#include "modules/TimeSmearing.h"
#include "modules/TimeOfFlight.h"
#include "modules/SimpleCalorimeter.h"
#include "modules/DenseTrackFilter.h"
#include "modules/Calorimeter.h"
#include "modules/DualReadoutCalorimeter.h"
#include "modules/OldCalorimeter.h"
#include "modules/Isolation.h"
#include "modules/EnergyScale.h"
#include "modules/UniqueObjectFinder.h"
#include "modules/TrackCountingBTagging.h"
#include "modules/BTagging.h"
#include "modules/TauTagging.h"
#include "modules/TrackCountingTauTagging.h"
#include "modules/TreeWriter.h"
#include "modules/Merger.h"
#include "modules/LeptonDressing.h"
#include "modules/PileUpMerger.h"
#include "modules/JetPileUpSubtractor.h"
#include "modules/TrackPileUpSubtractor.h"
#include "modules/TaggingParticlesSkimmer.h"
#include "modules/PileUpJetID.h"
#include "modules/PhotonID.h"
#include "modules/ConstituentFilter.h"
#include "modules/StatusPidFilter.h"
#include "modules/PdgCodeFilter.h"
#include "modules/BeamSpotFilter.h"
#include "modules/RecoPuFilter.h"
#include "modules/Cloner.h"
#include "modules/Weighter.h"
#include "modules/Hector.h"
#include "modules/JetFlavorAssociation.h"
#include "modules/JetFakeParticle.h"
#include "modules/VertexSorter.h"
#include "modules/VertexFinder.h"
#include "modules/VertexFinderDA4D.h"
#include "modules/DecayFilter.h"
#include "modules/ParticleDensity.h"
#include "modules/TruthVertexFinder.h"
#include "modules/ExampleModule.h"

// Header files passed via #pragma extra_include

namespace ROOT {
   static void *new_Delphes(void *p = 0);
   static void *newArray_Delphes(Long_t size, void *p);
   static void delete_Delphes(void *p);
   static void deleteArray_Delphes(void *p);
   static void destruct_Delphes(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::Delphes*)
   {
      ::Delphes *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::Delphes >(0);
      static ::ROOT::TGenericClassInfo 
         instance("Delphes", ::Delphes::Class_Version(), "modules/Delphes.h", 40,
                  typeid(::Delphes), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::Delphes::Dictionary, isa_proxy, 4,
                  sizeof(::Delphes) );
      instance.SetNew(&new_Delphes);
      instance.SetNewArray(&newArray_Delphes);
      instance.SetDelete(&delete_Delphes);
      instance.SetDeleteArray(&deleteArray_Delphes);
      instance.SetDestructor(&destruct_Delphes);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::Delphes*)
   {
      return GenerateInitInstanceLocal((::Delphes*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::Delphes*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_AngularSmearing(void *p = 0);
   static void *newArray_AngularSmearing(Long_t size, void *p);
   static void delete_AngularSmearing(void *p);
   static void deleteArray_AngularSmearing(void *p);
   static void destruct_AngularSmearing(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::AngularSmearing*)
   {
      ::AngularSmearing *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::AngularSmearing >(0);
      static ::ROOT::TGenericClassInfo 
         instance("AngularSmearing", ::AngularSmearing::Class_Version(), "modules/AngularSmearing.h", 36,
                  typeid(::AngularSmearing), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::AngularSmearing::Dictionary, isa_proxy, 4,
                  sizeof(::AngularSmearing) );
      instance.SetNew(&new_AngularSmearing);
      instance.SetNewArray(&newArray_AngularSmearing);
      instance.SetDelete(&delete_AngularSmearing);
      instance.SetDeleteArray(&deleteArray_AngularSmearing);
      instance.SetDestructor(&destruct_AngularSmearing);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::AngularSmearing*)
   {
      return GenerateInitInstanceLocal((::AngularSmearing*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::AngularSmearing*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_PhotonConversions(void *p = 0);
   static void *newArray_PhotonConversions(Long_t size, void *p);
   static void delete_PhotonConversions(void *p);
   static void deleteArray_PhotonConversions(void *p);
   static void destruct_PhotonConversions(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::PhotonConversions*)
   {
      ::PhotonConversions *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::PhotonConversions >(0);
      static ::ROOT::TGenericClassInfo 
         instance("PhotonConversions", ::PhotonConversions::Class_Version(), "modules/PhotonConversions.h", 37,
                  typeid(::PhotonConversions), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::PhotonConversions::Dictionary, isa_proxy, 4,
                  sizeof(::PhotonConversions) );
      instance.SetNew(&new_PhotonConversions);
      instance.SetNewArray(&newArray_PhotonConversions);
      instance.SetDelete(&delete_PhotonConversions);
      instance.SetDeleteArray(&deleteArray_PhotonConversions);
      instance.SetDestructor(&destruct_PhotonConversions);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::PhotonConversions*)
   {
      return GenerateInitInstanceLocal((::PhotonConversions*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::PhotonConversions*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_ParticlePropagator(void *p = 0);
   static void *newArray_ParticlePropagator(Long_t size, void *p);
   static void delete_ParticlePropagator(void *p);
   static void deleteArray_ParticlePropagator(void *p);
   static void destruct_ParticlePropagator(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::ParticlePropagator*)
   {
      ::ParticlePropagator *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::ParticlePropagator >(0);
      static ::ROOT::TGenericClassInfo 
         instance("ParticlePropagator", ::ParticlePropagator::Class_Version(), "modules/ParticlePropagator.h", 39,
                  typeid(::ParticlePropagator), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::ParticlePropagator::Dictionary, isa_proxy, 4,
                  sizeof(::ParticlePropagator) );
      instance.SetNew(&new_ParticlePropagator);
      instance.SetNewArray(&newArray_ParticlePropagator);
      instance.SetDelete(&delete_ParticlePropagator);
      instance.SetDeleteArray(&deleteArray_ParticlePropagator);
      instance.SetDestructor(&destruct_ParticlePropagator);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::ParticlePropagator*)
   {
      return GenerateInitInstanceLocal((::ParticlePropagator*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::ParticlePropagator*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_Efficiency(void *p = 0);
   static void *newArray_Efficiency(Long_t size, void *p);
   static void delete_Efficiency(void *p);
   static void deleteArray_Efficiency(void *p);
   static void destruct_Efficiency(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::Efficiency*)
   {
      ::Efficiency *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::Efficiency >(0);
      static ::ROOT::TGenericClassInfo 
         instance("Efficiency", ::Efficiency::Class_Version(), "modules/Efficiency.h", 36,
                  typeid(::Efficiency), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::Efficiency::Dictionary, isa_proxy, 4,
                  sizeof(::Efficiency) );
      instance.SetNew(&new_Efficiency);
      instance.SetNewArray(&newArray_Efficiency);
      instance.SetDelete(&delete_Efficiency);
      instance.SetDeleteArray(&deleteArray_Efficiency);
      instance.SetDestructor(&destruct_Efficiency);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::Efficiency*)
   {
      return GenerateInitInstanceLocal((::Efficiency*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::Efficiency*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_IdentificationMap(void *p = 0);
   static void *newArray_IdentificationMap(Long_t size, void *p);
   static void delete_IdentificationMap(void *p);
   static void deleteArray_IdentificationMap(void *p);
   static void destruct_IdentificationMap(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::IdentificationMap*)
   {
      ::IdentificationMap *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::IdentificationMap >(0);
      static ::ROOT::TGenericClassInfo 
         instance("IdentificationMap", ::IdentificationMap::Class_Version(), "modules/IdentificationMap.h", 37,
                  typeid(::IdentificationMap), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::IdentificationMap::Dictionary, isa_proxy, 4,
                  sizeof(::IdentificationMap) );
      instance.SetNew(&new_IdentificationMap);
      instance.SetNewArray(&newArray_IdentificationMap);
      instance.SetDelete(&delete_IdentificationMap);
      instance.SetDeleteArray(&deleteArray_IdentificationMap);
      instance.SetDestructor(&destruct_IdentificationMap);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::IdentificationMap*)
   {
      return GenerateInitInstanceLocal((::IdentificationMap*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::IdentificationMap*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_EnergySmearing(void *p = 0);
   static void *newArray_EnergySmearing(Long_t size, void *p);
   static void delete_EnergySmearing(void *p);
   static void deleteArray_EnergySmearing(void *p);
   static void destruct_EnergySmearing(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::EnergySmearing*)
   {
      ::EnergySmearing *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::EnergySmearing >(0);
      static ::ROOT::TGenericClassInfo 
         instance("EnergySmearing", ::EnergySmearing::Class_Version(), "modules/EnergySmearing.h", 36,
                  typeid(::EnergySmearing), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::EnergySmearing::Dictionary, isa_proxy, 4,
                  sizeof(::EnergySmearing) );
      instance.SetNew(&new_EnergySmearing);
      instance.SetNewArray(&newArray_EnergySmearing);
      instance.SetDelete(&delete_EnergySmearing);
      instance.SetDeleteArray(&deleteArray_EnergySmearing);
      instance.SetDestructor(&destruct_EnergySmearing);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::EnergySmearing*)
   {
      return GenerateInitInstanceLocal((::EnergySmearing*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::EnergySmearing*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_MomentumSmearing(void *p = 0);
   static void *newArray_MomentumSmearing(Long_t size, void *p);
   static void delete_MomentumSmearing(void *p);
   static void deleteArray_MomentumSmearing(void *p);
   static void destruct_MomentumSmearing(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::MomentumSmearing*)
   {
      ::MomentumSmearing *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::MomentumSmearing >(0);
      static ::ROOT::TGenericClassInfo 
         instance("MomentumSmearing", ::MomentumSmearing::Class_Version(), "modules/MomentumSmearing.h", 36,
                  typeid(::MomentumSmearing), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::MomentumSmearing::Dictionary, isa_proxy, 4,
                  sizeof(::MomentumSmearing) );
      instance.SetNew(&new_MomentumSmearing);
      instance.SetNewArray(&newArray_MomentumSmearing);
      instance.SetDelete(&delete_MomentumSmearing);
      instance.SetDeleteArray(&deleteArray_MomentumSmearing);
      instance.SetDestructor(&destruct_MomentumSmearing);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::MomentumSmearing*)
   {
      return GenerateInitInstanceLocal((::MomentumSmearing*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::MomentumSmearing*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_TrackSmearing(void *p = 0);
   static void *newArray_TrackSmearing(Long_t size, void *p);
   static void delete_TrackSmearing(void *p);
   static void deleteArray_TrackSmearing(void *p);
   static void destruct_TrackSmearing(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::TrackSmearing*)
   {
      ::TrackSmearing *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::TrackSmearing >(0);
      static ::ROOT::TGenericClassInfo 
         instance("TrackSmearing", ::TrackSmearing::Class_Version(), "modules/TrackSmearing.h", 20,
                  typeid(::TrackSmearing), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::TrackSmearing::Dictionary, isa_proxy, 4,
                  sizeof(::TrackSmearing) );
      instance.SetNew(&new_TrackSmearing);
      instance.SetNewArray(&newArray_TrackSmearing);
      instance.SetDelete(&delete_TrackSmearing);
      instance.SetDeleteArray(&deleteArray_TrackSmearing);
      instance.SetDestructor(&destruct_TrackSmearing);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::TrackSmearing*)
   {
      return GenerateInitInstanceLocal((::TrackSmearing*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::TrackSmearing*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_TrackCovariance(void *p = 0);
   static void *newArray_TrackCovariance(Long_t size, void *p);
   static void delete_TrackCovariance(void *p);
   static void deleteArray_TrackCovariance(void *p);
   static void destruct_TrackCovariance(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::TrackCovariance*)
   {
      ::TrackCovariance *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::TrackCovariance >(0);
      static ::ROOT::TGenericClassInfo 
         instance("TrackCovariance", ::TrackCovariance::Class_Version(), "modules/TrackCovariance.h", 40,
                  typeid(::TrackCovariance), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::TrackCovariance::Dictionary, isa_proxy, 4,
                  sizeof(::TrackCovariance) );
      instance.SetNew(&new_TrackCovariance);
      instance.SetNewArray(&newArray_TrackCovariance);
      instance.SetDelete(&delete_TrackCovariance);
      instance.SetDeleteArray(&deleteArray_TrackCovariance);
      instance.SetDestructor(&destruct_TrackCovariance);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::TrackCovariance*)
   {
      return GenerateInitInstanceLocal((::TrackCovariance*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::TrackCovariance*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_ClusterCounting(void *p = 0);
   static void *newArray_ClusterCounting(Long_t size, void *p);
   static void delete_ClusterCounting(void *p);
   static void deleteArray_ClusterCounting(void *p);
   static void destruct_ClusterCounting(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::ClusterCounting*)
   {
      ::ClusterCounting *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::ClusterCounting >(0);
      static ::ROOT::TGenericClassInfo 
         instance("ClusterCounting", ::ClusterCounting::Class_Version(), "modules/ClusterCounting.h", 38,
                  typeid(::ClusterCounting), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::ClusterCounting::Dictionary, isa_proxy, 4,
                  sizeof(::ClusterCounting) );
      instance.SetNew(&new_ClusterCounting);
      instance.SetNewArray(&newArray_ClusterCounting);
      instance.SetDelete(&delete_ClusterCounting);
      instance.SetDeleteArray(&deleteArray_ClusterCounting);
      instance.SetDestructor(&destruct_ClusterCounting);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::ClusterCounting*)
   {
      return GenerateInitInstanceLocal((::ClusterCounting*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::ClusterCounting*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_ImpactParameterSmearing(void *p = 0);
   static void *newArray_ImpactParameterSmearing(Long_t size, void *p);
   static void delete_ImpactParameterSmearing(void *p);
   static void deleteArray_ImpactParameterSmearing(void *p);
   static void destruct_ImpactParameterSmearing(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::ImpactParameterSmearing*)
   {
      ::ImpactParameterSmearing *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::ImpactParameterSmearing >(0);
      static ::ROOT::TGenericClassInfo 
         instance("ImpactParameterSmearing", ::ImpactParameterSmearing::Class_Version(), "modules/ImpactParameterSmearing.h", 36,
                  typeid(::ImpactParameterSmearing), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::ImpactParameterSmearing::Dictionary, isa_proxy, 4,
                  sizeof(::ImpactParameterSmearing) );
      instance.SetNew(&new_ImpactParameterSmearing);
      instance.SetNewArray(&newArray_ImpactParameterSmearing);
      instance.SetDelete(&delete_ImpactParameterSmearing);
      instance.SetDeleteArray(&deleteArray_ImpactParameterSmearing);
      instance.SetDestructor(&destruct_ImpactParameterSmearing);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::ImpactParameterSmearing*)
   {
      return GenerateInitInstanceLocal((::ImpactParameterSmearing*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::ImpactParameterSmearing*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_TimeSmearing(void *p = 0);
   static void *newArray_TimeSmearing(Long_t size, void *p);
   static void delete_TimeSmearing(void *p);
   static void deleteArray_TimeSmearing(void *p);
   static void destruct_TimeSmearing(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::TimeSmearing*)
   {
      ::TimeSmearing *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::TimeSmearing >(0);
      static ::ROOT::TGenericClassInfo 
         instance("TimeSmearing", ::TimeSmearing::Class_Version(), "modules/TimeSmearing.h", 36,
                  typeid(::TimeSmearing), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::TimeSmearing::Dictionary, isa_proxy, 4,
                  sizeof(::TimeSmearing) );
      instance.SetNew(&new_TimeSmearing);
      instance.SetNewArray(&newArray_TimeSmearing);
      instance.SetDelete(&delete_TimeSmearing);
      instance.SetDeleteArray(&deleteArray_TimeSmearing);
      instance.SetDestructor(&destruct_TimeSmearing);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::TimeSmearing*)
   {
      return GenerateInitInstanceLocal((::TimeSmearing*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::TimeSmearing*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_TimeOfFlight(void *p = 0);
   static void *newArray_TimeOfFlight(Long_t size, void *p);
   static void delete_TimeOfFlight(void *p);
   static void deleteArray_TimeOfFlight(void *p);
   static void destruct_TimeOfFlight(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::TimeOfFlight*)
   {
      ::TimeOfFlight *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::TimeOfFlight >(0);
      static ::ROOT::TGenericClassInfo 
         instance("TimeOfFlight", ::TimeOfFlight::Class_Version(), "modules/TimeOfFlight.h", 35,
                  typeid(::TimeOfFlight), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::TimeOfFlight::Dictionary, isa_proxy, 4,
                  sizeof(::TimeOfFlight) );
      instance.SetNew(&new_TimeOfFlight);
      instance.SetNewArray(&newArray_TimeOfFlight);
      instance.SetDelete(&delete_TimeOfFlight);
      instance.SetDeleteArray(&deleteArray_TimeOfFlight);
      instance.SetDestructor(&destruct_TimeOfFlight);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::TimeOfFlight*)
   {
      return GenerateInitInstanceLocal((::TimeOfFlight*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::TimeOfFlight*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_SimpleCalorimeter(void *p = 0);
   static void *newArray_SimpleCalorimeter(Long_t size, void *p);
   static void delete_SimpleCalorimeter(void *p);
   static void deleteArray_SimpleCalorimeter(void *p);
   static void destruct_SimpleCalorimeter(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::SimpleCalorimeter*)
   {
      ::SimpleCalorimeter *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::SimpleCalorimeter >(0);
      static ::ROOT::TGenericClassInfo 
         instance("SimpleCalorimeter", ::SimpleCalorimeter::Class_Version(), "modules/SimpleCalorimeter.h", 42,
                  typeid(::SimpleCalorimeter), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::SimpleCalorimeter::Dictionary, isa_proxy, 4,
                  sizeof(::SimpleCalorimeter) );
      instance.SetNew(&new_SimpleCalorimeter);
      instance.SetNewArray(&newArray_SimpleCalorimeter);
      instance.SetDelete(&delete_SimpleCalorimeter);
      instance.SetDeleteArray(&deleteArray_SimpleCalorimeter);
      instance.SetDestructor(&destruct_SimpleCalorimeter);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::SimpleCalorimeter*)
   {
      return GenerateInitInstanceLocal((::SimpleCalorimeter*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::SimpleCalorimeter*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_DenseTrackFilter(void *p = 0);
   static void *newArray_DenseTrackFilter(Long_t size, void *p);
   static void delete_DenseTrackFilter(void *p);
   static void deleteArray_DenseTrackFilter(void *p);
   static void destruct_DenseTrackFilter(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::DenseTrackFilter*)
   {
      ::DenseTrackFilter *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::DenseTrackFilter >(0);
      static ::ROOT::TGenericClassInfo 
         instance("DenseTrackFilter", ::DenseTrackFilter::Class_Version(), "modules/DenseTrackFilter.h", 40,
                  typeid(::DenseTrackFilter), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::DenseTrackFilter::Dictionary, isa_proxy, 4,
                  sizeof(::DenseTrackFilter) );
      instance.SetNew(&new_DenseTrackFilter);
      instance.SetNewArray(&newArray_DenseTrackFilter);
      instance.SetDelete(&delete_DenseTrackFilter);
      instance.SetDeleteArray(&deleteArray_DenseTrackFilter);
      instance.SetDestructor(&destruct_DenseTrackFilter);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::DenseTrackFilter*)
   {
      return GenerateInitInstanceLocal((::DenseTrackFilter*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::DenseTrackFilter*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_Calorimeter(void *p = 0);
   static void *newArray_Calorimeter(Long_t size, void *p);
   static void delete_Calorimeter(void *p);
   static void deleteArray_Calorimeter(void *p);
   static void destruct_Calorimeter(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::Calorimeter*)
   {
      ::Calorimeter *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::Calorimeter >(0);
      static ::ROOT::TGenericClassInfo 
         instance("Calorimeter", ::Calorimeter::Class_Version(), "modules/Calorimeter.h", 41,
                  typeid(::Calorimeter), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::Calorimeter::Dictionary, isa_proxy, 4,
                  sizeof(::Calorimeter) );
      instance.SetNew(&new_Calorimeter);
      instance.SetNewArray(&newArray_Calorimeter);
      instance.SetDelete(&delete_Calorimeter);
      instance.SetDeleteArray(&deleteArray_Calorimeter);
      instance.SetDestructor(&destruct_Calorimeter);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::Calorimeter*)
   {
      return GenerateInitInstanceLocal((::Calorimeter*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::Calorimeter*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_DualReadoutCalorimeter(void *p = 0);
   static void *newArray_DualReadoutCalorimeter(Long_t size, void *p);
   static void delete_DualReadoutCalorimeter(void *p);
   static void deleteArray_DualReadoutCalorimeter(void *p);
   static void destruct_DualReadoutCalorimeter(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::DualReadoutCalorimeter*)
   {
      ::DualReadoutCalorimeter *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::DualReadoutCalorimeter >(0);
      static ::ROOT::TGenericClassInfo 
         instance("DualReadoutCalorimeter", ::DualReadoutCalorimeter::Class_Version(), "modules/DualReadoutCalorimeter.h", 41,
                  typeid(::DualReadoutCalorimeter), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::DualReadoutCalorimeter::Dictionary, isa_proxy, 4,
                  sizeof(::DualReadoutCalorimeter) );
      instance.SetNew(&new_DualReadoutCalorimeter);
      instance.SetNewArray(&newArray_DualReadoutCalorimeter);
      instance.SetDelete(&delete_DualReadoutCalorimeter);
      instance.SetDeleteArray(&deleteArray_DualReadoutCalorimeter);
      instance.SetDestructor(&destruct_DualReadoutCalorimeter);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::DualReadoutCalorimeter*)
   {
      return GenerateInitInstanceLocal((::DualReadoutCalorimeter*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::DualReadoutCalorimeter*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_OldCalorimeter(void *p = 0);
   static void *newArray_OldCalorimeter(Long_t size, void *p);
   static void delete_OldCalorimeter(void *p);
   static void deleteArray_OldCalorimeter(void *p);
   static void destruct_OldCalorimeter(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::OldCalorimeter*)
   {
      ::OldCalorimeter *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::OldCalorimeter >(0);
      static ::ROOT::TGenericClassInfo 
         instance("OldCalorimeter", ::OldCalorimeter::Class_Version(), "modules/OldCalorimeter.h", 27,
                  typeid(::OldCalorimeter), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::OldCalorimeter::Dictionary, isa_proxy, 4,
                  sizeof(::OldCalorimeter) );
      instance.SetNew(&new_OldCalorimeter);
      instance.SetNewArray(&newArray_OldCalorimeter);
      instance.SetDelete(&delete_OldCalorimeter);
      instance.SetDeleteArray(&deleteArray_OldCalorimeter);
      instance.SetDestructor(&destruct_OldCalorimeter);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::OldCalorimeter*)
   {
      return GenerateInitInstanceLocal((::OldCalorimeter*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::OldCalorimeter*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_Isolation(void *p = 0);
   static void *newArray_Isolation(Long_t size, void *p);
   static void delete_Isolation(void *p);
   static void deleteArray_Isolation(void *p);
   static void destruct_Isolation(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::Isolation*)
   {
      ::Isolation *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::Isolation >(0);
      static ::ROOT::TGenericClassInfo 
         instance("Isolation", ::Isolation::Class_Version(), "modules/Isolation.h", 40,
                  typeid(::Isolation), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::Isolation::Dictionary, isa_proxy, 4,
                  sizeof(::Isolation) );
      instance.SetNew(&new_Isolation);
      instance.SetNewArray(&newArray_Isolation);
      instance.SetDelete(&delete_Isolation);
      instance.SetDeleteArray(&deleteArray_Isolation);
      instance.SetDestructor(&destruct_Isolation);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::Isolation*)
   {
      return GenerateInitInstanceLocal((::Isolation*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::Isolation*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_EnergyScale(void *p = 0);
   static void *newArray_EnergyScale(Long_t size, void *p);
   static void delete_EnergyScale(void *p);
   static void deleteArray_EnergyScale(void *p);
   static void destruct_EnergyScale(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::EnergyScale*)
   {
      ::EnergyScale *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::EnergyScale >(0);
      static ::ROOT::TGenericClassInfo 
         instance("EnergyScale", ::EnergyScale::Class_Version(), "modules/EnergyScale.h", 36,
                  typeid(::EnergyScale), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::EnergyScale::Dictionary, isa_proxy, 4,
                  sizeof(::EnergyScale) );
      instance.SetNew(&new_EnergyScale);
      instance.SetNewArray(&newArray_EnergyScale);
      instance.SetDelete(&delete_EnergyScale);
      instance.SetDeleteArray(&deleteArray_EnergyScale);
      instance.SetDestructor(&destruct_EnergyScale);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::EnergyScale*)
   {
      return GenerateInitInstanceLocal((::EnergyScale*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::EnergyScale*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_UniqueObjectFinder(void *p = 0);
   static void *newArray_UniqueObjectFinder(Long_t size, void *p);
   static void delete_UniqueObjectFinder(void *p);
   static void deleteArray_UniqueObjectFinder(void *p);
   static void destruct_UniqueObjectFinder(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::UniqueObjectFinder*)
   {
      ::UniqueObjectFinder *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::UniqueObjectFinder >(0);
      static ::ROOT::TGenericClassInfo 
         instance("UniqueObjectFinder", ::UniqueObjectFinder::Class_Version(), "modules/UniqueObjectFinder.h", 39,
                  typeid(::UniqueObjectFinder), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::UniqueObjectFinder::Dictionary, isa_proxy, 4,
                  sizeof(::UniqueObjectFinder) );
      instance.SetNew(&new_UniqueObjectFinder);
      instance.SetNewArray(&newArray_UniqueObjectFinder);
      instance.SetDelete(&delete_UniqueObjectFinder);
      instance.SetDeleteArray(&deleteArray_UniqueObjectFinder);
      instance.SetDestructor(&destruct_UniqueObjectFinder);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::UniqueObjectFinder*)
   {
      return GenerateInitInstanceLocal((::UniqueObjectFinder*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::UniqueObjectFinder*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_TrackCountingBTagging(void *p = 0);
   static void *newArray_TrackCountingBTagging(Long_t size, void *p);
   static void delete_TrackCountingBTagging(void *p);
   static void deleteArray_TrackCountingBTagging(void *p);
   static void destruct_TrackCountingBTagging(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::TrackCountingBTagging*)
   {
      ::TrackCountingBTagging *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::TrackCountingBTagging >(0);
      static ::ROOT::TGenericClassInfo 
         instance("TrackCountingBTagging", ::TrackCountingBTagging::Class_Version(), "modules/TrackCountingBTagging.h", 36,
                  typeid(::TrackCountingBTagging), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::TrackCountingBTagging::Dictionary, isa_proxy, 4,
                  sizeof(::TrackCountingBTagging) );
      instance.SetNew(&new_TrackCountingBTagging);
      instance.SetNewArray(&newArray_TrackCountingBTagging);
      instance.SetDelete(&delete_TrackCountingBTagging);
      instance.SetDeleteArray(&deleteArray_TrackCountingBTagging);
      instance.SetDestructor(&destruct_TrackCountingBTagging);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::TrackCountingBTagging*)
   {
      return GenerateInitInstanceLocal((::TrackCountingBTagging*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::TrackCountingBTagging*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_BTagging(void *p = 0);
   static void *newArray_BTagging(Long_t size, void *p);
   static void delete_BTagging(void *p);
   static void deleteArray_BTagging(void *p);
   static void destruct_BTagging(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::BTagging*)
   {
      ::BTagging *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::BTagging >(0);
      static ::ROOT::TGenericClassInfo 
         instance("BTagging", ::BTagging::Class_Version(), "modules/BTagging.h", 39,
                  typeid(::BTagging), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::BTagging::Dictionary, isa_proxy, 4,
                  sizeof(::BTagging) );
      instance.SetNew(&new_BTagging);
      instance.SetNewArray(&newArray_BTagging);
      instance.SetDelete(&delete_BTagging);
      instance.SetDeleteArray(&deleteArray_BTagging);
      instance.SetDestructor(&destruct_BTagging);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::BTagging*)
   {
      return GenerateInitInstanceLocal((::BTagging*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::BTagging*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_TauTagging(void *p = 0);
   static void *newArray_TauTagging(Long_t size, void *p);
   static void delete_TauTagging(void *p);
   static void deleteArray_TauTagging(void *p);
   static void destruct_TauTagging(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::TauTagging*)
   {
      ::TauTagging *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::TauTagging >(0);
      static ::ROOT::TGenericClassInfo 
         instance("TauTagging", ::TauTagging::Class_Version(), "modules/TauTagging.h", 45,
                  typeid(::TauTagging), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::TauTagging::Dictionary, isa_proxy, 4,
                  sizeof(::TauTagging) );
      instance.SetNew(&new_TauTagging);
      instance.SetNewArray(&newArray_TauTagging);
      instance.SetDelete(&delete_TauTagging);
      instance.SetDeleteArray(&deleteArray_TauTagging);
      instance.SetDestructor(&destruct_TauTagging);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::TauTagging*)
   {
      return GenerateInitInstanceLocal((::TauTagging*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::TauTagging*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_TrackCountingTauTagging(void *p = 0);
   static void *newArray_TrackCountingTauTagging(Long_t size, void *p);
   static void delete_TrackCountingTauTagging(void *p);
   static void deleteArray_TrackCountingTauTagging(void *p);
   static void destruct_TrackCountingTauTagging(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::TrackCountingTauTagging*)
   {
      ::TrackCountingTauTagging *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::TrackCountingTauTagging >(0);
      static ::ROOT::TGenericClassInfo 
         instance("TrackCountingTauTagging", ::TrackCountingTauTagging::Class_Version(), "modules/TrackCountingTauTagging.h", 28,
                  typeid(::TrackCountingTauTagging), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::TrackCountingTauTagging::Dictionary, isa_proxy, 4,
                  sizeof(::TrackCountingTauTagging) );
      instance.SetNew(&new_TrackCountingTauTagging);
      instance.SetNewArray(&newArray_TrackCountingTauTagging);
      instance.SetDelete(&delete_TrackCountingTauTagging);
      instance.SetDeleteArray(&deleteArray_TrackCountingTauTagging);
      instance.SetDestructor(&destruct_TrackCountingTauTagging);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::TrackCountingTauTagging*)
   {
      return GenerateInitInstanceLocal((::TrackCountingTauTagging*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::TrackCountingTauTagging*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_TreeWriter(void *p = 0);
   static void *newArray_TreeWriter(Long_t size, void *p);
   static void delete_TreeWriter(void *p);
   static void deleteArray_TreeWriter(void *p);
   static void destruct_TreeWriter(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::TreeWriter*)
   {
      ::TreeWriter *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::TreeWriter >(0);
      static ::ROOT::TGenericClassInfo 
         instance("TreeWriter", ::TreeWriter::Class_Version(), "modules/TreeWriter.h", 41,
                  typeid(::TreeWriter), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::TreeWriter::Dictionary, isa_proxy, 4,
                  sizeof(::TreeWriter) );
      instance.SetNew(&new_TreeWriter);
      instance.SetNewArray(&newArray_TreeWriter);
      instance.SetDelete(&delete_TreeWriter);
      instance.SetDeleteArray(&deleteArray_TreeWriter);
      instance.SetDestructor(&destruct_TreeWriter);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::TreeWriter*)
   {
      return GenerateInitInstanceLocal((::TreeWriter*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::TreeWriter*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_Merger(void *p = 0);
   static void *newArray_Merger(Long_t size, void *p);
   static void delete_Merger(void *p);
   static void deleteArray_Merger(void *p);
   static void destruct_Merger(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::Merger*)
   {
      ::Merger *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::Merger >(0);
      static ::ROOT::TGenericClassInfo 
         instance("Merger", ::Merger::Class_Version(), "modules/Merger.h", 38,
                  typeid(::Merger), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::Merger::Dictionary, isa_proxy, 4,
                  sizeof(::Merger) );
      instance.SetNew(&new_Merger);
      instance.SetNewArray(&newArray_Merger);
      instance.SetDelete(&delete_Merger);
      instance.SetDeleteArray(&deleteArray_Merger);
      instance.SetDestructor(&destruct_Merger);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::Merger*)
   {
      return GenerateInitInstanceLocal((::Merger*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::Merger*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_LeptonDressing(void *p = 0);
   static void *newArray_LeptonDressing(Long_t size, void *p);
   static void delete_LeptonDressing(void *p);
   static void deleteArray_LeptonDressing(void *p);
   static void destruct_LeptonDressing(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::LeptonDressing*)
   {
      ::LeptonDressing *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::LeptonDressing >(0);
      static ::ROOT::TGenericClassInfo 
         instance("LeptonDressing", ::LeptonDressing::Class_Version(), "modules/LeptonDressing.h", 33,
                  typeid(::LeptonDressing), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::LeptonDressing::Dictionary, isa_proxy, 4,
                  sizeof(::LeptonDressing) );
      instance.SetNew(&new_LeptonDressing);
      instance.SetNewArray(&newArray_LeptonDressing);
      instance.SetDelete(&delete_LeptonDressing);
      instance.SetDeleteArray(&deleteArray_LeptonDressing);
      instance.SetDestructor(&destruct_LeptonDressing);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::LeptonDressing*)
   {
      return GenerateInitInstanceLocal((::LeptonDressing*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::LeptonDressing*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_PileUpMerger(void *p = 0);
   static void *newArray_PileUpMerger(Long_t size, void *p);
   static void delete_PileUpMerger(void *p);
   static void deleteArray_PileUpMerger(void *p);
   static void destruct_PileUpMerger(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::PileUpMerger*)
   {
      ::PileUpMerger *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::PileUpMerger >(0);
      static ::ROOT::TGenericClassInfo 
         instance("PileUpMerger", ::PileUpMerger::Class_Version(), "modules/PileUpMerger.h", 36,
                  typeid(::PileUpMerger), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::PileUpMerger::Dictionary, isa_proxy, 4,
                  sizeof(::PileUpMerger) );
      instance.SetNew(&new_PileUpMerger);
      instance.SetNewArray(&newArray_PileUpMerger);
      instance.SetDelete(&delete_PileUpMerger);
      instance.SetDeleteArray(&deleteArray_PileUpMerger);
      instance.SetDestructor(&destruct_PileUpMerger);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::PileUpMerger*)
   {
      return GenerateInitInstanceLocal((::PileUpMerger*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::PileUpMerger*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_JetPileUpSubtractor(void *p = 0);
   static void *newArray_JetPileUpSubtractor(Long_t size, void *p);
   static void delete_JetPileUpSubtractor(void *p);
   static void deleteArray_JetPileUpSubtractor(void *p);
   static void destruct_JetPileUpSubtractor(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::JetPileUpSubtractor*)
   {
      ::JetPileUpSubtractor *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::JetPileUpSubtractor >(0);
      static ::ROOT::TGenericClassInfo 
         instance("JetPileUpSubtractor", ::JetPileUpSubtractor::Class_Version(), "modules/JetPileUpSubtractor.h", 36,
                  typeid(::JetPileUpSubtractor), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::JetPileUpSubtractor::Dictionary, isa_proxy, 4,
                  sizeof(::JetPileUpSubtractor) );
      instance.SetNew(&new_JetPileUpSubtractor);
      instance.SetNewArray(&newArray_JetPileUpSubtractor);
      instance.SetDelete(&delete_JetPileUpSubtractor);
      instance.SetDeleteArray(&deleteArray_JetPileUpSubtractor);
      instance.SetDestructor(&destruct_JetPileUpSubtractor);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::JetPileUpSubtractor*)
   {
      return GenerateInitInstanceLocal((::JetPileUpSubtractor*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::JetPileUpSubtractor*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_TrackPileUpSubtractor(void *p = 0);
   static void *newArray_TrackPileUpSubtractor(Long_t size, void *p);
   static void delete_TrackPileUpSubtractor(void *p);
   static void deleteArray_TrackPileUpSubtractor(void *p);
   static void destruct_TrackPileUpSubtractor(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::TrackPileUpSubtractor*)
   {
      ::TrackPileUpSubtractor *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::TrackPileUpSubtractor >(0);
      static ::ROOT::TGenericClassInfo 
         instance("TrackPileUpSubtractor", ::TrackPileUpSubtractor::Class_Version(), "modules/TrackPileUpSubtractor.h", 38,
                  typeid(::TrackPileUpSubtractor), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::TrackPileUpSubtractor::Dictionary, isa_proxy, 4,
                  sizeof(::TrackPileUpSubtractor) );
      instance.SetNew(&new_TrackPileUpSubtractor);
      instance.SetNewArray(&newArray_TrackPileUpSubtractor);
      instance.SetDelete(&delete_TrackPileUpSubtractor);
      instance.SetDeleteArray(&deleteArray_TrackPileUpSubtractor);
      instance.SetDestructor(&destruct_TrackPileUpSubtractor);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::TrackPileUpSubtractor*)
   {
      return GenerateInitInstanceLocal((::TrackPileUpSubtractor*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::TrackPileUpSubtractor*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_TaggingParticlesSkimmer(void *p = 0);
   static void *newArray_TaggingParticlesSkimmer(Long_t size, void *p);
   static void delete_TaggingParticlesSkimmer(void *p);
   static void deleteArray_TaggingParticlesSkimmer(void *p);
   static void destruct_TaggingParticlesSkimmer(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::TaggingParticlesSkimmer*)
   {
      ::TaggingParticlesSkimmer *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::TaggingParticlesSkimmer >(0);
      static ::ROOT::TGenericClassInfo 
         instance("TaggingParticlesSkimmer", ::TaggingParticlesSkimmer::Class_Version(), "modules/TaggingParticlesSkimmer.h", 41,
                  typeid(::TaggingParticlesSkimmer), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::TaggingParticlesSkimmer::Dictionary, isa_proxy, 4,
                  sizeof(::TaggingParticlesSkimmer) );
      instance.SetNew(&new_TaggingParticlesSkimmer);
      instance.SetNewArray(&newArray_TaggingParticlesSkimmer);
      instance.SetDelete(&delete_TaggingParticlesSkimmer);
      instance.SetDeleteArray(&deleteArray_TaggingParticlesSkimmer);
      instance.SetDestructor(&destruct_TaggingParticlesSkimmer);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::TaggingParticlesSkimmer*)
   {
      return GenerateInitInstanceLocal((::TaggingParticlesSkimmer*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::TaggingParticlesSkimmer*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_PileUpJetID(void *p = 0);
   static void *newArray_PileUpJetID(Long_t size, void *p);
   static void delete_PileUpJetID(void *p);
   static void deleteArray_PileUpJetID(void *p);
   static void destruct_PileUpJetID(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::PileUpJetID*)
   {
      ::PileUpJetID *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::PileUpJetID >(0);
      static ::ROOT::TGenericClassInfo 
         instance("PileUpJetID", ::PileUpJetID::Class_Version(), "modules/PileUpJetID.h", 19,
                  typeid(::PileUpJetID), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::PileUpJetID::Dictionary, isa_proxy, 4,
                  sizeof(::PileUpJetID) );
      instance.SetNew(&new_PileUpJetID);
      instance.SetNewArray(&newArray_PileUpJetID);
      instance.SetDelete(&delete_PileUpJetID);
      instance.SetDeleteArray(&deleteArray_PileUpJetID);
      instance.SetDestructor(&destruct_PileUpJetID);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::PileUpJetID*)
   {
      return GenerateInitInstanceLocal((::PileUpJetID*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::PileUpJetID*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_PhotonID(void *p = 0);
   static void *newArray_PhotonID(Long_t size, void *p);
   static void delete_PhotonID(void *p);
   static void deleteArray_PhotonID(void *p);
   static void destruct_PhotonID(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::PhotonID*)
   {
      ::PhotonID *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::PhotonID >(0);
      static ::ROOT::TGenericClassInfo 
         instance("PhotonID", ::PhotonID::Class_Version(), "modules/PhotonID.h", 39,
                  typeid(::PhotonID), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::PhotonID::Dictionary, isa_proxy, 4,
                  sizeof(::PhotonID) );
      instance.SetNew(&new_PhotonID);
      instance.SetNewArray(&newArray_PhotonID);
      instance.SetDelete(&delete_PhotonID);
      instance.SetDeleteArray(&deleteArray_PhotonID);
      instance.SetDestructor(&destruct_PhotonID);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::PhotonID*)
   {
      return GenerateInitInstanceLocal((::PhotonID*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::PhotonID*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_ConstituentFilter(void *p = 0);
   static void *newArray_ConstituentFilter(Long_t size, void *p);
   static void delete_ConstituentFilter(void *p);
   static void deleteArray_ConstituentFilter(void *p);
   static void destruct_ConstituentFilter(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::ConstituentFilter*)
   {
      ::ConstituentFilter *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::ConstituentFilter >(0);
      static ::ROOT::TGenericClassInfo 
         instance("ConstituentFilter", ::ConstituentFilter::Class_Version(), "modules/ConstituentFilter.h", 38,
                  typeid(::ConstituentFilter), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::ConstituentFilter::Dictionary, isa_proxy, 4,
                  sizeof(::ConstituentFilter) );
      instance.SetNew(&new_ConstituentFilter);
      instance.SetNewArray(&newArray_ConstituentFilter);
      instance.SetDelete(&delete_ConstituentFilter);
      instance.SetDeleteArray(&deleteArray_ConstituentFilter);
      instance.SetDestructor(&destruct_ConstituentFilter);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::ConstituentFilter*)
   {
      return GenerateInitInstanceLocal((::ConstituentFilter*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::ConstituentFilter*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_StatusPidFilter(void *p = 0);
   static void *newArray_StatusPidFilter(Long_t size, void *p);
   static void delete_StatusPidFilter(void *p);
   static void deleteArray_StatusPidFilter(void *p);
   static void destruct_StatusPidFilter(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::StatusPidFilter*)
   {
      ::StatusPidFilter *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::StatusPidFilter >(0);
      static ::ROOT::TGenericClassInfo 
         instance("StatusPidFilter", ::StatusPidFilter::Class_Version(), "modules/StatusPidFilter.h", 38,
                  typeid(::StatusPidFilter), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::StatusPidFilter::Dictionary, isa_proxy, 4,
                  sizeof(::StatusPidFilter) );
      instance.SetNew(&new_StatusPidFilter);
      instance.SetNewArray(&newArray_StatusPidFilter);
      instance.SetDelete(&delete_StatusPidFilter);
      instance.SetDeleteArray(&deleteArray_StatusPidFilter);
      instance.SetDestructor(&destruct_StatusPidFilter);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::StatusPidFilter*)
   {
      return GenerateInitInstanceLocal((::StatusPidFilter*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::StatusPidFilter*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_PdgCodeFilter(void *p = 0);
   static void *newArray_PdgCodeFilter(Long_t size, void *p);
   static void delete_PdgCodeFilter(void *p);
   static void deleteArray_PdgCodeFilter(void *p);
   static void destruct_PdgCodeFilter(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::PdgCodeFilter*)
   {
      ::PdgCodeFilter *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::PdgCodeFilter >(0);
      static ::ROOT::TGenericClassInfo 
         instance("PdgCodeFilter", ::PdgCodeFilter::Class_Version(), "modules/PdgCodeFilter.h", 38,
                  typeid(::PdgCodeFilter), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::PdgCodeFilter::Dictionary, isa_proxy, 4,
                  sizeof(::PdgCodeFilter) );
      instance.SetNew(&new_PdgCodeFilter);
      instance.SetNewArray(&newArray_PdgCodeFilter);
      instance.SetDelete(&delete_PdgCodeFilter);
      instance.SetDeleteArray(&deleteArray_PdgCodeFilter);
      instance.SetDestructor(&destruct_PdgCodeFilter);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::PdgCodeFilter*)
   {
      return GenerateInitInstanceLocal((::PdgCodeFilter*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::PdgCodeFilter*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_BeamSpotFilter(void *p = 0);
   static void *newArray_BeamSpotFilter(Long_t size, void *p);
   static void delete_BeamSpotFilter(void *p);
   static void deleteArray_BeamSpotFilter(void *p);
   static void destruct_BeamSpotFilter(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::BeamSpotFilter*)
   {
      ::BeamSpotFilter *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::BeamSpotFilter >(0);
      static ::ROOT::TGenericClassInfo 
         instance("BeamSpotFilter", ::BeamSpotFilter::Class_Version(), "modules/BeamSpotFilter.h", 19,
                  typeid(::BeamSpotFilter), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::BeamSpotFilter::Dictionary, isa_proxy, 4,
                  sizeof(::BeamSpotFilter) );
      instance.SetNew(&new_BeamSpotFilter);
      instance.SetNewArray(&newArray_BeamSpotFilter);
      instance.SetDelete(&delete_BeamSpotFilter);
      instance.SetDeleteArray(&deleteArray_BeamSpotFilter);
      instance.SetDestructor(&destruct_BeamSpotFilter);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::BeamSpotFilter*)
   {
      return GenerateInitInstanceLocal((::BeamSpotFilter*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::BeamSpotFilter*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_RecoPuFilter(void *p = 0);
   static void *newArray_RecoPuFilter(Long_t size, void *p);
   static void delete_RecoPuFilter(void *p);
   static void deleteArray_RecoPuFilter(void *p);
   static void destruct_RecoPuFilter(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::RecoPuFilter*)
   {
      ::RecoPuFilter *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::RecoPuFilter >(0);
      static ::ROOT::TGenericClassInfo 
         instance("RecoPuFilter", ::RecoPuFilter::Class_Version(), "modules/RecoPuFilter.h", 39,
                  typeid(::RecoPuFilter), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::RecoPuFilter::Dictionary, isa_proxy, 4,
                  sizeof(::RecoPuFilter) );
      instance.SetNew(&new_RecoPuFilter);
      instance.SetNewArray(&newArray_RecoPuFilter);
      instance.SetDelete(&delete_RecoPuFilter);
      instance.SetDeleteArray(&deleteArray_RecoPuFilter);
      instance.SetDestructor(&destruct_RecoPuFilter);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::RecoPuFilter*)
   {
      return GenerateInitInstanceLocal((::RecoPuFilter*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::RecoPuFilter*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_Cloner(void *p = 0);
   static void *newArray_Cloner(Long_t size, void *p);
   static void delete_Cloner(void *p);
   static void deleteArray_Cloner(void *p);
   static void destruct_Cloner(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::Cloner*)
   {
      ::Cloner *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::Cloner >(0);
      static ::ROOT::TGenericClassInfo 
         instance("Cloner", ::Cloner::Class_Version(), "modules/Cloner.h", 36,
                  typeid(::Cloner), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::Cloner::Dictionary, isa_proxy, 4,
                  sizeof(::Cloner) );
      instance.SetNew(&new_Cloner);
      instance.SetNewArray(&newArray_Cloner);
      instance.SetDelete(&delete_Cloner);
      instance.SetDeleteArray(&deleteArray_Cloner);
      instance.SetDestructor(&destruct_Cloner);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::Cloner*)
   {
      return GenerateInitInstanceLocal((::Cloner*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::Cloner*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_Weighter(void *p = 0);
   static void *newArray_Weighter(Long_t size, void *p);
   static void delete_Weighter(void *p);
   static void deleteArray_Weighter(void *p);
   static void destruct_Weighter(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::Weighter*)
   {
      ::Weighter *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::Weighter >(0);
      static ::ROOT::TGenericClassInfo 
         instance("Weighter", ::Weighter::Class_Version(), "modules/Weighter.h", 37,
                  typeid(::Weighter), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::Weighter::Dictionary, isa_proxy, 4,
                  sizeof(::Weighter) );
      instance.SetNew(&new_Weighter);
      instance.SetNewArray(&newArray_Weighter);
      instance.SetDelete(&delete_Weighter);
      instance.SetDeleteArray(&deleteArray_Weighter);
      instance.SetDestructor(&destruct_Weighter);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::Weighter*)
   {
      return GenerateInitInstanceLocal((::Weighter*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::Weighter*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_Hector(void *p = 0);
   static void *newArray_Hector(Long_t size, void *p);
   static void delete_Hector(void *p);
   static void deleteArray_Hector(void *p);
   static void destruct_Hector(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::Hector*)
   {
      ::Hector *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::Hector >(0);
      static ::ROOT::TGenericClassInfo 
         instance("Hector", ::Hector::Class_Version(), "modules/Hector.h", 36,
                  typeid(::Hector), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::Hector::Dictionary, isa_proxy, 4,
                  sizeof(::Hector) );
      instance.SetNew(&new_Hector);
      instance.SetNewArray(&newArray_Hector);
      instance.SetDelete(&delete_Hector);
      instance.SetDeleteArray(&deleteArray_Hector);
      instance.SetDestructor(&destruct_Hector);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::Hector*)
   {
      return GenerateInitInstanceLocal((::Hector*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::Hector*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_JetFlavorAssociation(void *p = 0);
   static void *newArray_JetFlavorAssociation(Long_t size, void *p);
   static void delete_JetFlavorAssociation(void *p);
   static void deleteArray_JetFlavorAssociation(void *p);
   static void destruct_JetFlavorAssociation(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::JetFlavorAssociation*)
   {
      ::JetFlavorAssociation *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::JetFlavorAssociation >(0);
      static ::ROOT::TGenericClassInfo 
         instance("JetFlavorAssociation", ::JetFlavorAssociation::Class_Version(), "modules/JetFlavorAssociation.h", 41,
                  typeid(::JetFlavorAssociation), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::JetFlavorAssociation::Dictionary, isa_proxy, 4,
                  sizeof(::JetFlavorAssociation) );
      instance.SetNew(&new_JetFlavorAssociation);
      instance.SetNewArray(&newArray_JetFlavorAssociation);
      instance.SetDelete(&delete_JetFlavorAssociation);
      instance.SetDeleteArray(&deleteArray_JetFlavorAssociation);
      instance.SetDestructor(&destruct_JetFlavorAssociation);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::JetFlavorAssociation*)
   {
      return GenerateInitInstanceLocal((::JetFlavorAssociation*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::JetFlavorAssociation*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_JetFakeParticle(void *p = 0);
   static void *newArray_JetFakeParticle(Long_t size, void *p);
   static void delete_JetFakeParticle(void *p);
   static void deleteArray_JetFakeParticle(void *p);
   static void destruct_JetFakeParticle(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::JetFakeParticle*)
   {
      ::JetFakeParticle *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::JetFakeParticle >(0);
      static ::ROOT::TGenericClassInfo 
         instance("JetFakeParticle", ::JetFakeParticle::Class_Version(), "modules/JetFakeParticle.h", 37,
                  typeid(::JetFakeParticle), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::JetFakeParticle::Dictionary, isa_proxy, 4,
                  sizeof(::JetFakeParticle) );
      instance.SetNew(&new_JetFakeParticle);
      instance.SetNewArray(&newArray_JetFakeParticle);
      instance.SetDelete(&delete_JetFakeParticle);
      instance.SetDeleteArray(&deleteArray_JetFakeParticle);
      instance.SetDestructor(&destruct_JetFakeParticle);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::JetFakeParticle*)
   {
      return GenerateInitInstanceLocal((::JetFakeParticle*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::JetFakeParticle*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_VertexSorter(void *p = 0);
   static void *newArray_VertexSorter(Long_t size, void *p);
   static void delete_VertexSorter(void *p);
   static void deleteArray_VertexSorter(void *p);
   static void destruct_VertexSorter(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::VertexSorter*)
   {
      ::VertexSorter *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::VertexSorter >(0);
      static ::ROOT::TGenericClassInfo 
         instance("VertexSorter", ::VertexSorter::Class_Version(), "modules/VertexSorter.h", 22,
                  typeid(::VertexSorter), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::VertexSorter::Dictionary, isa_proxy, 4,
                  sizeof(::VertexSorter) );
      instance.SetNew(&new_VertexSorter);
      instance.SetNewArray(&newArray_VertexSorter);
      instance.SetDelete(&delete_VertexSorter);
      instance.SetDeleteArray(&deleteArray_VertexSorter);
      instance.SetDestructor(&destruct_VertexSorter);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::VertexSorter*)
   {
      return GenerateInitInstanceLocal((::VertexSorter*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::VertexSorter*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_VertexFinder(void *p = 0);
   static void *newArray_VertexFinder(Long_t size, void *p);
   static void delete_VertexFinder(void *p);
   static void deleteArray_VertexFinder(void *p);
   static void destruct_VertexFinder(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::VertexFinder*)
   {
      ::VertexFinder *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::VertexFinder >(0);
      static ::ROOT::TGenericClassInfo 
         instance("VertexFinder", ::VertexFinder::Class_Version(), "modules/VertexFinder.h", 21,
                  typeid(::VertexFinder), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::VertexFinder::Dictionary, isa_proxy, 4,
                  sizeof(::VertexFinder) );
      instance.SetNew(&new_VertexFinder);
      instance.SetNewArray(&newArray_VertexFinder);
      instance.SetDelete(&delete_VertexFinder);
      instance.SetDeleteArray(&deleteArray_VertexFinder);
      instance.SetDestructor(&destruct_VertexFinder);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::VertexFinder*)
   {
      return GenerateInitInstanceLocal((::VertexFinder*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::VertexFinder*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_VertexFinderDA4D(void *p = 0);
   static void *newArray_VertexFinderDA4D(Long_t size, void *p);
   static void delete_VertexFinderDA4D(void *p);
   static void deleteArray_VertexFinderDA4D(void *p);
   static void destruct_VertexFinderDA4D(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::VertexFinderDA4D*)
   {
      ::VertexFinderDA4D *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::VertexFinderDA4D >(0);
      static ::ROOT::TGenericClassInfo 
         instance("VertexFinderDA4D", ::VertexFinderDA4D::Class_Version(), "modules/VertexFinderDA4D.h", 20,
                  typeid(::VertexFinderDA4D), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::VertexFinderDA4D::Dictionary, isa_proxy, 4,
                  sizeof(::VertexFinderDA4D) );
      instance.SetNew(&new_VertexFinderDA4D);
      instance.SetNewArray(&newArray_VertexFinderDA4D);
      instance.SetDelete(&delete_VertexFinderDA4D);
      instance.SetDeleteArray(&deleteArray_VertexFinderDA4D);
      instance.SetDestructor(&destruct_VertexFinderDA4D);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::VertexFinderDA4D*)
   {
      return GenerateInitInstanceLocal((::VertexFinderDA4D*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::VertexFinderDA4D*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_DecayFilter(void *p = 0);
   static void *newArray_DecayFilter(Long_t size, void *p);
   static void delete_DecayFilter(void *p);
   static void deleteArray_DecayFilter(void *p);
   static void destruct_DecayFilter(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::DecayFilter*)
   {
      ::DecayFilter *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::DecayFilter >(0);
      static ::ROOT::TGenericClassInfo 
         instance("DecayFilter", ::DecayFilter::Class_Version(), "modules/DecayFilter.h", 43,
                  typeid(::DecayFilter), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::DecayFilter::Dictionary, isa_proxy, 4,
                  sizeof(::DecayFilter) );
      instance.SetNew(&new_DecayFilter);
      instance.SetNewArray(&newArray_DecayFilter);
      instance.SetDelete(&delete_DecayFilter);
      instance.SetDeleteArray(&deleteArray_DecayFilter);
      instance.SetDestructor(&destruct_DecayFilter);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::DecayFilter*)
   {
      return GenerateInitInstanceLocal((::DecayFilter*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::DecayFilter*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_ParticleDensity(void *p = 0);
   static void *newArray_ParticleDensity(Long_t size, void *p);
   static void delete_ParticleDensity(void *p);
   static void deleteArray_ParticleDensity(void *p);
   static void destruct_ParticleDensity(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::ParticleDensity*)
   {
      ::ParticleDensity *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::ParticleDensity >(0);
      static ::ROOT::TGenericClassInfo 
         instance("ParticleDensity", ::ParticleDensity::Class_Version(), "modules/ParticleDensity.h", 38,
                  typeid(::ParticleDensity), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::ParticleDensity::Dictionary, isa_proxy, 4,
                  sizeof(::ParticleDensity) );
      instance.SetNew(&new_ParticleDensity);
      instance.SetNewArray(&newArray_ParticleDensity);
      instance.SetDelete(&delete_ParticleDensity);
      instance.SetDeleteArray(&deleteArray_ParticleDensity);
      instance.SetDestructor(&destruct_ParticleDensity);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::ParticleDensity*)
   {
      return GenerateInitInstanceLocal((::ParticleDensity*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::ParticleDensity*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_TruthVertexFinder(void *p = 0);
   static void *newArray_TruthVertexFinder(Long_t size, void *p);
   static void delete_TruthVertexFinder(void *p);
   static void deleteArray_TruthVertexFinder(void *p);
   static void destruct_TruthVertexFinder(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::TruthVertexFinder*)
   {
      ::TruthVertexFinder *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::TruthVertexFinder >(0);
      static ::ROOT::TGenericClassInfo 
         instance("TruthVertexFinder", ::TruthVertexFinder::Class_Version(), "modules/TruthVertexFinder.h", 34,
                  typeid(::TruthVertexFinder), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::TruthVertexFinder::Dictionary, isa_proxy, 4,
                  sizeof(::TruthVertexFinder) );
      instance.SetNew(&new_TruthVertexFinder);
      instance.SetNewArray(&newArray_TruthVertexFinder);
      instance.SetDelete(&delete_TruthVertexFinder);
      instance.SetDeleteArray(&deleteArray_TruthVertexFinder);
      instance.SetDestructor(&destruct_TruthVertexFinder);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::TruthVertexFinder*)
   {
      return GenerateInitInstanceLocal((::TruthVertexFinder*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::TruthVertexFinder*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_ExampleModule(void *p = 0);
   static void *newArray_ExampleModule(Long_t size, void *p);
   static void delete_ExampleModule(void *p);
   static void deleteArray_ExampleModule(void *p);
   static void destruct_ExampleModule(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::ExampleModule*)
   {
      ::ExampleModule *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::ExampleModule >(0);
      static ::ROOT::TGenericClassInfo 
         instance("ExampleModule", ::ExampleModule::Class_Version(), "modules/ExampleModule.h", 37,
                  typeid(::ExampleModule), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::ExampleModule::Dictionary, isa_proxy, 4,
                  sizeof(::ExampleModule) );
      instance.SetNew(&new_ExampleModule);
      instance.SetNewArray(&newArray_ExampleModule);
      instance.SetDelete(&delete_ExampleModule);
      instance.SetDeleteArray(&deleteArray_ExampleModule);
      instance.SetDestructor(&destruct_ExampleModule);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::ExampleModule*)
   {
      return GenerateInitInstanceLocal((::ExampleModule*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::ExampleModule*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

//______________________________________________________________________________
atomic_TClass_ptr Delphes::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *Delphes::Class_Name()
{
   return "Delphes";
}

//______________________________________________________________________________
const char *Delphes::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::Delphes*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int Delphes::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::Delphes*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *Delphes::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::Delphes*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *Delphes::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::Delphes*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr AngularSmearing::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *AngularSmearing::Class_Name()
{
   return "AngularSmearing";
}

//______________________________________________________________________________
const char *AngularSmearing::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::AngularSmearing*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int AngularSmearing::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::AngularSmearing*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *AngularSmearing::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::AngularSmearing*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *AngularSmearing::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::AngularSmearing*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr PhotonConversions::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *PhotonConversions::Class_Name()
{
   return "PhotonConversions";
}

//______________________________________________________________________________
const char *PhotonConversions::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::PhotonConversions*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int PhotonConversions::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::PhotonConversions*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *PhotonConversions::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::PhotonConversions*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *PhotonConversions::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::PhotonConversions*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr ParticlePropagator::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *ParticlePropagator::Class_Name()
{
   return "ParticlePropagator";
}

//______________________________________________________________________________
const char *ParticlePropagator::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::ParticlePropagator*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int ParticlePropagator::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::ParticlePropagator*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *ParticlePropagator::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::ParticlePropagator*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *ParticlePropagator::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::ParticlePropagator*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr Efficiency::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *Efficiency::Class_Name()
{
   return "Efficiency";
}

//______________________________________________________________________________
const char *Efficiency::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::Efficiency*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int Efficiency::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::Efficiency*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *Efficiency::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::Efficiency*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *Efficiency::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::Efficiency*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr IdentificationMap::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *IdentificationMap::Class_Name()
{
   return "IdentificationMap";
}

//______________________________________________________________________________
const char *IdentificationMap::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::IdentificationMap*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int IdentificationMap::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::IdentificationMap*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *IdentificationMap::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::IdentificationMap*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *IdentificationMap::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::IdentificationMap*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr EnergySmearing::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *EnergySmearing::Class_Name()
{
   return "EnergySmearing";
}

//______________________________________________________________________________
const char *EnergySmearing::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::EnergySmearing*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int EnergySmearing::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::EnergySmearing*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *EnergySmearing::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::EnergySmearing*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *EnergySmearing::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::EnergySmearing*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr MomentumSmearing::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *MomentumSmearing::Class_Name()
{
   return "MomentumSmearing";
}

//______________________________________________________________________________
const char *MomentumSmearing::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::MomentumSmearing*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int MomentumSmearing::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::MomentumSmearing*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *MomentumSmearing::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::MomentumSmearing*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *MomentumSmearing::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::MomentumSmearing*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr TrackSmearing::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *TrackSmearing::Class_Name()
{
   return "TrackSmearing";
}

//______________________________________________________________________________
const char *TrackSmearing::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::TrackSmearing*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int TrackSmearing::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::TrackSmearing*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *TrackSmearing::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::TrackSmearing*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *TrackSmearing::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::TrackSmearing*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr TrackCovariance::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *TrackCovariance::Class_Name()
{
   return "TrackCovariance";
}

//______________________________________________________________________________
const char *TrackCovariance::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::TrackCovariance*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int TrackCovariance::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::TrackCovariance*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *TrackCovariance::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::TrackCovariance*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *TrackCovariance::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::TrackCovariance*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr ClusterCounting::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *ClusterCounting::Class_Name()
{
   return "ClusterCounting";
}

//______________________________________________________________________________
const char *ClusterCounting::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::ClusterCounting*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int ClusterCounting::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::ClusterCounting*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *ClusterCounting::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::ClusterCounting*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *ClusterCounting::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::ClusterCounting*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr ImpactParameterSmearing::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *ImpactParameterSmearing::Class_Name()
{
   return "ImpactParameterSmearing";
}

//______________________________________________________________________________
const char *ImpactParameterSmearing::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::ImpactParameterSmearing*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int ImpactParameterSmearing::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::ImpactParameterSmearing*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *ImpactParameterSmearing::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::ImpactParameterSmearing*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *ImpactParameterSmearing::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::ImpactParameterSmearing*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr TimeSmearing::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *TimeSmearing::Class_Name()
{
   return "TimeSmearing";
}

//______________________________________________________________________________
const char *TimeSmearing::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::TimeSmearing*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int TimeSmearing::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::TimeSmearing*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *TimeSmearing::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::TimeSmearing*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *TimeSmearing::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::TimeSmearing*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr TimeOfFlight::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *TimeOfFlight::Class_Name()
{
   return "TimeOfFlight";
}

//______________________________________________________________________________
const char *TimeOfFlight::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::TimeOfFlight*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int TimeOfFlight::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::TimeOfFlight*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *TimeOfFlight::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::TimeOfFlight*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *TimeOfFlight::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::TimeOfFlight*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr SimpleCalorimeter::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *SimpleCalorimeter::Class_Name()
{
   return "SimpleCalorimeter";
}

//______________________________________________________________________________
const char *SimpleCalorimeter::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::SimpleCalorimeter*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int SimpleCalorimeter::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::SimpleCalorimeter*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *SimpleCalorimeter::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::SimpleCalorimeter*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *SimpleCalorimeter::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::SimpleCalorimeter*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr DenseTrackFilter::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *DenseTrackFilter::Class_Name()
{
   return "DenseTrackFilter";
}

//______________________________________________________________________________
const char *DenseTrackFilter::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::DenseTrackFilter*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int DenseTrackFilter::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::DenseTrackFilter*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *DenseTrackFilter::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::DenseTrackFilter*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *DenseTrackFilter::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::DenseTrackFilter*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr Calorimeter::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *Calorimeter::Class_Name()
{
   return "Calorimeter";
}

//______________________________________________________________________________
const char *Calorimeter::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::Calorimeter*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int Calorimeter::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::Calorimeter*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *Calorimeter::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::Calorimeter*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *Calorimeter::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::Calorimeter*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr DualReadoutCalorimeter::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *DualReadoutCalorimeter::Class_Name()
{
   return "DualReadoutCalorimeter";
}

//______________________________________________________________________________
const char *DualReadoutCalorimeter::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::DualReadoutCalorimeter*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int DualReadoutCalorimeter::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::DualReadoutCalorimeter*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *DualReadoutCalorimeter::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::DualReadoutCalorimeter*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *DualReadoutCalorimeter::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::DualReadoutCalorimeter*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr OldCalorimeter::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *OldCalorimeter::Class_Name()
{
   return "OldCalorimeter";
}

//______________________________________________________________________________
const char *OldCalorimeter::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::OldCalorimeter*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int OldCalorimeter::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::OldCalorimeter*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *OldCalorimeter::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::OldCalorimeter*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *OldCalorimeter::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::OldCalorimeter*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr Isolation::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *Isolation::Class_Name()
{
   return "Isolation";
}

//______________________________________________________________________________
const char *Isolation::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::Isolation*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int Isolation::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::Isolation*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *Isolation::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::Isolation*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *Isolation::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::Isolation*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr EnergyScale::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *EnergyScale::Class_Name()
{
   return "EnergyScale";
}

//______________________________________________________________________________
const char *EnergyScale::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::EnergyScale*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int EnergyScale::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::EnergyScale*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *EnergyScale::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::EnergyScale*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *EnergyScale::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::EnergyScale*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr UniqueObjectFinder::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *UniqueObjectFinder::Class_Name()
{
   return "UniqueObjectFinder";
}

//______________________________________________________________________________
const char *UniqueObjectFinder::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::UniqueObjectFinder*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int UniqueObjectFinder::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::UniqueObjectFinder*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *UniqueObjectFinder::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::UniqueObjectFinder*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *UniqueObjectFinder::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::UniqueObjectFinder*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr TrackCountingBTagging::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *TrackCountingBTagging::Class_Name()
{
   return "TrackCountingBTagging";
}

//______________________________________________________________________________
const char *TrackCountingBTagging::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::TrackCountingBTagging*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int TrackCountingBTagging::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::TrackCountingBTagging*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *TrackCountingBTagging::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::TrackCountingBTagging*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *TrackCountingBTagging::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::TrackCountingBTagging*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr BTagging::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *BTagging::Class_Name()
{
   return "BTagging";
}

//______________________________________________________________________________
const char *BTagging::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::BTagging*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int BTagging::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::BTagging*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *BTagging::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::BTagging*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *BTagging::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::BTagging*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr TauTagging::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *TauTagging::Class_Name()
{
   return "TauTagging";
}

//______________________________________________________________________________
const char *TauTagging::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::TauTagging*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int TauTagging::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::TauTagging*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *TauTagging::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::TauTagging*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *TauTagging::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::TauTagging*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr TrackCountingTauTagging::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *TrackCountingTauTagging::Class_Name()
{
   return "TrackCountingTauTagging";
}

//______________________________________________________________________________
const char *TrackCountingTauTagging::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::TrackCountingTauTagging*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int TrackCountingTauTagging::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::TrackCountingTauTagging*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *TrackCountingTauTagging::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::TrackCountingTauTagging*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *TrackCountingTauTagging::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::TrackCountingTauTagging*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr TreeWriter::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *TreeWriter::Class_Name()
{
   return "TreeWriter";
}

//______________________________________________________________________________
const char *TreeWriter::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::TreeWriter*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int TreeWriter::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::TreeWriter*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *TreeWriter::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::TreeWriter*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *TreeWriter::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::TreeWriter*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr Merger::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *Merger::Class_Name()
{
   return "Merger";
}

//______________________________________________________________________________
const char *Merger::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::Merger*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int Merger::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::Merger*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *Merger::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::Merger*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *Merger::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::Merger*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr LeptonDressing::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *LeptonDressing::Class_Name()
{
   return "LeptonDressing";
}

//______________________________________________________________________________
const char *LeptonDressing::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::LeptonDressing*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int LeptonDressing::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::LeptonDressing*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *LeptonDressing::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::LeptonDressing*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *LeptonDressing::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::LeptonDressing*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr PileUpMerger::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *PileUpMerger::Class_Name()
{
   return "PileUpMerger";
}

//______________________________________________________________________________
const char *PileUpMerger::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::PileUpMerger*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int PileUpMerger::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::PileUpMerger*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *PileUpMerger::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::PileUpMerger*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *PileUpMerger::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::PileUpMerger*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr JetPileUpSubtractor::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *JetPileUpSubtractor::Class_Name()
{
   return "JetPileUpSubtractor";
}

//______________________________________________________________________________
const char *JetPileUpSubtractor::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::JetPileUpSubtractor*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int JetPileUpSubtractor::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::JetPileUpSubtractor*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *JetPileUpSubtractor::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::JetPileUpSubtractor*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *JetPileUpSubtractor::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::JetPileUpSubtractor*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr TrackPileUpSubtractor::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *TrackPileUpSubtractor::Class_Name()
{
   return "TrackPileUpSubtractor";
}

//______________________________________________________________________________
const char *TrackPileUpSubtractor::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::TrackPileUpSubtractor*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int TrackPileUpSubtractor::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::TrackPileUpSubtractor*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *TrackPileUpSubtractor::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::TrackPileUpSubtractor*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *TrackPileUpSubtractor::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::TrackPileUpSubtractor*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr TaggingParticlesSkimmer::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *TaggingParticlesSkimmer::Class_Name()
{
   return "TaggingParticlesSkimmer";
}

//______________________________________________________________________________
const char *TaggingParticlesSkimmer::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::TaggingParticlesSkimmer*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int TaggingParticlesSkimmer::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::TaggingParticlesSkimmer*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *TaggingParticlesSkimmer::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::TaggingParticlesSkimmer*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *TaggingParticlesSkimmer::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::TaggingParticlesSkimmer*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr PileUpJetID::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *PileUpJetID::Class_Name()
{
   return "PileUpJetID";
}

//______________________________________________________________________________
const char *PileUpJetID::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::PileUpJetID*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int PileUpJetID::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::PileUpJetID*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *PileUpJetID::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::PileUpJetID*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *PileUpJetID::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::PileUpJetID*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr PhotonID::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *PhotonID::Class_Name()
{
   return "PhotonID";
}

//______________________________________________________________________________
const char *PhotonID::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::PhotonID*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int PhotonID::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::PhotonID*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *PhotonID::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::PhotonID*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *PhotonID::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::PhotonID*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr ConstituentFilter::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *ConstituentFilter::Class_Name()
{
   return "ConstituentFilter";
}

//______________________________________________________________________________
const char *ConstituentFilter::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::ConstituentFilter*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int ConstituentFilter::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::ConstituentFilter*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *ConstituentFilter::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::ConstituentFilter*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *ConstituentFilter::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::ConstituentFilter*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr StatusPidFilter::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *StatusPidFilter::Class_Name()
{
   return "StatusPidFilter";
}

//______________________________________________________________________________
const char *StatusPidFilter::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::StatusPidFilter*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int StatusPidFilter::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::StatusPidFilter*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *StatusPidFilter::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::StatusPidFilter*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *StatusPidFilter::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::StatusPidFilter*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr PdgCodeFilter::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *PdgCodeFilter::Class_Name()
{
   return "PdgCodeFilter";
}

//______________________________________________________________________________
const char *PdgCodeFilter::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::PdgCodeFilter*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int PdgCodeFilter::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::PdgCodeFilter*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *PdgCodeFilter::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::PdgCodeFilter*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *PdgCodeFilter::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::PdgCodeFilter*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr BeamSpotFilter::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *BeamSpotFilter::Class_Name()
{
   return "BeamSpotFilter";
}

//______________________________________________________________________________
const char *BeamSpotFilter::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::BeamSpotFilter*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int BeamSpotFilter::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::BeamSpotFilter*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *BeamSpotFilter::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::BeamSpotFilter*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *BeamSpotFilter::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::BeamSpotFilter*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr RecoPuFilter::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *RecoPuFilter::Class_Name()
{
   return "RecoPuFilter";
}

//______________________________________________________________________________
const char *RecoPuFilter::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::RecoPuFilter*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int RecoPuFilter::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::RecoPuFilter*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *RecoPuFilter::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::RecoPuFilter*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *RecoPuFilter::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::RecoPuFilter*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr Cloner::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *Cloner::Class_Name()
{
   return "Cloner";
}

//______________________________________________________________________________
const char *Cloner::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::Cloner*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int Cloner::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::Cloner*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *Cloner::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::Cloner*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *Cloner::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::Cloner*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr Weighter::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *Weighter::Class_Name()
{
   return "Weighter";
}

//______________________________________________________________________________
const char *Weighter::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::Weighter*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int Weighter::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::Weighter*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *Weighter::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::Weighter*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *Weighter::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::Weighter*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr Hector::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *Hector::Class_Name()
{
   return "Hector";
}

//______________________________________________________________________________
const char *Hector::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::Hector*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int Hector::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::Hector*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *Hector::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::Hector*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *Hector::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::Hector*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr JetFlavorAssociation::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *JetFlavorAssociation::Class_Name()
{
   return "JetFlavorAssociation";
}

//______________________________________________________________________________
const char *JetFlavorAssociation::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::JetFlavorAssociation*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int JetFlavorAssociation::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::JetFlavorAssociation*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *JetFlavorAssociation::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::JetFlavorAssociation*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *JetFlavorAssociation::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::JetFlavorAssociation*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr JetFakeParticle::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *JetFakeParticle::Class_Name()
{
   return "JetFakeParticle";
}

//______________________________________________________________________________
const char *JetFakeParticle::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::JetFakeParticle*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int JetFakeParticle::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::JetFakeParticle*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *JetFakeParticle::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::JetFakeParticle*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *JetFakeParticle::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::JetFakeParticle*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr VertexSorter::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *VertexSorter::Class_Name()
{
   return "VertexSorter";
}

//______________________________________________________________________________
const char *VertexSorter::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::VertexSorter*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int VertexSorter::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::VertexSorter*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *VertexSorter::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::VertexSorter*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *VertexSorter::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::VertexSorter*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr VertexFinder::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *VertexFinder::Class_Name()
{
   return "VertexFinder";
}

//______________________________________________________________________________
const char *VertexFinder::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::VertexFinder*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int VertexFinder::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::VertexFinder*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *VertexFinder::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::VertexFinder*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *VertexFinder::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::VertexFinder*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr VertexFinderDA4D::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *VertexFinderDA4D::Class_Name()
{
   return "VertexFinderDA4D";
}

//______________________________________________________________________________
const char *VertexFinderDA4D::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::VertexFinderDA4D*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int VertexFinderDA4D::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::VertexFinderDA4D*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *VertexFinderDA4D::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::VertexFinderDA4D*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *VertexFinderDA4D::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::VertexFinderDA4D*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr DecayFilter::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *DecayFilter::Class_Name()
{
   return "DecayFilter";
}

//______________________________________________________________________________
const char *DecayFilter::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::DecayFilter*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int DecayFilter::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::DecayFilter*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *DecayFilter::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::DecayFilter*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *DecayFilter::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::DecayFilter*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr ParticleDensity::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *ParticleDensity::Class_Name()
{
   return "ParticleDensity";
}

//______________________________________________________________________________
const char *ParticleDensity::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::ParticleDensity*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int ParticleDensity::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::ParticleDensity*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *ParticleDensity::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::ParticleDensity*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *ParticleDensity::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::ParticleDensity*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr TruthVertexFinder::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *TruthVertexFinder::Class_Name()
{
   return "TruthVertexFinder";
}

//______________________________________________________________________________
const char *TruthVertexFinder::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::TruthVertexFinder*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int TruthVertexFinder::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::TruthVertexFinder*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *TruthVertexFinder::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::TruthVertexFinder*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *TruthVertexFinder::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::TruthVertexFinder*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr ExampleModule::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *ExampleModule::Class_Name()
{
   return "ExampleModule";
}

//______________________________________________________________________________
const char *ExampleModule::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::ExampleModule*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int ExampleModule::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::ExampleModule*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *ExampleModule::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::ExampleModule*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *ExampleModule::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::ExampleModule*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
void Delphes::Streamer(TBuffer &R__b)
{
   // Stream an object of class Delphes.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(Delphes::Class(),this);
   } else {
      R__b.WriteClassBuffer(Delphes::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_Delphes(void *p) {
      return  p ? new(p) ::Delphes : new ::Delphes;
   }
   static void *newArray_Delphes(Long_t nElements, void *p) {
      return p ? new(p) ::Delphes[nElements] : new ::Delphes[nElements];
   }
   // Wrapper around operator delete
   static void delete_Delphes(void *p) {
      delete ((::Delphes*)p);
   }
   static void deleteArray_Delphes(void *p) {
      delete [] ((::Delphes*)p);
   }
   static void destruct_Delphes(void *p) {
      typedef ::Delphes current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::Delphes

//______________________________________________________________________________
void AngularSmearing::Streamer(TBuffer &R__b)
{
   // Stream an object of class AngularSmearing.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(AngularSmearing::Class(),this);
   } else {
      R__b.WriteClassBuffer(AngularSmearing::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_AngularSmearing(void *p) {
      return  p ? new(p) ::AngularSmearing : new ::AngularSmearing;
   }
   static void *newArray_AngularSmearing(Long_t nElements, void *p) {
      return p ? new(p) ::AngularSmearing[nElements] : new ::AngularSmearing[nElements];
   }
   // Wrapper around operator delete
   static void delete_AngularSmearing(void *p) {
      delete ((::AngularSmearing*)p);
   }
   static void deleteArray_AngularSmearing(void *p) {
      delete [] ((::AngularSmearing*)p);
   }
   static void destruct_AngularSmearing(void *p) {
      typedef ::AngularSmearing current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::AngularSmearing

//______________________________________________________________________________
void PhotonConversions::Streamer(TBuffer &R__b)
{
   // Stream an object of class PhotonConversions.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(PhotonConversions::Class(),this);
   } else {
      R__b.WriteClassBuffer(PhotonConversions::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_PhotonConversions(void *p) {
      return  p ? new(p) ::PhotonConversions : new ::PhotonConversions;
   }
   static void *newArray_PhotonConversions(Long_t nElements, void *p) {
      return p ? new(p) ::PhotonConversions[nElements] : new ::PhotonConversions[nElements];
   }
   // Wrapper around operator delete
   static void delete_PhotonConversions(void *p) {
      delete ((::PhotonConversions*)p);
   }
   static void deleteArray_PhotonConversions(void *p) {
      delete [] ((::PhotonConversions*)p);
   }
   static void destruct_PhotonConversions(void *p) {
      typedef ::PhotonConversions current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::PhotonConversions

//______________________________________________________________________________
void ParticlePropagator::Streamer(TBuffer &R__b)
{
   // Stream an object of class ParticlePropagator.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(ParticlePropagator::Class(),this);
   } else {
      R__b.WriteClassBuffer(ParticlePropagator::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_ParticlePropagator(void *p) {
      return  p ? new(p) ::ParticlePropagator : new ::ParticlePropagator;
   }
   static void *newArray_ParticlePropagator(Long_t nElements, void *p) {
      return p ? new(p) ::ParticlePropagator[nElements] : new ::ParticlePropagator[nElements];
   }
   // Wrapper around operator delete
   static void delete_ParticlePropagator(void *p) {
      delete ((::ParticlePropagator*)p);
   }
   static void deleteArray_ParticlePropagator(void *p) {
      delete [] ((::ParticlePropagator*)p);
   }
   static void destruct_ParticlePropagator(void *p) {
      typedef ::ParticlePropagator current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::ParticlePropagator

//______________________________________________________________________________
void Efficiency::Streamer(TBuffer &R__b)
{
   // Stream an object of class Efficiency.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(Efficiency::Class(),this);
   } else {
      R__b.WriteClassBuffer(Efficiency::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_Efficiency(void *p) {
      return  p ? new(p) ::Efficiency : new ::Efficiency;
   }
   static void *newArray_Efficiency(Long_t nElements, void *p) {
      return p ? new(p) ::Efficiency[nElements] : new ::Efficiency[nElements];
   }
   // Wrapper around operator delete
   static void delete_Efficiency(void *p) {
      delete ((::Efficiency*)p);
   }
   static void deleteArray_Efficiency(void *p) {
      delete [] ((::Efficiency*)p);
   }
   static void destruct_Efficiency(void *p) {
      typedef ::Efficiency current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::Efficiency

//______________________________________________________________________________
void IdentificationMap::Streamer(TBuffer &R__b)
{
   // Stream an object of class IdentificationMap.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(IdentificationMap::Class(),this);
   } else {
      R__b.WriteClassBuffer(IdentificationMap::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_IdentificationMap(void *p) {
      return  p ? new(p) ::IdentificationMap : new ::IdentificationMap;
   }
   static void *newArray_IdentificationMap(Long_t nElements, void *p) {
      return p ? new(p) ::IdentificationMap[nElements] : new ::IdentificationMap[nElements];
   }
   // Wrapper around operator delete
   static void delete_IdentificationMap(void *p) {
      delete ((::IdentificationMap*)p);
   }
   static void deleteArray_IdentificationMap(void *p) {
      delete [] ((::IdentificationMap*)p);
   }
   static void destruct_IdentificationMap(void *p) {
      typedef ::IdentificationMap current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::IdentificationMap

//______________________________________________________________________________
void EnergySmearing::Streamer(TBuffer &R__b)
{
   // Stream an object of class EnergySmearing.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(EnergySmearing::Class(),this);
   } else {
      R__b.WriteClassBuffer(EnergySmearing::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_EnergySmearing(void *p) {
      return  p ? new(p) ::EnergySmearing : new ::EnergySmearing;
   }
   static void *newArray_EnergySmearing(Long_t nElements, void *p) {
      return p ? new(p) ::EnergySmearing[nElements] : new ::EnergySmearing[nElements];
   }
   // Wrapper around operator delete
   static void delete_EnergySmearing(void *p) {
      delete ((::EnergySmearing*)p);
   }
   static void deleteArray_EnergySmearing(void *p) {
      delete [] ((::EnergySmearing*)p);
   }
   static void destruct_EnergySmearing(void *p) {
      typedef ::EnergySmearing current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::EnergySmearing

//______________________________________________________________________________
void MomentumSmearing::Streamer(TBuffer &R__b)
{
   // Stream an object of class MomentumSmearing.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(MomentumSmearing::Class(),this);
   } else {
      R__b.WriteClassBuffer(MomentumSmearing::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_MomentumSmearing(void *p) {
      return  p ? new(p) ::MomentumSmearing : new ::MomentumSmearing;
   }
   static void *newArray_MomentumSmearing(Long_t nElements, void *p) {
      return p ? new(p) ::MomentumSmearing[nElements] : new ::MomentumSmearing[nElements];
   }
   // Wrapper around operator delete
   static void delete_MomentumSmearing(void *p) {
      delete ((::MomentumSmearing*)p);
   }
   static void deleteArray_MomentumSmearing(void *p) {
      delete [] ((::MomentumSmearing*)p);
   }
   static void destruct_MomentumSmearing(void *p) {
      typedef ::MomentumSmearing current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::MomentumSmearing

//______________________________________________________________________________
void TrackSmearing::Streamer(TBuffer &R__b)
{
   // Stream an object of class TrackSmearing.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(TrackSmearing::Class(),this);
   } else {
      R__b.WriteClassBuffer(TrackSmearing::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_TrackSmearing(void *p) {
      return  p ? new(p) ::TrackSmearing : new ::TrackSmearing;
   }
   static void *newArray_TrackSmearing(Long_t nElements, void *p) {
      return p ? new(p) ::TrackSmearing[nElements] : new ::TrackSmearing[nElements];
   }
   // Wrapper around operator delete
   static void delete_TrackSmearing(void *p) {
      delete ((::TrackSmearing*)p);
   }
   static void deleteArray_TrackSmearing(void *p) {
      delete [] ((::TrackSmearing*)p);
   }
   static void destruct_TrackSmearing(void *p) {
      typedef ::TrackSmearing current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::TrackSmearing

//______________________________________________________________________________
void TrackCovariance::Streamer(TBuffer &R__b)
{
   // Stream an object of class TrackCovariance.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(TrackCovariance::Class(),this);
   } else {
      R__b.WriteClassBuffer(TrackCovariance::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_TrackCovariance(void *p) {
      return  p ? new(p) ::TrackCovariance : new ::TrackCovariance;
   }
   static void *newArray_TrackCovariance(Long_t nElements, void *p) {
      return p ? new(p) ::TrackCovariance[nElements] : new ::TrackCovariance[nElements];
   }
   // Wrapper around operator delete
   static void delete_TrackCovariance(void *p) {
      delete ((::TrackCovariance*)p);
   }
   static void deleteArray_TrackCovariance(void *p) {
      delete [] ((::TrackCovariance*)p);
   }
   static void destruct_TrackCovariance(void *p) {
      typedef ::TrackCovariance current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::TrackCovariance

//______________________________________________________________________________
void ClusterCounting::Streamer(TBuffer &R__b)
{
   // Stream an object of class ClusterCounting.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(ClusterCounting::Class(),this);
   } else {
      R__b.WriteClassBuffer(ClusterCounting::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_ClusterCounting(void *p) {
      return  p ? new(p) ::ClusterCounting : new ::ClusterCounting;
   }
   static void *newArray_ClusterCounting(Long_t nElements, void *p) {
      return p ? new(p) ::ClusterCounting[nElements] : new ::ClusterCounting[nElements];
   }
   // Wrapper around operator delete
   static void delete_ClusterCounting(void *p) {
      delete ((::ClusterCounting*)p);
   }
   static void deleteArray_ClusterCounting(void *p) {
      delete [] ((::ClusterCounting*)p);
   }
   static void destruct_ClusterCounting(void *p) {
      typedef ::ClusterCounting current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::ClusterCounting

//______________________________________________________________________________
void ImpactParameterSmearing::Streamer(TBuffer &R__b)
{
   // Stream an object of class ImpactParameterSmearing.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(ImpactParameterSmearing::Class(),this);
   } else {
      R__b.WriteClassBuffer(ImpactParameterSmearing::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_ImpactParameterSmearing(void *p) {
      return  p ? new(p) ::ImpactParameterSmearing : new ::ImpactParameterSmearing;
   }
   static void *newArray_ImpactParameterSmearing(Long_t nElements, void *p) {
      return p ? new(p) ::ImpactParameterSmearing[nElements] : new ::ImpactParameterSmearing[nElements];
   }
   // Wrapper around operator delete
   static void delete_ImpactParameterSmearing(void *p) {
      delete ((::ImpactParameterSmearing*)p);
   }
   static void deleteArray_ImpactParameterSmearing(void *p) {
      delete [] ((::ImpactParameterSmearing*)p);
   }
   static void destruct_ImpactParameterSmearing(void *p) {
      typedef ::ImpactParameterSmearing current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::ImpactParameterSmearing

//______________________________________________________________________________
void TimeSmearing::Streamer(TBuffer &R__b)
{
   // Stream an object of class TimeSmearing.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(TimeSmearing::Class(),this);
   } else {
      R__b.WriteClassBuffer(TimeSmearing::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_TimeSmearing(void *p) {
      return  p ? new(p) ::TimeSmearing : new ::TimeSmearing;
   }
   static void *newArray_TimeSmearing(Long_t nElements, void *p) {
      return p ? new(p) ::TimeSmearing[nElements] : new ::TimeSmearing[nElements];
   }
   // Wrapper around operator delete
   static void delete_TimeSmearing(void *p) {
      delete ((::TimeSmearing*)p);
   }
   static void deleteArray_TimeSmearing(void *p) {
      delete [] ((::TimeSmearing*)p);
   }
   static void destruct_TimeSmearing(void *p) {
      typedef ::TimeSmearing current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::TimeSmearing

//______________________________________________________________________________
void TimeOfFlight::Streamer(TBuffer &R__b)
{
   // Stream an object of class TimeOfFlight.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(TimeOfFlight::Class(),this);
   } else {
      R__b.WriteClassBuffer(TimeOfFlight::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_TimeOfFlight(void *p) {
      return  p ? new(p) ::TimeOfFlight : new ::TimeOfFlight;
   }
   static void *newArray_TimeOfFlight(Long_t nElements, void *p) {
      return p ? new(p) ::TimeOfFlight[nElements] : new ::TimeOfFlight[nElements];
   }
   // Wrapper around operator delete
   static void delete_TimeOfFlight(void *p) {
      delete ((::TimeOfFlight*)p);
   }
   static void deleteArray_TimeOfFlight(void *p) {
      delete [] ((::TimeOfFlight*)p);
   }
   static void destruct_TimeOfFlight(void *p) {
      typedef ::TimeOfFlight current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::TimeOfFlight

//______________________________________________________________________________
void SimpleCalorimeter::Streamer(TBuffer &R__b)
{
   // Stream an object of class SimpleCalorimeter.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(SimpleCalorimeter::Class(),this);
   } else {
      R__b.WriteClassBuffer(SimpleCalorimeter::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_SimpleCalorimeter(void *p) {
      return  p ? new(p) ::SimpleCalorimeter : new ::SimpleCalorimeter;
   }
   static void *newArray_SimpleCalorimeter(Long_t nElements, void *p) {
      return p ? new(p) ::SimpleCalorimeter[nElements] : new ::SimpleCalorimeter[nElements];
   }
   // Wrapper around operator delete
   static void delete_SimpleCalorimeter(void *p) {
      delete ((::SimpleCalorimeter*)p);
   }
   static void deleteArray_SimpleCalorimeter(void *p) {
      delete [] ((::SimpleCalorimeter*)p);
   }
   static void destruct_SimpleCalorimeter(void *p) {
      typedef ::SimpleCalorimeter current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::SimpleCalorimeter

//______________________________________________________________________________
void DenseTrackFilter::Streamer(TBuffer &R__b)
{
   // Stream an object of class DenseTrackFilter.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(DenseTrackFilter::Class(),this);
   } else {
      R__b.WriteClassBuffer(DenseTrackFilter::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_DenseTrackFilter(void *p) {
      return  p ? new(p) ::DenseTrackFilter : new ::DenseTrackFilter;
   }
   static void *newArray_DenseTrackFilter(Long_t nElements, void *p) {
      return p ? new(p) ::DenseTrackFilter[nElements] : new ::DenseTrackFilter[nElements];
   }
   // Wrapper around operator delete
   static void delete_DenseTrackFilter(void *p) {
      delete ((::DenseTrackFilter*)p);
   }
   static void deleteArray_DenseTrackFilter(void *p) {
      delete [] ((::DenseTrackFilter*)p);
   }
   static void destruct_DenseTrackFilter(void *p) {
      typedef ::DenseTrackFilter current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::DenseTrackFilter

//______________________________________________________________________________
void Calorimeter::Streamer(TBuffer &R__b)
{
   // Stream an object of class Calorimeter.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(Calorimeter::Class(),this);
   } else {
      R__b.WriteClassBuffer(Calorimeter::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_Calorimeter(void *p) {
      return  p ? new(p) ::Calorimeter : new ::Calorimeter;
   }
   static void *newArray_Calorimeter(Long_t nElements, void *p) {
      return p ? new(p) ::Calorimeter[nElements] : new ::Calorimeter[nElements];
   }
   // Wrapper around operator delete
   static void delete_Calorimeter(void *p) {
      delete ((::Calorimeter*)p);
   }
   static void deleteArray_Calorimeter(void *p) {
      delete [] ((::Calorimeter*)p);
   }
   static void destruct_Calorimeter(void *p) {
      typedef ::Calorimeter current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::Calorimeter

//______________________________________________________________________________
void DualReadoutCalorimeter::Streamer(TBuffer &R__b)
{
   // Stream an object of class DualReadoutCalorimeter.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(DualReadoutCalorimeter::Class(),this);
   } else {
      R__b.WriteClassBuffer(DualReadoutCalorimeter::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_DualReadoutCalorimeter(void *p) {
      return  p ? new(p) ::DualReadoutCalorimeter : new ::DualReadoutCalorimeter;
   }
   static void *newArray_DualReadoutCalorimeter(Long_t nElements, void *p) {
      return p ? new(p) ::DualReadoutCalorimeter[nElements] : new ::DualReadoutCalorimeter[nElements];
   }
   // Wrapper around operator delete
   static void delete_DualReadoutCalorimeter(void *p) {
      delete ((::DualReadoutCalorimeter*)p);
   }
   static void deleteArray_DualReadoutCalorimeter(void *p) {
      delete [] ((::DualReadoutCalorimeter*)p);
   }
   static void destruct_DualReadoutCalorimeter(void *p) {
      typedef ::DualReadoutCalorimeter current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::DualReadoutCalorimeter

//______________________________________________________________________________
void OldCalorimeter::Streamer(TBuffer &R__b)
{
   // Stream an object of class OldCalorimeter.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(OldCalorimeter::Class(),this);
   } else {
      R__b.WriteClassBuffer(OldCalorimeter::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_OldCalorimeter(void *p) {
      return  p ? new(p) ::OldCalorimeter : new ::OldCalorimeter;
   }
   static void *newArray_OldCalorimeter(Long_t nElements, void *p) {
      return p ? new(p) ::OldCalorimeter[nElements] : new ::OldCalorimeter[nElements];
   }
   // Wrapper around operator delete
   static void delete_OldCalorimeter(void *p) {
      delete ((::OldCalorimeter*)p);
   }
   static void deleteArray_OldCalorimeter(void *p) {
      delete [] ((::OldCalorimeter*)p);
   }
   static void destruct_OldCalorimeter(void *p) {
      typedef ::OldCalorimeter current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::OldCalorimeter

//______________________________________________________________________________
void Isolation::Streamer(TBuffer &R__b)
{
   // Stream an object of class Isolation.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(Isolation::Class(),this);
   } else {
      R__b.WriteClassBuffer(Isolation::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_Isolation(void *p) {
      return  p ? new(p) ::Isolation : new ::Isolation;
   }
   static void *newArray_Isolation(Long_t nElements, void *p) {
      return p ? new(p) ::Isolation[nElements] : new ::Isolation[nElements];
   }
   // Wrapper around operator delete
   static void delete_Isolation(void *p) {
      delete ((::Isolation*)p);
   }
   static void deleteArray_Isolation(void *p) {
      delete [] ((::Isolation*)p);
   }
   static void destruct_Isolation(void *p) {
      typedef ::Isolation current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::Isolation

//______________________________________________________________________________
void EnergyScale::Streamer(TBuffer &R__b)
{
   // Stream an object of class EnergyScale.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(EnergyScale::Class(),this);
   } else {
      R__b.WriteClassBuffer(EnergyScale::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_EnergyScale(void *p) {
      return  p ? new(p) ::EnergyScale : new ::EnergyScale;
   }
   static void *newArray_EnergyScale(Long_t nElements, void *p) {
      return p ? new(p) ::EnergyScale[nElements] : new ::EnergyScale[nElements];
   }
   // Wrapper around operator delete
   static void delete_EnergyScale(void *p) {
      delete ((::EnergyScale*)p);
   }
   static void deleteArray_EnergyScale(void *p) {
      delete [] ((::EnergyScale*)p);
   }
   static void destruct_EnergyScale(void *p) {
      typedef ::EnergyScale current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::EnergyScale

//______________________________________________________________________________
void UniqueObjectFinder::Streamer(TBuffer &R__b)
{
   // Stream an object of class UniqueObjectFinder.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(UniqueObjectFinder::Class(),this);
   } else {
      R__b.WriteClassBuffer(UniqueObjectFinder::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_UniqueObjectFinder(void *p) {
      return  p ? new(p) ::UniqueObjectFinder : new ::UniqueObjectFinder;
   }
   static void *newArray_UniqueObjectFinder(Long_t nElements, void *p) {
      return p ? new(p) ::UniqueObjectFinder[nElements] : new ::UniqueObjectFinder[nElements];
   }
   // Wrapper around operator delete
   static void delete_UniqueObjectFinder(void *p) {
      delete ((::UniqueObjectFinder*)p);
   }
   static void deleteArray_UniqueObjectFinder(void *p) {
      delete [] ((::UniqueObjectFinder*)p);
   }
   static void destruct_UniqueObjectFinder(void *p) {
      typedef ::UniqueObjectFinder current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::UniqueObjectFinder

//______________________________________________________________________________
void TrackCountingBTagging::Streamer(TBuffer &R__b)
{
   // Stream an object of class TrackCountingBTagging.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(TrackCountingBTagging::Class(),this);
   } else {
      R__b.WriteClassBuffer(TrackCountingBTagging::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_TrackCountingBTagging(void *p) {
      return  p ? new(p) ::TrackCountingBTagging : new ::TrackCountingBTagging;
   }
   static void *newArray_TrackCountingBTagging(Long_t nElements, void *p) {
      return p ? new(p) ::TrackCountingBTagging[nElements] : new ::TrackCountingBTagging[nElements];
   }
   // Wrapper around operator delete
   static void delete_TrackCountingBTagging(void *p) {
      delete ((::TrackCountingBTagging*)p);
   }
   static void deleteArray_TrackCountingBTagging(void *p) {
      delete [] ((::TrackCountingBTagging*)p);
   }
   static void destruct_TrackCountingBTagging(void *p) {
      typedef ::TrackCountingBTagging current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::TrackCountingBTagging

//______________________________________________________________________________
void BTagging::Streamer(TBuffer &R__b)
{
   // Stream an object of class BTagging.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(BTagging::Class(),this);
   } else {
      R__b.WriteClassBuffer(BTagging::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_BTagging(void *p) {
      return  p ? new(p) ::BTagging : new ::BTagging;
   }
   static void *newArray_BTagging(Long_t nElements, void *p) {
      return p ? new(p) ::BTagging[nElements] : new ::BTagging[nElements];
   }
   // Wrapper around operator delete
   static void delete_BTagging(void *p) {
      delete ((::BTagging*)p);
   }
   static void deleteArray_BTagging(void *p) {
      delete [] ((::BTagging*)p);
   }
   static void destruct_BTagging(void *p) {
      typedef ::BTagging current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::BTagging

//______________________________________________________________________________
void TauTagging::Streamer(TBuffer &R__b)
{
   // Stream an object of class TauTagging.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(TauTagging::Class(),this);
   } else {
      R__b.WriteClassBuffer(TauTagging::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_TauTagging(void *p) {
      return  p ? new(p) ::TauTagging : new ::TauTagging;
   }
   static void *newArray_TauTagging(Long_t nElements, void *p) {
      return p ? new(p) ::TauTagging[nElements] : new ::TauTagging[nElements];
   }
   // Wrapper around operator delete
   static void delete_TauTagging(void *p) {
      delete ((::TauTagging*)p);
   }
   static void deleteArray_TauTagging(void *p) {
      delete [] ((::TauTagging*)p);
   }
   static void destruct_TauTagging(void *p) {
      typedef ::TauTagging current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::TauTagging

//______________________________________________________________________________
void TrackCountingTauTagging::Streamer(TBuffer &R__b)
{
   // Stream an object of class TrackCountingTauTagging.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(TrackCountingTauTagging::Class(),this);
   } else {
      R__b.WriteClassBuffer(TrackCountingTauTagging::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_TrackCountingTauTagging(void *p) {
      return  p ? new(p) ::TrackCountingTauTagging : new ::TrackCountingTauTagging;
   }
   static void *newArray_TrackCountingTauTagging(Long_t nElements, void *p) {
      return p ? new(p) ::TrackCountingTauTagging[nElements] : new ::TrackCountingTauTagging[nElements];
   }
   // Wrapper around operator delete
   static void delete_TrackCountingTauTagging(void *p) {
      delete ((::TrackCountingTauTagging*)p);
   }
   static void deleteArray_TrackCountingTauTagging(void *p) {
      delete [] ((::TrackCountingTauTagging*)p);
   }
   static void destruct_TrackCountingTauTagging(void *p) {
      typedef ::TrackCountingTauTagging current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::TrackCountingTauTagging

//______________________________________________________________________________
void TreeWriter::Streamer(TBuffer &R__b)
{
   // Stream an object of class TreeWriter.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(TreeWriter::Class(),this);
   } else {
      R__b.WriteClassBuffer(TreeWriter::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_TreeWriter(void *p) {
      return  p ? new(p) ::TreeWriter : new ::TreeWriter;
   }
   static void *newArray_TreeWriter(Long_t nElements, void *p) {
      return p ? new(p) ::TreeWriter[nElements] : new ::TreeWriter[nElements];
   }
   // Wrapper around operator delete
   static void delete_TreeWriter(void *p) {
      delete ((::TreeWriter*)p);
   }
   static void deleteArray_TreeWriter(void *p) {
      delete [] ((::TreeWriter*)p);
   }
   static void destruct_TreeWriter(void *p) {
      typedef ::TreeWriter current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::TreeWriter

//______________________________________________________________________________
void Merger::Streamer(TBuffer &R__b)
{
   // Stream an object of class Merger.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(Merger::Class(),this);
   } else {
      R__b.WriteClassBuffer(Merger::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_Merger(void *p) {
      return  p ? new(p) ::Merger : new ::Merger;
   }
   static void *newArray_Merger(Long_t nElements, void *p) {
      return p ? new(p) ::Merger[nElements] : new ::Merger[nElements];
   }
   // Wrapper around operator delete
   static void delete_Merger(void *p) {
      delete ((::Merger*)p);
   }
   static void deleteArray_Merger(void *p) {
      delete [] ((::Merger*)p);
   }
   static void destruct_Merger(void *p) {
      typedef ::Merger current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::Merger

//______________________________________________________________________________
void LeptonDressing::Streamer(TBuffer &R__b)
{
   // Stream an object of class LeptonDressing.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(LeptonDressing::Class(),this);
   } else {
      R__b.WriteClassBuffer(LeptonDressing::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_LeptonDressing(void *p) {
      return  p ? new(p) ::LeptonDressing : new ::LeptonDressing;
   }
   static void *newArray_LeptonDressing(Long_t nElements, void *p) {
      return p ? new(p) ::LeptonDressing[nElements] : new ::LeptonDressing[nElements];
   }
   // Wrapper around operator delete
   static void delete_LeptonDressing(void *p) {
      delete ((::LeptonDressing*)p);
   }
   static void deleteArray_LeptonDressing(void *p) {
      delete [] ((::LeptonDressing*)p);
   }
   static void destruct_LeptonDressing(void *p) {
      typedef ::LeptonDressing current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::LeptonDressing

//______________________________________________________________________________
void PileUpMerger::Streamer(TBuffer &R__b)
{
   // Stream an object of class PileUpMerger.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(PileUpMerger::Class(),this);
   } else {
      R__b.WriteClassBuffer(PileUpMerger::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_PileUpMerger(void *p) {
      return  p ? new(p) ::PileUpMerger : new ::PileUpMerger;
   }
   static void *newArray_PileUpMerger(Long_t nElements, void *p) {
      return p ? new(p) ::PileUpMerger[nElements] : new ::PileUpMerger[nElements];
   }
   // Wrapper around operator delete
   static void delete_PileUpMerger(void *p) {
      delete ((::PileUpMerger*)p);
   }
   static void deleteArray_PileUpMerger(void *p) {
      delete [] ((::PileUpMerger*)p);
   }
   static void destruct_PileUpMerger(void *p) {
      typedef ::PileUpMerger current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::PileUpMerger

//______________________________________________________________________________
void JetPileUpSubtractor::Streamer(TBuffer &R__b)
{
   // Stream an object of class JetPileUpSubtractor.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(JetPileUpSubtractor::Class(),this);
   } else {
      R__b.WriteClassBuffer(JetPileUpSubtractor::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_JetPileUpSubtractor(void *p) {
      return  p ? new(p) ::JetPileUpSubtractor : new ::JetPileUpSubtractor;
   }
   static void *newArray_JetPileUpSubtractor(Long_t nElements, void *p) {
      return p ? new(p) ::JetPileUpSubtractor[nElements] : new ::JetPileUpSubtractor[nElements];
   }
   // Wrapper around operator delete
   static void delete_JetPileUpSubtractor(void *p) {
      delete ((::JetPileUpSubtractor*)p);
   }
   static void deleteArray_JetPileUpSubtractor(void *p) {
      delete [] ((::JetPileUpSubtractor*)p);
   }
   static void destruct_JetPileUpSubtractor(void *p) {
      typedef ::JetPileUpSubtractor current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::JetPileUpSubtractor

//______________________________________________________________________________
void TrackPileUpSubtractor::Streamer(TBuffer &R__b)
{
   // Stream an object of class TrackPileUpSubtractor.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(TrackPileUpSubtractor::Class(),this);
   } else {
      R__b.WriteClassBuffer(TrackPileUpSubtractor::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_TrackPileUpSubtractor(void *p) {
      return  p ? new(p) ::TrackPileUpSubtractor : new ::TrackPileUpSubtractor;
   }
   static void *newArray_TrackPileUpSubtractor(Long_t nElements, void *p) {
      return p ? new(p) ::TrackPileUpSubtractor[nElements] : new ::TrackPileUpSubtractor[nElements];
   }
   // Wrapper around operator delete
   static void delete_TrackPileUpSubtractor(void *p) {
      delete ((::TrackPileUpSubtractor*)p);
   }
   static void deleteArray_TrackPileUpSubtractor(void *p) {
      delete [] ((::TrackPileUpSubtractor*)p);
   }
   static void destruct_TrackPileUpSubtractor(void *p) {
      typedef ::TrackPileUpSubtractor current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::TrackPileUpSubtractor

//______________________________________________________________________________
void TaggingParticlesSkimmer::Streamer(TBuffer &R__b)
{
   // Stream an object of class TaggingParticlesSkimmer.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(TaggingParticlesSkimmer::Class(),this);
   } else {
      R__b.WriteClassBuffer(TaggingParticlesSkimmer::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_TaggingParticlesSkimmer(void *p) {
      return  p ? new(p) ::TaggingParticlesSkimmer : new ::TaggingParticlesSkimmer;
   }
   static void *newArray_TaggingParticlesSkimmer(Long_t nElements, void *p) {
      return p ? new(p) ::TaggingParticlesSkimmer[nElements] : new ::TaggingParticlesSkimmer[nElements];
   }
   // Wrapper around operator delete
   static void delete_TaggingParticlesSkimmer(void *p) {
      delete ((::TaggingParticlesSkimmer*)p);
   }
   static void deleteArray_TaggingParticlesSkimmer(void *p) {
      delete [] ((::TaggingParticlesSkimmer*)p);
   }
   static void destruct_TaggingParticlesSkimmer(void *p) {
      typedef ::TaggingParticlesSkimmer current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::TaggingParticlesSkimmer

//______________________________________________________________________________
void PileUpJetID::Streamer(TBuffer &R__b)
{
   // Stream an object of class PileUpJetID.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(PileUpJetID::Class(),this);
   } else {
      R__b.WriteClassBuffer(PileUpJetID::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_PileUpJetID(void *p) {
      return  p ? new(p) ::PileUpJetID : new ::PileUpJetID;
   }
   static void *newArray_PileUpJetID(Long_t nElements, void *p) {
      return p ? new(p) ::PileUpJetID[nElements] : new ::PileUpJetID[nElements];
   }
   // Wrapper around operator delete
   static void delete_PileUpJetID(void *p) {
      delete ((::PileUpJetID*)p);
   }
   static void deleteArray_PileUpJetID(void *p) {
      delete [] ((::PileUpJetID*)p);
   }
   static void destruct_PileUpJetID(void *p) {
      typedef ::PileUpJetID current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::PileUpJetID

//______________________________________________________________________________
void PhotonID::Streamer(TBuffer &R__b)
{
   // Stream an object of class PhotonID.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(PhotonID::Class(),this);
   } else {
      R__b.WriteClassBuffer(PhotonID::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_PhotonID(void *p) {
      return  p ? new(p) ::PhotonID : new ::PhotonID;
   }
   static void *newArray_PhotonID(Long_t nElements, void *p) {
      return p ? new(p) ::PhotonID[nElements] : new ::PhotonID[nElements];
   }
   // Wrapper around operator delete
   static void delete_PhotonID(void *p) {
      delete ((::PhotonID*)p);
   }
   static void deleteArray_PhotonID(void *p) {
      delete [] ((::PhotonID*)p);
   }
   static void destruct_PhotonID(void *p) {
      typedef ::PhotonID current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::PhotonID

//______________________________________________________________________________
void ConstituentFilter::Streamer(TBuffer &R__b)
{
   // Stream an object of class ConstituentFilter.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(ConstituentFilter::Class(),this);
   } else {
      R__b.WriteClassBuffer(ConstituentFilter::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_ConstituentFilter(void *p) {
      return  p ? new(p) ::ConstituentFilter : new ::ConstituentFilter;
   }
   static void *newArray_ConstituentFilter(Long_t nElements, void *p) {
      return p ? new(p) ::ConstituentFilter[nElements] : new ::ConstituentFilter[nElements];
   }
   // Wrapper around operator delete
   static void delete_ConstituentFilter(void *p) {
      delete ((::ConstituentFilter*)p);
   }
   static void deleteArray_ConstituentFilter(void *p) {
      delete [] ((::ConstituentFilter*)p);
   }
   static void destruct_ConstituentFilter(void *p) {
      typedef ::ConstituentFilter current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::ConstituentFilter

//______________________________________________________________________________
void StatusPidFilter::Streamer(TBuffer &R__b)
{
   // Stream an object of class StatusPidFilter.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(StatusPidFilter::Class(),this);
   } else {
      R__b.WriteClassBuffer(StatusPidFilter::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_StatusPidFilter(void *p) {
      return  p ? new(p) ::StatusPidFilter : new ::StatusPidFilter;
   }
   static void *newArray_StatusPidFilter(Long_t nElements, void *p) {
      return p ? new(p) ::StatusPidFilter[nElements] : new ::StatusPidFilter[nElements];
   }
   // Wrapper around operator delete
   static void delete_StatusPidFilter(void *p) {
      delete ((::StatusPidFilter*)p);
   }
   static void deleteArray_StatusPidFilter(void *p) {
      delete [] ((::StatusPidFilter*)p);
   }
   static void destruct_StatusPidFilter(void *p) {
      typedef ::StatusPidFilter current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::StatusPidFilter

//______________________________________________________________________________
void PdgCodeFilter::Streamer(TBuffer &R__b)
{
   // Stream an object of class PdgCodeFilter.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(PdgCodeFilter::Class(),this);
   } else {
      R__b.WriteClassBuffer(PdgCodeFilter::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_PdgCodeFilter(void *p) {
      return  p ? new(p) ::PdgCodeFilter : new ::PdgCodeFilter;
   }
   static void *newArray_PdgCodeFilter(Long_t nElements, void *p) {
      return p ? new(p) ::PdgCodeFilter[nElements] : new ::PdgCodeFilter[nElements];
   }
   // Wrapper around operator delete
   static void delete_PdgCodeFilter(void *p) {
      delete ((::PdgCodeFilter*)p);
   }
   static void deleteArray_PdgCodeFilter(void *p) {
      delete [] ((::PdgCodeFilter*)p);
   }
   static void destruct_PdgCodeFilter(void *p) {
      typedef ::PdgCodeFilter current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::PdgCodeFilter

//______________________________________________________________________________
void BeamSpotFilter::Streamer(TBuffer &R__b)
{
   // Stream an object of class BeamSpotFilter.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(BeamSpotFilter::Class(),this);
   } else {
      R__b.WriteClassBuffer(BeamSpotFilter::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_BeamSpotFilter(void *p) {
      return  p ? new(p) ::BeamSpotFilter : new ::BeamSpotFilter;
   }
   static void *newArray_BeamSpotFilter(Long_t nElements, void *p) {
      return p ? new(p) ::BeamSpotFilter[nElements] : new ::BeamSpotFilter[nElements];
   }
   // Wrapper around operator delete
   static void delete_BeamSpotFilter(void *p) {
      delete ((::BeamSpotFilter*)p);
   }
   static void deleteArray_BeamSpotFilter(void *p) {
      delete [] ((::BeamSpotFilter*)p);
   }
   static void destruct_BeamSpotFilter(void *p) {
      typedef ::BeamSpotFilter current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::BeamSpotFilter

//______________________________________________________________________________
void RecoPuFilter::Streamer(TBuffer &R__b)
{
   // Stream an object of class RecoPuFilter.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(RecoPuFilter::Class(),this);
   } else {
      R__b.WriteClassBuffer(RecoPuFilter::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_RecoPuFilter(void *p) {
      return  p ? new(p) ::RecoPuFilter : new ::RecoPuFilter;
   }
   static void *newArray_RecoPuFilter(Long_t nElements, void *p) {
      return p ? new(p) ::RecoPuFilter[nElements] : new ::RecoPuFilter[nElements];
   }
   // Wrapper around operator delete
   static void delete_RecoPuFilter(void *p) {
      delete ((::RecoPuFilter*)p);
   }
   static void deleteArray_RecoPuFilter(void *p) {
      delete [] ((::RecoPuFilter*)p);
   }
   static void destruct_RecoPuFilter(void *p) {
      typedef ::RecoPuFilter current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::RecoPuFilter

//______________________________________________________________________________
void Cloner::Streamer(TBuffer &R__b)
{
   // Stream an object of class Cloner.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(Cloner::Class(),this);
   } else {
      R__b.WriteClassBuffer(Cloner::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_Cloner(void *p) {
      return  p ? new(p) ::Cloner : new ::Cloner;
   }
   static void *newArray_Cloner(Long_t nElements, void *p) {
      return p ? new(p) ::Cloner[nElements] : new ::Cloner[nElements];
   }
   // Wrapper around operator delete
   static void delete_Cloner(void *p) {
      delete ((::Cloner*)p);
   }
   static void deleteArray_Cloner(void *p) {
      delete [] ((::Cloner*)p);
   }
   static void destruct_Cloner(void *p) {
      typedef ::Cloner current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::Cloner

//______________________________________________________________________________
void Weighter::Streamer(TBuffer &R__b)
{
   // Stream an object of class Weighter.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(Weighter::Class(),this);
   } else {
      R__b.WriteClassBuffer(Weighter::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_Weighter(void *p) {
      return  p ? new(p) ::Weighter : new ::Weighter;
   }
   static void *newArray_Weighter(Long_t nElements, void *p) {
      return p ? new(p) ::Weighter[nElements] : new ::Weighter[nElements];
   }
   // Wrapper around operator delete
   static void delete_Weighter(void *p) {
      delete ((::Weighter*)p);
   }
   static void deleteArray_Weighter(void *p) {
      delete [] ((::Weighter*)p);
   }
   static void destruct_Weighter(void *p) {
      typedef ::Weighter current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::Weighter

//______________________________________________________________________________
void Hector::Streamer(TBuffer &R__b)
{
   // Stream an object of class Hector.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(Hector::Class(),this);
   } else {
      R__b.WriteClassBuffer(Hector::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_Hector(void *p) {
      return  p ? new(p) ::Hector : new ::Hector;
   }
   static void *newArray_Hector(Long_t nElements, void *p) {
      return p ? new(p) ::Hector[nElements] : new ::Hector[nElements];
   }
   // Wrapper around operator delete
   static void delete_Hector(void *p) {
      delete ((::Hector*)p);
   }
   static void deleteArray_Hector(void *p) {
      delete [] ((::Hector*)p);
   }
   static void destruct_Hector(void *p) {
      typedef ::Hector current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::Hector

//______________________________________________________________________________
void JetFlavorAssociation::Streamer(TBuffer &R__b)
{
   // Stream an object of class JetFlavorAssociation.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(JetFlavorAssociation::Class(),this);
   } else {
      R__b.WriteClassBuffer(JetFlavorAssociation::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_JetFlavorAssociation(void *p) {
      return  p ? new(p) ::JetFlavorAssociation : new ::JetFlavorAssociation;
   }
   static void *newArray_JetFlavorAssociation(Long_t nElements, void *p) {
      return p ? new(p) ::JetFlavorAssociation[nElements] : new ::JetFlavorAssociation[nElements];
   }
   // Wrapper around operator delete
   static void delete_JetFlavorAssociation(void *p) {
      delete ((::JetFlavorAssociation*)p);
   }
   static void deleteArray_JetFlavorAssociation(void *p) {
      delete [] ((::JetFlavorAssociation*)p);
   }
   static void destruct_JetFlavorAssociation(void *p) {
      typedef ::JetFlavorAssociation current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::JetFlavorAssociation

//______________________________________________________________________________
void JetFakeParticle::Streamer(TBuffer &R__b)
{
   // Stream an object of class JetFakeParticle.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(JetFakeParticle::Class(),this);
   } else {
      R__b.WriteClassBuffer(JetFakeParticle::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_JetFakeParticle(void *p) {
      return  p ? new(p) ::JetFakeParticle : new ::JetFakeParticle;
   }
   static void *newArray_JetFakeParticle(Long_t nElements, void *p) {
      return p ? new(p) ::JetFakeParticle[nElements] : new ::JetFakeParticle[nElements];
   }
   // Wrapper around operator delete
   static void delete_JetFakeParticle(void *p) {
      delete ((::JetFakeParticle*)p);
   }
   static void deleteArray_JetFakeParticle(void *p) {
      delete [] ((::JetFakeParticle*)p);
   }
   static void destruct_JetFakeParticle(void *p) {
      typedef ::JetFakeParticle current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::JetFakeParticle

//______________________________________________________________________________
void VertexSorter::Streamer(TBuffer &R__b)
{
   // Stream an object of class VertexSorter.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(VertexSorter::Class(),this);
   } else {
      R__b.WriteClassBuffer(VertexSorter::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_VertexSorter(void *p) {
      return  p ? new(p) ::VertexSorter : new ::VertexSorter;
   }
   static void *newArray_VertexSorter(Long_t nElements, void *p) {
      return p ? new(p) ::VertexSorter[nElements] : new ::VertexSorter[nElements];
   }
   // Wrapper around operator delete
   static void delete_VertexSorter(void *p) {
      delete ((::VertexSorter*)p);
   }
   static void deleteArray_VertexSorter(void *p) {
      delete [] ((::VertexSorter*)p);
   }
   static void destruct_VertexSorter(void *p) {
      typedef ::VertexSorter current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::VertexSorter

//______________________________________________________________________________
void VertexFinder::Streamer(TBuffer &R__b)
{
   // Stream an object of class VertexFinder.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(VertexFinder::Class(),this);
   } else {
      R__b.WriteClassBuffer(VertexFinder::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_VertexFinder(void *p) {
      return  p ? new(p) ::VertexFinder : new ::VertexFinder;
   }
   static void *newArray_VertexFinder(Long_t nElements, void *p) {
      return p ? new(p) ::VertexFinder[nElements] : new ::VertexFinder[nElements];
   }
   // Wrapper around operator delete
   static void delete_VertexFinder(void *p) {
      delete ((::VertexFinder*)p);
   }
   static void deleteArray_VertexFinder(void *p) {
      delete [] ((::VertexFinder*)p);
   }
   static void destruct_VertexFinder(void *p) {
      typedef ::VertexFinder current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::VertexFinder

//______________________________________________________________________________
void VertexFinderDA4D::Streamer(TBuffer &R__b)
{
   // Stream an object of class VertexFinderDA4D.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(VertexFinderDA4D::Class(),this);
   } else {
      R__b.WriteClassBuffer(VertexFinderDA4D::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_VertexFinderDA4D(void *p) {
      return  p ? new(p) ::VertexFinderDA4D : new ::VertexFinderDA4D;
   }
   static void *newArray_VertexFinderDA4D(Long_t nElements, void *p) {
      return p ? new(p) ::VertexFinderDA4D[nElements] : new ::VertexFinderDA4D[nElements];
   }
   // Wrapper around operator delete
   static void delete_VertexFinderDA4D(void *p) {
      delete ((::VertexFinderDA4D*)p);
   }
   static void deleteArray_VertexFinderDA4D(void *p) {
      delete [] ((::VertexFinderDA4D*)p);
   }
   static void destruct_VertexFinderDA4D(void *p) {
      typedef ::VertexFinderDA4D current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::VertexFinderDA4D

//______________________________________________________________________________
void DecayFilter::Streamer(TBuffer &R__b)
{
   // Stream an object of class DecayFilter.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(DecayFilter::Class(),this);
   } else {
      R__b.WriteClassBuffer(DecayFilter::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_DecayFilter(void *p) {
      return  p ? new(p) ::DecayFilter : new ::DecayFilter;
   }
   static void *newArray_DecayFilter(Long_t nElements, void *p) {
      return p ? new(p) ::DecayFilter[nElements] : new ::DecayFilter[nElements];
   }
   // Wrapper around operator delete
   static void delete_DecayFilter(void *p) {
      delete ((::DecayFilter*)p);
   }
   static void deleteArray_DecayFilter(void *p) {
      delete [] ((::DecayFilter*)p);
   }
   static void destruct_DecayFilter(void *p) {
      typedef ::DecayFilter current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::DecayFilter

//______________________________________________________________________________
void ParticleDensity::Streamer(TBuffer &R__b)
{
   // Stream an object of class ParticleDensity.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(ParticleDensity::Class(),this);
   } else {
      R__b.WriteClassBuffer(ParticleDensity::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_ParticleDensity(void *p) {
      return  p ? new(p) ::ParticleDensity : new ::ParticleDensity;
   }
   static void *newArray_ParticleDensity(Long_t nElements, void *p) {
      return p ? new(p) ::ParticleDensity[nElements] : new ::ParticleDensity[nElements];
   }
   // Wrapper around operator delete
   static void delete_ParticleDensity(void *p) {
      delete ((::ParticleDensity*)p);
   }
   static void deleteArray_ParticleDensity(void *p) {
      delete [] ((::ParticleDensity*)p);
   }
   static void destruct_ParticleDensity(void *p) {
      typedef ::ParticleDensity current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::ParticleDensity

//______________________________________________________________________________
void TruthVertexFinder::Streamer(TBuffer &R__b)
{
   // Stream an object of class TruthVertexFinder.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(TruthVertexFinder::Class(),this);
   } else {
      R__b.WriteClassBuffer(TruthVertexFinder::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_TruthVertexFinder(void *p) {
      return  p ? new(p) ::TruthVertexFinder : new ::TruthVertexFinder;
   }
   static void *newArray_TruthVertexFinder(Long_t nElements, void *p) {
      return p ? new(p) ::TruthVertexFinder[nElements] : new ::TruthVertexFinder[nElements];
   }
   // Wrapper around operator delete
   static void delete_TruthVertexFinder(void *p) {
      delete ((::TruthVertexFinder*)p);
   }
   static void deleteArray_TruthVertexFinder(void *p) {
      delete [] ((::TruthVertexFinder*)p);
   }
   static void destruct_TruthVertexFinder(void *p) {
      typedef ::TruthVertexFinder current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::TruthVertexFinder

//______________________________________________________________________________
void ExampleModule::Streamer(TBuffer &R__b)
{
   // Stream an object of class ExampleModule.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(ExampleModule::Class(),this);
   } else {
      R__b.WriteClassBuffer(ExampleModule::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_ExampleModule(void *p) {
      return  p ? new(p) ::ExampleModule : new ::ExampleModule;
   }
   static void *newArray_ExampleModule(Long_t nElements, void *p) {
      return p ? new(p) ::ExampleModule[nElements] : new ::ExampleModule[nElements];
   }
   // Wrapper around operator delete
   static void delete_ExampleModule(void *p) {
      delete ((::ExampleModule*)p);
   }
   static void deleteArray_ExampleModule(void *p) {
      delete [] ((::ExampleModule*)p);
   }
   static void destruct_ExampleModule(void *p) {
      typedef ::ExampleModule current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::ExampleModule

namespace ROOT {
   static TClass *vectorlEvectorlEdoublegRmUgR_Dictionary();
   static void vectorlEvectorlEdoublegRmUgR_TClassManip(TClass*);
   static void *new_vectorlEvectorlEdoublegRmUgR(void *p = 0);
   static void *newArray_vectorlEvectorlEdoublegRmUgR(Long_t size, void *p);
   static void delete_vectorlEvectorlEdoublegRmUgR(void *p);
   static void deleteArray_vectorlEvectorlEdoublegRmUgR(void *p);
   static void destruct_vectorlEvectorlEdoublegRmUgR(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const vector<vector<double>*>*)
   {
      vector<vector<double>*> *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(vector<vector<double>*>));
      static ::ROOT::TGenericClassInfo 
         instance("vector<vector<double>*>", -2, "vector", 216,
                  typeid(vector<vector<double>*>), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &vectorlEvectorlEdoublegRmUgR_Dictionary, isa_proxy, 0,
                  sizeof(vector<vector<double>*>) );
      instance.SetNew(&new_vectorlEvectorlEdoublegRmUgR);
      instance.SetNewArray(&newArray_vectorlEvectorlEdoublegRmUgR);
      instance.SetDelete(&delete_vectorlEvectorlEdoublegRmUgR);
      instance.SetDeleteArray(&deleteArray_vectorlEvectorlEdoublegRmUgR);
      instance.SetDestructor(&destruct_vectorlEvectorlEdoublegRmUgR);
      instance.AdoptCollectionProxyInfo(TCollectionProxyInfo::Generate(TCollectionProxyInfo::Pushback< vector<vector<double>*> >()));
      return &instance;
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const vector<vector<double>*>*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *vectorlEvectorlEdoublegRmUgR_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const vector<vector<double>*>*)0x0)->GetClass();
      vectorlEvectorlEdoublegRmUgR_TClassManip(theClass);
   return theClass;
   }

   static void vectorlEvectorlEdoublegRmUgR_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   // Wrappers around operator new
   static void *new_vectorlEvectorlEdoublegRmUgR(void *p) {
      return  p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) vector<vector<double>*> : new vector<vector<double>*>;
   }
   static void *newArray_vectorlEvectorlEdoublegRmUgR(Long_t nElements, void *p) {
      return p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) vector<vector<double>*>[nElements] : new vector<vector<double>*>[nElements];
   }
   // Wrapper around operator delete
   static void delete_vectorlEvectorlEdoublegRmUgR(void *p) {
      delete ((vector<vector<double>*>*)p);
   }
   static void deleteArray_vectorlEvectorlEdoublegRmUgR(void *p) {
      delete [] ((vector<vector<double>*>*)p);
   }
   static void destruct_vectorlEvectorlEdoublegRmUgR(void *p) {
      typedef vector<vector<double>*> current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class vector<vector<double>*>

namespace ROOT {
   static TClass *vectorlEpairlEunsignedsPintcOdoublegRsPgR_Dictionary();
   static void vectorlEpairlEunsignedsPintcOdoublegRsPgR_TClassManip(TClass*);
   static void *new_vectorlEpairlEunsignedsPintcOdoublegRsPgR(void *p = 0);
   static void *newArray_vectorlEpairlEunsignedsPintcOdoublegRsPgR(Long_t size, void *p);
   static void delete_vectorlEpairlEunsignedsPintcOdoublegRsPgR(void *p);
   static void deleteArray_vectorlEpairlEunsignedsPintcOdoublegRsPgR(void *p);
   static void destruct_vectorlEpairlEunsignedsPintcOdoublegRsPgR(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const vector<pair<unsigned int,double> >*)
   {
      vector<pair<unsigned int,double> > *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(vector<pair<unsigned int,double> >));
      static ::ROOT::TGenericClassInfo 
         instance("vector<pair<unsigned int,double> >", -2, "vector", 216,
                  typeid(vector<pair<unsigned int,double> >), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &vectorlEpairlEunsignedsPintcOdoublegRsPgR_Dictionary, isa_proxy, 0,
                  sizeof(vector<pair<unsigned int,double> >) );
      instance.SetNew(&new_vectorlEpairlEunsignedsPintcOdoublegRsPgR);
      instance.SetNewArray(&newArray_vectorlEpairlEunsignedsPintcOdoublegRsPgR);
      instance.SetDelete(&delete_vectorlEpairlEunsignedsPintcOdoublegRsPgR);
      instance.SetDeleteArray(&deleteArray_vectorlEpairlEunsignedsPintcOdoublegRsPgR);
      instance.SetDestructor(&destruct_vectorlEpairlEunsignedsPintcOdoublegRsPgR);
      instance.AdoptCollectionProxyInfo(TCollectionProxyInfo::Generate(TCollectionProxyInfo::Pushback< vector<pair<unsigned int,double> > >()));
      return &instance;
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const vector<pair<unsigned int,double> >*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *vectorlEpairlEunsignedsPintcOdoublegRsPgR_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const vector<pair<unsigned int,double> >*)0x0)->GetClass();
      vectorlEpairlEunsignedsPintcOdoublegRsPgR_TClassManip(theClass);
   return theClass;
   }

   static void vectorlEpairlEunsignedsPintcOdoublegRsPgR_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   // Wrappers around operator new
   static void *new_vectorlEpairlEunsignedsPintcOdoublegRsPgR(void *p) {
      return  p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) vector<pair<unsigned int,double> > : new vector<pair<unsigned int,double> >;
   }
   static void *newArray_vectorlEpairlEunsignedsPintcOdoublegRsPgR(Long_t nElements, void *p) {
      return p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) vector<pair<unsigned int,double> >[nElements] : new vector<pair<unsigned int,double> >[nElements];
   }
   // Wrapper around operator delete
   static void delete_vectorlEpairlEunsignedsPintcOdoublegRsPgR(void *p) {
      delete ((vector<pair<unsigned int,double> >*)p);
   }
   static void deleteArray_vectorlEpairlEunsignedsPintcOdoublegRsPgR(void *p) {
      delete [] ((vector<pair<unsigned int,double> >*)p);
   }
   static void destruct_vectorlEpairlEunsignedsPintcOdoublegRsPgR(void *p) {
      typedef vector<pair<unsigned int,double> > current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class vector<pair<unsigned int,double> >

namespace ROOT {
   static TClass *vectorlEintgR_Dictionary();
   static void vectorlEintgR_TClassManip(TClass*);
   static void *new_vectorlEintgR(void *p = 0);
   static void *newArray_vectorlEintgR(Long_t size, void *p);
   static void delete_vectorlEintgR(void *p);
   static void deleteArray_vectorlEintgR(void *p);
   static void destruct_vectorlEintgR(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const vector<int>*)
   {
      vector<int> *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(vector<int>));
      static ::ROOT::TGenericClassInfo 
         instance("vector<int>", -2, "vector", 216,
                  typeid(vector<int>), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &vectorlEintgR_Dictionary, isa_proxy, 0,
                  sizeof(vector<int>) );
      instance.SetNew(&new_vectorlEintgR);
      instance.SetNewArray(&newArray_vectorlEintgR);
      instance.SetDelete(&delete_vectorlEintgR);
      instance.SetDeleteArray(&deleteArray_vectorlEintgR);
      instance.SetDestructor(&destruct_vectorlEintgR);
      instance.AdoptCollectionProxyInfo(TCollectionProxyInfo::Generate(TCollectionProxyInfo::Pushback< vector<int> >()));
      return &instance;
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const vector<int>*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *vectorlEintgR_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const vector<int>*)0x0)->GetClass();
      vectorlEintgR_TClassManip(theClass);
   return theClass;
   }

   static void vectorlEintgR_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   // Wrappers around operator new
   static void *new_vectorlEintgR(void *p) {
      return  p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) vector<int> : new vector<int>;
   }
   static void *newArray_vectorlEintgR(Long_t nElements, void *p) {
      return p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) vector<int>[nElements] : new vector<int>[nElements];
   }
   // Wrapper around operator delete
   static void delete_vectorlEintgR(void *p) {
      delete ((vector<int>*)p);
   }
   static void deleteArray_vectorlEintgR(void *p) {
      delete [] ((vector<int>*)p);
   }
   static void destruct_vectorlEintgR(void *p) {
      typedef vector<int> current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class vector<int>

namespace ROOT {
   static TClass *vectorlEdoublegR_Dictionary();
   static void vectorlEdoublegR_TClassManip(TClass*);
   static void *new_vectorlEdoublegR(void *p = 0);
   static void *newArray_vectorlEdoublegR(Long_t size, void *p);
   static void delete_vectorlEdoublegR(void *p);
   static void deleteArray_vectorlEdoublegR(void *p);
   static void destruct_vectorlEdoublegR(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const vector<double>*)
   {
      vector<double> *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(vector<double>));
      static ::ROOT::TGenericClassInfo 
         instance("vector<double>", -2, "vector", 216,
                  typeid(vector<double>), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &vectorlEdoublegR_Dictionary, isa_proxy, 0,
                  sizeof(vector<double>) );
      instance.SetNew(&new_vectorlEdoublegR);
      instance.SetNewArray(&newArray_vectorlEdoublegR);
      instance.SetDelete(&delete_vectorlEdoublegR);
      instance.SetDeleteArray(&deleteArray_vectorlEdoublegR);
      instance.SetDestructor(&destruct_vectorlEdoublegR);
      instance.AdoptCollectionProxyInfo(TCollectionProxyInfo::Generate(TCollectionProxyInfo::Pushback< vector<double> >()));
      return &instance;
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const vector<double>*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *vectorlEdoublegR_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const vector<double>*)0x0)->GetClass();
      vectorlEdoublegR_TClassManip(theClass);
   return theClass;
   }

   static void vectorlEdoublegR_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   // Wrappers around operator new
   static void *new_vectorlEdoublegR(void *p) {
      return  p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) vector<double> : new vector<double>;
   }
   static void *newArray_vectorlEdoublegR(Long_t nElements, void *p) {
      return p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) vector<double>[nElements] : new vector<double>[nElements];
   }
   // Wrapper around operator delete
   static void delete_vectorlEdoublegR(void *p) {
      delete ((vector<double>*)p);
   }
   static void deleteArray_vectorlEdoublegR(void *p) {
      delete [] ((vector<double>*)p);
   }
   static void destruct_vectorlEdoublegR(void *p) {
      typedef vector<double> current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class vector<double>

namespace ROOT {
   static TClass *vectorlELong64_tgR_Dictionary();
   static void vectorlELong64_tgR_TClassManip(TClass*);
   static void *new_vectorlELong64_tgR(void *p = 0);
   static void *newArray_vectorlELong64_tgR(Long_t size, void *p);
   static void delete_vectorlELong64_tgR(void *p);
   static void deleteArray_vectorlELong64_tgR(void *p);
   static void destruct_vectorlELong64_tgR(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const vector<Long64_t>*)
   {
      vector<Long64_t> *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(vector<Long64_t>));
      static ::ROOT::TGenericClassInfo 
         instance("vector<Long64_t>", -2, "vector", 216,
                  typeid(vector<Long64_t>), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &vectorlELong64_tgR_Dictionary, isa_proxy, 0,
                  sizeof(vector<Long64_t>) );
      instance.SetNew(&new_vectorlELong64_tgR);
      instance.SetNewArray(&newArray_vectorlELong64_tgR);
      instance.SetDelete(&delete_vectorlELong64_tgR);
      instance.SetDeleteArray(&deleteArray_vectorlELong64_tgR);
      instance.SetDestructor(&destruct_vectorlELong64_tgR);
      instance.AdoptCollectionProxyInfo(TCollectionProxyInfo::Generate(TCollectionProxyInfo::Pushback< vector<Long64_t> >()));
      return &instance;
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const vector<Long64_t>*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *vectorlELong64_tgR_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const vector<Long64_t>*)0x0)->GetClass();
      vectorlELong64_tgR_TClassManip(theClass);
   return theClass;
   }

   static void vectorlELong64_tgR_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   // Wrappers around operator new
   static void *new_vectorlELong64_tgR(void *p) {
      return  p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) vector<Long64_t> : new vector<Long64_t>;
   }
   static void *newArray_vectorlELong64_tgR(Long_t nElements, void *p) {
      return p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) vector<Long64_t>[nElements] : new vector<Long64_t>[nElements];
   }
   // Wrapper around operator delete
   static void delete_vectorlELong64_tgR(void *p) {
      delete ((vector<Long64_t>*)p);
   }
   static void deleteArray_vectorlELong64_tgR(void *p) {
      delete [] ((vector<Long64_t>*)p);
   }
   static void destruct_vectorlELong64_tgR(void *p) {
      typedef vector<Long64_t> current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class vector<Long64_t>

namespace ROOT {
   static TClass *maplEunsignedsPintcOmaplEstringcOintgRsPgR_Dictionary();
   static void maplEunsignedsPintcOmaplEstringcOintgRsPgR_TClassManip(TClass*);
   static void *new_maplEunsignedsPintcOmaplEstringcOintgRsPgR(void *p = 0);
   static void *newArray_maplEunsignedsPintcOmaplEstringcOintgRsPgR(Long_t size, void *p);
   static void delete_maplEunsignedsPintcOmaplEstringcOintgRsPgR(void *p);
   static void deleteArray_maplEunsignedsPintcOmaplEstringcOintgRsPgR(void *p);
   static void destruct_maplEunsignedsPintcOmaplEstringcOintgRsPgR(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const map<unsigned int,map<string,int> >*)
   {
      map<unsigned int,map<string,int> > *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(map<unsigned int,map<string,int> >));
      static ::ROOT::TGenericClassInfo 
         instance("map<unsigned int,map<string,int> >", -2, "map", 99,
                  typeid(map<unsigned int,map<string,int> >), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &maplEunsignedsPintcOmaplEstringcOintgRsPgR_Dictionary, isa_proxy, 0,
                  sizeof(map<unsigned int,map<string,int> >) );
      instance.SetNew(&new_maplEunsignedsPintcOmaplEstringcOintgRsPgR);
      instance.SetNewArray(&newArray_maplEunsignedsPintcOmaplEstringcOintgRsPgR);
      instance.SetDelete(&delete_maplEunsignedsPintcOmaplEstringcOintgRsPgR);
      instance.SetDeleteArray(&deleteArray_maplEunsignedsPintcOmaplEstringcOintgRsPgR);
      instance.SetDestructor(&destruct_maplEunsignedsPintcOmaplEstringcOintgRsPgR);
      instance.AdoptCollectionProxyInfo(TCollectionProxyInfo::Generate(TCollectionProxyInfo::MapInsert< map<unsigned int,map<string,int> > >()));
      return &instance;
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const map<unsigned int,map<string,int> >*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *maplEunsignedsPintcOmaplEstringcOintgRsPgR_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const map<unsigned int,map<string,int> >*)0x0)->GetClass();
      maplEunsignedsPintcOmaplEstringcOintgRsPgR_TClassManip(theClass);
   return theClass;
   }

   static void maplEunsignedsPintcOmaplEstringcOintgRsPgR_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   // Wrappers around operator new
   static void *new_maplEunsignedsPintcOmaplEstringcOintgRsPgR(void *p) {
      return  p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) map<unsigned int,map<string,int> > : new map<unsigned int,map<string,int> >;
   }
   static void *newArray_maplEunsignedsPintcOmaplEstringcOintgRsPgR(Long_t nElements, void *p) {
      return p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) map<unsigned int,map<string,int> >[nElements] : new map<unsigned int,map<string,int> >[nElements];
   }
   // Wrapper around operator delete
   static void delete_maplEunsignedsPintcOmaplEstringcOintgRsPgR(void *p) {
      delete ((map<unsigned int,map<string,int> >*)p);
   }
   static void deleteArray_maplEunsignedsPintcOmaplEstringcOintgRsPgR(void *p) {
      delete [] ((map<unsigned int,map<string,int> >*)p);
   }
   static void destruct_maplEunsignedsPintcOmaplEstringcOintgRsPgR(void *p) {
      typedef map<unsigned int,map<string,int> > current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class map<unsigned int,map<string,int> >

namespace ROOT {
   static TClass *maplEunsignedsPintcOmaplEstringcOdoublegRsPgR_Dictionary();
   static void maplEunsignedsPintcOmaplEstringcOdoublegRsPgR_TClassManip(TClass*);
   static void *new_maplEunsignedsPintcOmaplEstringcOdoublegRsPgR(void *p = 0);
   static void *newArray_maplEunsignedsPintcOmaplEstringcOdoublegRsPgR(Long_t size, void *p);
   static void delete_maplEunsignedsPintcOmaplEstringcOdoublegRsPgR(void *p);
   static void deleteArray_maplEunsignedsPintcOmaplEstringcOdoublegRsPgR(void *p);
   static void destruct_maplEunsignedsPintcOmaplEstringcOdoublegRsPgR(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const map<unsigned int,map<string,double> >*)
   {
      map<unsigned int,map<string,double> > *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(map<unsigned int,map<string,double> >));
      static ::ROOT::TGenericClassInfo 
         instance("map<unsigned int,map<string,double> >", -2, "map", 99,
                  typeid(map<unsigned int,map<string,double> >), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &maplEunsignedsPintcOmaplEstringcOdoublegRsPgR_Dictionary, isa_proxy, 0,
                  sizeof(map<unsigned int,map<string,double> >) );
      instance.SetNew(&new_maplEunsignedsPintcOmaplEstringcOdoublegRsPgR);
      instance.SetNewArray(&newArray_maplEunsignedsPintcOmaplEstringcOdoublegRsPgR);
      instance.SetDelete(&delete_maplEunsignedsPintcOmaplEstringcOdoublegRsPgR);
      instance.SetDeleteArray(&deleteArray_maplEunsignedsPintcOmaplEstringcOdoublegRsPgR);
      instance.SetDestructor(&destruct_maplEunsignedsPintcOmaplEstringcOdoublegRsPgR);
      instance.AdoptCollectionProxyInfo(TCollectionProxyInfo::Generate(TCollectionProxyInfo::MapInsert< map<unsigned int,map<string,double> > >()));
      return &instance;
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const map<unsigned int,map<string,double> >*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *maplEunsignedsPintcOmaplEstringcOdoublegRsPgR_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const map<unsigned int,map<string,double> >*)0x0)->GetClass();
      maplEunsignedsPintcOmaplEstringcOdoublegRsPgR_TClassManip(theClass);
   return theClass;
   }

   static void maplEunsignedsPintcOmaplEstringcOdoublegRsPgR_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   // Wrappers around operator new
   static void *new_maplEunsignedsPintcOmaplEstringcOdoublegRsPgR(void *p) {
      return  p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) map<unsigned int,map<string,double> > : new map<unsigned int,map<string,double> >;
   }
   static void *newArray_maplEunsignedsPintcOmaplEstringcOdoublegRsPgR(Long_t nElements, void *p) {
      return p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) map<unsigned int,map<string,double> >[nElements] : new map<unsigned int,map<string,double> >[nElements];
   }
   // Wrapper around operator delete
   static void delete_maplEunsignedsPintcOmaplEstringcOdoublegRsPgR(void *p) {
      delete ((map<unsigned int,map<string,double> >*)p);
   }
   static void deleteArray_maplEunsignedsPintcOmaplEstringcOdoublegRsPgR(void *p) {
      delete [] ((map<unsigned int,map<string,double> >*)p);
   }
   static void destruct_maplEunsignedsPintcOmaplEstringcOdoublegRsPgR(void *p) {
      typedef map<unsigned int,map<string,double> > current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class map<unsigned int,map<string,double> >

namespace ROOT {
   static TClass *maplEunsignedsPintcOmaplEstringcOboolgRsPgR_Dictionary();
   static void maplEunsignedsPintcOmaplEstringcOboolgRsPgR_TClassManip(TClass*);
   static void *new_maplEunsignedsPintcOmaplEstringcOboolgRsPgR(void *p = 0);
   static void *newArray_maplEunsignedsPintcOmaplEstringcOboolgRsPgR(Long_t size, void *p);
   static void delete_maplEunsignedsPintcOmaplEstringcOboolgRsPgR(void *p);
   static void deleteArray_maplEunsignedsPintcOmaplEstringcOboolgRsPgR(void *p);
   static void destruct_maplEunsignedsPintcOmaplEstringcOboolgRsPgR(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const map<unsigned int,map<string,bool> >*)
   {
      map<unsigned int,map<string,bool> > *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(map<unsigned int,map<string,bool> >));
      static ::ROOT::TGenericClassInfo 
         instance("map<unsigned int,map<string,bool> >", -2, "map", 99,
                  typeid(map<unsigned int,map<string,bool> >), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &maplEunsignedsPintcOmaplEstringcOboolgRsPgR_Dictionary, isa_proxy, 0,
                  sizeof(map<unsigned int,map<string,bool> >) );
      instance.SetNew(&new_maplEunsignedsPintcOmaplEstringcOboolgRsPgR);
      instance.SetNewArray(&newArray_maplEunsignedsPintcOmaplEstringcOboolgRsPgR);
      instance.SetDelete(&delete_maplEunsignedsPintcOmaplEstringcOboolgRsPgR);
      instance.SetDeleteArray(&deleteArray_maplEunsignedsPintcOmaplEstringcOboolgRsPgR);
      instance.SetDestructor(&destruct_maplEunsignedsPintcOmaplEstringcOboolgRsPgR);
      instance.AdoptCollectionProxyInfo(TCollectionProxyInfo::Generate(TCollectionProxyInfo::MapInsert< map<unsigned int,map<string,bool> > >()));
      return &instance;
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const map<unsigned int,map<string,bool> >*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *maplEunsignedsPintcOmaplEstringcOboolgRsPgR_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const map<unsigned int,map<string,bool> >*)0x0)->GetClass();
      maplEunsignedsPintcOmaplEstringcOboolgRsPgR_TClassManip(theClass);
   return theClass;
   }

   static void maplEunsignedsPintcOmaplEstringcOboolgRsPgR_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   // Wrappers around operator new
   static void *new_maplEunsignedsPintcOmaplEstringcOboolgRsPgR(void *p) {
      return  p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) map<unsigned int,map<string,bool> > : new map<unsigned int,map<string,bool> >;
   }
   static void *newArray_maplEunsignedsPintcOmaplEstringcOboolgRsPgR(Long_t nElements, void *p) {
      return p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) map<unsigned int,map<string,bool> >[nElements] : new map<unsigned int,map<string,bool> >[nElements];
   }
   // Wrapper around operator delete
   static void delete_maplEunsignedsPintcOmaplEstringcOboolgRsPgR(void *p) {
      delete ((map<unsigned int,map<string,bool> >*)p);
   }
   static void deleteArray_maplEunsignedsPintcOmaplEstringcOboolgRsPgR(void *p) {
      delete [] ((map<unsigned int,map<string,bool> >*)p);
   }
   static void destruct_maplEunsignedsPintcOmaplEstringcOboolgRsPgR(void *p) {
      typedef map<unsigned int,map<string,bool> > current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class map<unsigned int,map<string,bool> >

namespace ROOT {
   static TClass *maplEstringcOintgR_Dictionary();
   static void maplEstringcOintgR_TClassManip(TClass*);
   static void *new_maplEstringcOintgR(void *p = 0);
   static void *newArray_maplEstringcOintgR(Long_t size, void *p);
   static void delete_maplEstringcOintgR(void *p);
   static void deleteArray_maplEstringcOintgR(void *p);
   static void destruct_maplEstringcOintgR(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const map<string,int>*)
   {
      map<string,int> *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(map<string,int>));
      static ::ROOT::TGenericClassInfo 
         instance("map<string,int>", -2, "map", 99,
                  typeid(map<string,int>), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &maplEstringcOintgR_Dictionary, isa_proxy, 0,
                  sizeof(map<string,int>) );
      instance.SetNew(&new_maplEstringcOintgR);
      instance.SetNewArray(&newArray_maplEstringcOintgR);
      instance.SetDelete(&delete_maplEstringcOintgR);
      instance.SetDeleteArray(&deleteArray_maplEstringcOintgR);
      instance.SetDestructor(&destruct_maplEstringcOintgR);
      instance.AdoptCollectionProxyInfo(TCollectionProxyInfo::Generate(TCollectionProxyInfo::MapInsert< map<string,int> >()));
      return &instance;
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const map<string,int>*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *maplEstringcOintgR_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const map<string,int>*)0x0)->GetClass();
      maplEstringcOintgR_TClassManip(theClass);
   return theClass;
   }

   static void maplEstringcOintgR_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   // Wrappers around operator new
   static void *new_maplEstringcOintgR(void *p) {
      return  p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) map<string,int> : new map<string,int>;
   }
   static void *newArray_maplEstringcOintgR(Long_t nElements, void *p) {
      return p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) map<string,int>[nElements] : new map<string,int>[nElements];
   }
   // Wrapper around operator delete
   static void delete_maplEstringcOintgR(void *p) {
      delete ((map<string,int>*)p);
   }
   static void deleteArray_maplEstringcOintgR(void *p) {
      delete [] ((map<string,int>*)p);
   }
   static void destruct_maplEstringcOintgR(void *p) {
      typedef map<string,int> current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class map<string,int>

namespace ROOT {
   static TClass *maplEstringcOdoublegR_Dictionary();
   static void maplEstringcOdoublegR_TClassManip(TClass*);
   static void *new_maplEstringcOdoublegR(void *p = 0);
   static void *newArray_maplEstringcOdoublegR(Long_t size, void *p);
   static void delete_maplEstringcOdoublegR(void *p);
   static void deleteArray_maplEstringcOdoublegR(void *p);
   static void destruct_maplEstringcOdoublegR(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const map<string,double>*)
   {
      map<string,double> *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(map<string,double>));
      static ::ROOT::TGenericClassInfo 
         instance("map<string,double>", -2, "map", 99,
                  typeid(map<string,double>), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &maplEstringcOdoublegR_Dictionary, isa_proxy, 0,
                  sizeof(map<string,double>) );
      instance.SetNew(&new_maplEstringcOdoublegR);
      instance.SetNewArray(&newArray_maplEstringcOdoublegR);
      instance.SetDelete(&delete_maplEstringcOdoublegR);
      instance.SetDeleteArray(&deleteArray_maplEstringcOdoublegR);
      instance.SetDestructor(&destruct_maplEstringcOdoublegR);
      instance.AdoptCollectionProxyInfo(TCollectionProxyInfo::Generate(TCollectionProxyInfo::MapInsert< map<string,double> >()));
      return &instance;
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const map<string,double>*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *maplEstringcOdoublegR_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const map<string,double>*)0x0)->GetClass();
      maplEstringcOdoublegR_TClassManip(theClass);
   return theClass;
   }

   static void maplEstringcOdoublegR_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   // Wrappers around operator new
   static void *new_maplEstringcOdoublegR(void *p) {
      return  p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) map<string,double> : new map<string,double>;
   }
   static void *newArray_maplEstringcOdoublegR(Long_t nElements, void *p) {
      return p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) map<string,double>[nElements] : new map<string,double>[nElements];
   }
   // Wrapper around operator delete
   static void delete_maplEstringcOdoublegR(void *p) {
      delete ((map<string,double>*)p);
   }
   static void deleteArray_maplEstringcOdoublegR(void *p) {
      delete [] ((map<string,double>*)p);
   }
   static void destruct_maplEstringcOdoublegR(void *p) {
      typedef map<string,double> current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class map<string,double>

namespace ROOT {
   static TClass *maplEstringcOboolgR_Dictionary();
   static void maplEstringcOboolgR_TClassManip(TClass*);
   static void *new_maplEstringcOboolgR(void *p = 0);
   static void *newArray_maplEstringcOboolgR(Long_t size, void *p);
   static void delete_maplEstringcOboolgR(void *p);
   static void deleteArray_maplEstringcOboolgR(void *p);
   static void destruct_maplEstringcOboolgR(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const map<string,bool>*)
   {
      map<string,bool> *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(map<string,bool>));
      static ::ROOT::TGenericClassInfo 
         instance("map<string,bool>", -2, "map", 99,
                  typeid(map<string,bool>), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &maplEstringcOboolgR_Dictionary, isa_proxy, 0,
                  sizeof(map<string,bool>) );
      instance.SetNew(&new_maplEstringcOboolgR);
      instance.SetNewArray(&newArray_maplEstringcOboolgR);
      instance.SetDelete(&delete_maplEstringcOboolgR);
      instance.SetDeleteArray(&deleteArray_maplEstringcOboolgR);
      instance.SetDestructor(&destruct_maplEstringcOboolgR);
      instance.AdoptCollectionProxyInfo(TCollectionProxyInfo::Generate(TCollectionProxyInfo::MapInsert< map<string,bool> >()));
      return &instance;
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const map<string,bool>*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *maplEstringcOboolgR_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const map<string,bool>*)0x0)->GetClass();
      maplEstringcOboolgR_TClassManip(theClass);
   return theClass;
   }

   static void maplEstringcOboolgR_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   // Wrappers around operator new
   static void *new_maplEstringcOboolgR(void *p) {
      return  p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) map<string,bool> : new map<string,bool>;
   }
   static void *newArray_maplEstringcOboolgR(Long_t nElements, void *p) {
      return p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) map<string,bool>[nElements] : new map<string,bool>[nElements];
   }
   // Wrapper around operator delete
   static void delete_maplEstringcOboolgR(void *p) {
      delete ((map<string,bool>*)p);
   }
   static void deleteArray_maplEstringcOboolgR(void *p) {
      delete [] ((map<string,bool>*)p);
   }
   static void destruct_maplEstringcOboolgR(void *p) {
      typedef map<string,bool> current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class map<string,bool>

namespace ROOT {
   static TClass *dequelEdoublegR_Dictionary();
   static void dequelEdoublegR_TClassManip(TClass*);
   static void *new_dequelEdoublegR(void *p = 0);
   static void *newArray_dequelEdoublegR(Long_t size, void *p);
   static void delete_dequelEdoublegR(void *p);
   static void deleteArray_dequelEdoublegR(void *p);
   static void destruct_dequelEdoublegR(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const deque<double>*)
   {
      deque<double> *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(deque<double>));
      static ::ROOT::TGenericClassInfo 
         instance("deque<double>", -2, "deque", 831,
                  typeid(deque<double>), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &dequelEdoublegR_Dictionary, isa_proxy, 0,
                  sizeof(deque<double>) );
      instance.SetNew(&new_dequelEdoublegR);
      instance.SetNewArray(&newArray_dequelEdoublegR);
      instance.SetDelete(&delete_dequelEdoublegR);
      instance.SetDeleteArray(&deleteArray_dequelEdoublegR);
      instance.SetDestructor(&destruct_dequelEdoublegR);
      instance.AdoptCollectionProxyInfo(TCollectionProxyInfo::Generate(TCollectionProxyInfo::Pushback< deque<double> >()));
      return &instance;
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const deque<double>*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *dequelEdoublegR_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const deque<double>*)0x0)->GetClass();
      dequelEdoublegR_TClassManip(theClass);
   return theClass;
   }

   static void dequelEdoublegR_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   // Wrappers around operator new
   static void *new_dequelEdoublegR(void *p) {
      return  p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) deque<double> : new deque<double>;
   }
   static void *newArray_dequelEdoublegR(Long_t nElements, void *p) {
      return p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) deque<double>[nElements] : new deque<double>[nElements];
   }
   // Wrapper around operator delete
   static void delete_dequelEdoublegR(void *p) {
      delete ((deque<double>*)p);
   }
   static void deleteArray_dequelEdoublegR(void *p) {
      delete [] ((deque<double>*)p);
   }
   static void destruct_dequelEdoublegR(void *p) {
      typedef deque<double> current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class deque<double>

namespace {
  void TriggerDictionaryInitialization_ModulesDict_Impl() {
    static const char* headers[] = {
0
    };
    static const char* includePaths[] = {
"external",
"/cvmfs/sft.cern.ch/lcg/releases/ROOT/6.14.04-0d8dc/x86_64-slc6-gcc7-opt/include",
"/afs/cern.ch/user/d/dimoulin/FCCAnalyses/Madgraph/MG5_aMC_v2_6_7/Delphes/",
0
    };
    static const char* fwdDeclCode = R"DICTFWDDCLS(
#line 1 "ModulesDict dictionary forward declarations' payload"
#pragma clang diagnostic ignored "-Wkeyword-compat"
#pragma clang diagnostic ignored "-Wignored-attributes"
#pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
extern int __Cling_Autoloading_Map;
class __attribute__((annotate("$clingAutoload$modules/Delphes.h")))  Delphes;
class __attribute__((annotate("$clingAutoload$modules/AngularSmearing.h")))  AngularSmearing;
class __attribute__((annotate("$clingAutoload$modules/PhotonConversions.h")))  PhotonConversions;
class __attribute__((annotate("$clingAutoload$modules/ParticlePropagator.h")))  ParticlePropagator;
class __attribute__((annotate("$clingAutoload$modules/Efficiency.h")))  Efficiency;
class __attribute__((annotate("$clingAutoload$modules/IdentificationMap.h")))  IdentificationMap;
class __attribute__((annotate("$clingAutoload$modules/EnergySmearing.h")))  EnergySmearing;
class __attribute__((annotate("$clingAutoload$modules/MomentumSmearing.h")))  MomentumSmearing;
class __attribute__((annotate("$clingAutoload$modules/TrackSmearing.h")))  TrackSmearing;
class __attribute__((annotate("$clingAutoload$modules/TrackCovariance.h")))  TrackCovariance;
class __attribute__((annotate("$clingAutoload$modules/ClusterCounting.h")))  ClusterCounting;
class __attribute__((annotate("$clingAutoload$modules/ImpactParameterSmearing.h")))  ImpactParameterSmearing;
class __attribute__((annotate("$clingAutoload$modules/TimeSmearing.h")))  TimeSmearing;
class __attribute__((annotate("$clingAutoload$modules/TimeOfFlight.h")))  TimeOfFlight;
class __attribute__((annotate("$clingAutoload$modules/SimpleCalorimeter.h")))  SimpleCalorimeter;
class __attribute__((annotate("$clingAutoload$modules/DenseTrackFilter.h")))  DenseTrackFilter;
class __attribute__((annotate("$clingAutoload$modules/Calorimeter.h")))  Calorimeter;
class __attribute__((annotate("$clingAutoload$modules/DualReadoutCalorimeter.h")))  DualReadoutCalorimeter;
class __attribute__((annotate("$clingAutoload$modules/OldCalorimeter.h")))  OldCalorimeter;
class __attribute__((annotate("$clingAutoload$modules/Isolation.h")))  Isolation;
class __attribute__((annotate("$clingAutoload$modules/EnergyScale.h")))  EnergyScale;
class __attribute__((annotate("$clingAutoload$modules/UniqueObjectFinder.h")))  UniqueObjectFinder;
class __attribute__((annotate("$clingAutoload$modules/TrackCountingBTagging.h")))  TrackCountingBTagging;
class __attribute__((annotate("$clingAutoload$modules/BTagging.h")))  BTagging;
class __attribute__((annotate("$clingAutoload$modules/TauTagging.h")))  TauTagging;
class __attribute__((annotate("$clingAutoload$modules/TrackCountingTauTagging.h")))  TrackCountingTauTagging;
class __attribute__((annotate("$clingAutoload$modules/TreeWriter.h")))  TreeWriter;
class __attribute__((annotate("$clingAutoload$modules/Merger.h")))  Merger;
class __attribute__((annotate("$clingAutoload$modules/LeptonDressing.h")))  LeptonDressing;
class __attribute__((annotate("$clingAutoload$modules/PileUpMerger.h")))  PileUpMerger;
class __attribute__((annotate("$clingAutoload$modules/JetPileUpSubtractor.h")))  JetPileUpSubtractor;
class __attribute__((annotate("$clingAutoload$modules/TrackPileUpSubtractor.h")))  TrackPileUpSubtractor;
class __attribute__((annotate("$clingAutoload$modules/TaggingParticlesSkimmer.h")))  TaggingParticlesSkimmer;
class __attribute__((annotate("$clingAutoload$modules/PileUpJetID.h")))  PileUpJetID;
class __attribute__((annotate("$clingAutoload$modules/PhotonID.h")))  PhotonID;
class __attribute__((annotate("$clingAutoload$modules/ConstituentFilter.h")))  ConstituentFilter;
class __attribute__((annotate("$clingAutoload$modules/StatusPidFilter.h")))  StatusPidFilter;
class __attribute__((annotate("$clingAutoload$modules/PdgCodeFilter.h")))  PdgCodeFilter;
class __attribute__((annotate("$clingAutoload$modules/BeamSpotFilter.h")))  BeamSpotFilter;
class __attribute__((annotate("$clingAutoload$modules/RecoPuFilter.h")))  RecoPuFilter;
class __attribute__((annotate("$clingAutoload$modules/Cloner.h")))  Cloner;
class __attribute__((annotate("$clingAutoload$modules/Weighter.h")))  Weighter;
class __attribute__((annotate("$clingAutoload$modules/Hector.h")))  Hector;
class __attribute__((annotate("$clingAutoload$modules/JetFlavorAssociation.h")))  JetFlavorAssociation;
class __attribute__((annotate("$clingAutoload$modules/JetFakeParticle.h")))  JetFakeParticle;
class __attribute__((annotate("$clingAutoload$modules/VertexSorter.h")))  VertexSorter;
class __attribute__((annotate("$clingAutoload$modules/VertexFinder.h")))  VertexFinder;
class __attribute__((annotate("$clingAutoload$modules/VertexFinderDA4D.h")))  VertexFinderDA4D;
class __attribute__((annotate("$clingAutoload$modules/DecayFilter.h")))  DecayFilter;
class __attribute__((annotate("$clingAutoload$modules/ParticleDensity.h")))  ParticleDensity;
class __attribute__((annotate("$clingAutoload$modules/TruthVertexFinder.h")))  TruthVertexFinder;
class __attribute__((annotate("$clingAutoload$modules/ExampleModule.h")))  ExampleModule;
)DICTFWDDCLS";
    static const char* payloadCode = R"DICTPAYLOAD(
#line 1 "ModulesDict dictionary payload"

#ifndef G__VECTOR_HAS_CLASS_ITERATOR
  #define G__VECTOR_HAS_CLASS_ITERATOR 1
#endif

#define _BACKWARD_BACKWARD_WARNING_H
/*
 *  Delphes: a framework for fast simulation of a generic collider experiment
 *  Copyright (C) 2012-2014  Universite catholique de Louvain (UCL), Belgium
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */


/** \class
 *
 *  Lists classes to be included in cint dicitonary
 *
 *  \author P. Demin - UCL, Louvain-la-Neuve
 *
 */

#include "modules/Delphes.h"

#include "modules/AngularSmearing.h"
#include "modules/PhotonConversions.h"
#include "modules/ParticlePropagator.h"
#include "modules/Efficiency.h"
#include "modules/IdentificationMap.h"
#include "modules/EnergySmearing.h"
#include "modules/MomentumSmearing.h"
#include "modules/TrackSmearing.h"
#include "modules/TrackCovariance.h"
#include "modules/ClusterCounting.h"
#include "modules/ImpactParameterSmearing.h"
#include "modules/TimeSmearing.h"
#include "modules/TimeOfFlight.h"
#include "modules/SimpleCalorimeter.h"
#include "modules/DenseTrackFilter.h"
#include "modules/Calorimeter.h"
#include "modules/DualReadoutCalorimeter.h"
#include "modules/OldCalorimeter.h"
#include "modules/Isolation.h"
#include "modules/EnergyScale.h"
#include "modules/UniqueObjectFinder.h"
#include "modules/TrackCountingBTagging.h"
#include "modules/BTagging.h"
#include "modules/TauTagging.h"
#include "modules/TrackCountingTauTagging.h"
#include "modules/TreeWriter.h"
#include "modules/Merger.h"
#include "modules/LeptonDressing.h"
#include "modules/PileUpMerger.h"
#include "modules/JetPileUpSubtractor.h"
#include "modules/TrackPileUpSubtractor.h"
#include "modules/TaggingParticlesSkimmer.h"
#include "modules/PileUpJetID.h"
#include "modules/PhotonID.h"
#include "modules/ConstituentFilter.h"
#include "modules/StatusPidFilter.h"
#include "modules/PdgCodeFilter.h"
#include "modules/BeamSpotFilter.h"
#include "modules/RecoPuFilter.h"
#include "modules/Cloner.h"
#include "modules/Weighter.h"
#include "modules/Hector.h"
#include "modules/JetFlavorAssociation.h"
#include "modules/JetFakeParticle.h"
#include "modules/VertexSorter.h"
#include "modules/VertexFinder.h"
#include "modules/VertexFinderDA4D.h"
#include "modules/DecayFilter.h"
#include "modules/ParticleDensity.h"
#include "modules/TruthVertexFinder.h"
#include "modules/ExampleModule.h"

#ifdef __CINT__

#pragma link off all globals;
#pragma link off all classes;
#pragma link off all functions;

#pragma link C++ class Delphes+;

#pragma link C++ class AngularSmearing+;
#pragma link C++ class PhotonConversions+;
#pragma link C++ class ParticlePropagator+;
#pragma link C++ class Efficiency+;
#pragma link C++ class IdentificationMap+;
#pragma link C++ class EnergySmearing+;
#pragma link C++ class MomentumSmearing+;
#pragma link C++ class TrackSmearing+;
#pragma link C++ class TrackCovariance+;
#pragma link C++ class ClusterCounting+;
#pragma link C++ class ImpactParameterSmearing+;
#pragma link C++ class TimeSmearing+;
#pragma link C++ class TimeOfFlight+;
#pragma link C++ class SimpleCalorimeter+;
#pragma link C++ class DenseTrackFilter+;
#pragma link C++ class Calorimeter+;
#pragma link C++ class DualReadoutCalorimeter+;
#pragma link C++ class OldCalorimeter+;
#pragma link C++ class Isolation+;
#pragma link C++ class EnergyScale+;
#pragma link C++ class UniqueObjectFinder+;
#pragma link C++ class TrackCountingBTagging+;
#pragma link C++ class BTagging+;
#pragma link C++ class TauTagging+;
#pragma link C++ class TrackCountingTauTagging+;
#pragma link C++ class TreeWriter+;
#pragma link C++ class Merger+;
#pragma link C++ class LeptonDressing+;
#pragma link C++ class PileUpMerger+;
#pragma link C++ class JetPileUpSubtractor+;
#pragma link C++ class TrackPileUpSubtractor+;
#pragma link C++ class TaggingParticlesSkimmer+;
#pragma link C++ class PileUpJetID+;
#pragma link C++ class PhotonID+;
#pragma link C++ class ConstituentFilter+;
#pragma link C++ class StatusPidFilter+;
#pragma link C++ class PdgCodeFilter+;
#pragma link C++ class BeamSpotFilter+;
#pragma link C++ class RecoPuFilter+;
#pragma link C++ class Cloner+;
#pragma link C++ class Weighter+;
#pragma link C++ class Hector+;
#pragma link C++ class JetFlavorAssociation+;
#pragma link C++ class JetFakeParticle+;
#pragma link C++ class VertexSorter+;
#pragma link C++ class VertexFinder+;
#pragma link C++ class VertexFinderDA4D+;
#pragma link C++ class DecayFilter+;
#pragma link C++ class ParticleDensity+;
#pragma link C++ class TruthVertexFinder+;
#pragma link C++ class ExampleModule+;

#endif

#undef  _BACKWARD_BACKWARD_WARNING_H
)DICTPAYLOAD";
    static const char* classesHeaders[]={
"AngularSmearing", payloadCode, "@",
"BTagging", payloadCode, "@",
"BeamSpotFilter", payloadCode, "@",
"Calorimeter", payloadCode, "@",
"Cloner", payloadCode, "@",
"ClusterCounting", payloadCode, "@",
"ConstituentFilter", payloadCode, "@",
"DecayFilter", payloadCode, "@",
"Delphes", payloadCode, "@",
"DenseTrackFilter", payloadCode, "@",
"DualReadoutCalorimeter", payloadCode, "@",
"Efficiency", payloadCode, "@",
"EnergyScale", payloadCode, "@",
"EnergySmearing", payloadCode, "@",
"ExampleModule", payloadCode, "@",
"Hector", payloadCode, "@",
"IdentificationMap", payloadCode, "@",
"ImpactParameterSmearing", payloadCode, "@",
"Isolation", payloadCode, "@",
"JetFakeParticle", payloadCode, "@",
"JetFlavorAssociation", payloadCode, "@",
"JetPileUpSubtractor", payloadCode, "@",
"LeptonDressing", payloadCode, "@",
"Merger", payloadCode, "@",
"MomentumSmearing", payloadCode, "@",
"OldCalorimeter", payloadCode, "@",
"ParticleDensity", payloadCode, "@",
"ParticlePropagator", payloadCode, "@",
"PdgCodeFilter", payloadCode, "@",
"PhotonConversions", payloadCode, "@",
"PhotonID", payloadCode, "@",
"PileUpJetID", payloadCode, "@",
"PileUpMerger", payloadCode, "@",
"RecoPuFilter", payloadCode, "@",
"SimpleCalorimeter", payloadCode, "@",
"StatusPidFilter", payloadCode, "@",
"TaggingParticlesSkimmer", payloadCode, "@",
"TauTagging", payloadCode, "@",
"TimeOfFlight", payloadCode, "@",
"TimeSmearing", payloadCode, "@",
"TrackCountingBTagging", payloadCode, "@",
"TrackCountingTauTagging", payloadCode, "@",
"TrackCovariance", payloadCode, "@",
"TrackPileUpSubtractor", payloadCode, "@",
"TrackSmearing", payloadCode, "@",
"TreeWriter", payloadCode, "@",
"TruthVertexFinder", payloadCode, "@",
"UniqueObjectFinder", payloadCode, "@",
"VertexFinder", payloadCode, "@",
"VertexFinderDA4D", payloadCode, "@",
"VertexSorter", payloadCode, "@",
"Weighter", payloadCode, "@",
nullptr};

    static bool isInitialized = false;
    if (!isInitialized) {
      TROOT::RegisterModule("ModulesDict",
        headers, includePaths, payloadCode, fwdDeclCode,
        TriggerDictionaryInitialization_ModulesDict_Impl, {}, classesHeaders, /*has no C++ module*/false);
      isInitialized = true;
    }
  }
  static struct DictInit {
    DictInit() {
      TriggerDictionaryInitialization_ModulesDict_Impl();
    }
  } __TheDictionaryInitializer;
}
void TriggerDictionaryInitialization_ModulesDict() {
  TriggerDictionaryInitialization_ModulesDict_Impl();
}
