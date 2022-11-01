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


/** ExRootAnalysisLinkDef
 *
 *  Lists classes to be included in cint dicitonary
 *
 *  \author P. Demin - UCL, Louvain-la-Neuve
 *
 */

#include "classes/DelphesModule.h"
#include "classes/DelphesFactory.h"

#include "classes/SortableObject.h"
#include "classes/DelphesClasses.h"

#ifdef __CINT__

#pragma link off all globals;
#pragma link off all classes;
#pragma link off all functions;

#pragma link C++ class DelphesModule+;
#pragma link C++ class DelphesFactory+;

#pragma link C++ class SortableObject+;

#pragma link C++ class Event+;
#pragma link C++ class LHCOEvent+;
#pragma link C++ class LHEFEvent+;
#pragma link C++ class LHEFWeight+;
#pragma link C++ class HepMCEvent+;
#pragma link C++ class GenParticle+;
#pragma link C++ class Vertex+;
#pragma link C++ class MissingET+;
#pragma link C++ class ScalarHT+;
#pragma link C++ class Rho+;
#pragma link C++ class Weight+;
#pragma link C++ class Photon+;
#pragma link C++ class Electron+;
#pragma link C++ class Muon+;
#pragma link C++ class Jet+;
#pragma link C++ class Track+;
#pragma link C++ class Tower+;
#pragma link C++ class ParticleFlowCandidate+;
#pragma link C++ class HectorHit+;

#pragma link C++ class Candidate+;

#endif

// Do NOT change. Changes will be lost next time file is generated

#define R__DICTIONARY_FILENAME tmpdIclassesdIClassesDict

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
#include "classes/DelphesModule.h"
#include "classes/DelphesFactory.h"
#include "classes/SortableObject.h"
#include "classes/DelphesClasses.h"

// Header files passed via #pragma extra_include

namespace ROOT {
   static void *new_DelphesModule(void *p = 0);
   static void *newArray_DelphesModule(Long_t size, void *p);
   static void delete_DelphesModule(void *p);
   static void deleteArray_DelphesModule(void *p);
   static void destruct_DelphesModule(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::DelphesModule*)
   {
      ::DelphesModule *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::DelphesModule >(0);
      static ::ROOT::TGenericClassInfo 
         instance("DelphesModule", ::DelphesModule::Class_Version(), "classes/DelphesModule.h", 43,
                  typeid(::DelphesModule), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::DelphesModule::Dictionary, isa_proxy, 4,
                  sizeof(::DelphesModule) );
      instance.SetNew(&new_DelphesModule);
      instance.SetNewArray(&newArray_DelphesModule);
      instance.SetDelete(&delete_DelphesModule);
      instance.SetDeleteArray(&deleteArray_DelphesModule);
      instance.SetDestructor(&destruct_DelphesModule);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::DelphesModule*)
   {
      return GenerateInitInstanceLocal((::DelphesModule*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::DelphesModule*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_DelphesFactory(void *p = 0);
   static void *newArray_DelphesFactory(Long_t size, void *p);
   static void delete_DelphesFactory(void *p);
   static void deleteArray_DelphesFactory(void *p);
   static void destruct_DelphesFactory(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::DelphesFactory*)
   {
      ::DelphesFactory *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::DelphesFactory >(0);
      static ::ROOT::TGenericClassInfo 
         instance("DelphesFactory", ::DelphesFactory::Class_Version(), "classes/DelphesFactory.h", 41,
                  typeid(::DelphesFactory), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::DelphesFactory::Dictionary, isa_proxy, 4,
                  sizeof(::DelphesFactory) );
      instance.SetNew(&new_DelphesFactory);
      instance.SetNewArray(&newArray_DelphesFactory);
      instance.SetDelete(&delete_DelphesFactory);
      instance.SetDeleteArray(&deleteArray_DelphesFactory);
      instance.SetDestructor(&destruct_DelphesFactory);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::DelphesFactory*)
   {
      return GenerateInitInstanceLocal((::DelphesFactory*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::DelphesFactory*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void delete_SortableObject(void *p);
   static void deleteArray_SortableObject(void *p);
   static void destruct_SortableObject(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::SortableObject*)
   {
      ::SortableObject *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::SortableObject >(0);
      static ::ROOT::TGenericClassInfo 
         instance("SortableObject", ::SortableObject::Class_Version(), "classes/SortableObject.h", 46,
                  typeid(::SortableObject), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::SortableObject::Dictionary, isa_proxy, 4,
                  sizeof(::SortableObject) );
      instance.SetDelete(&delete_SortableObject);
      instance.SetDeleteArray(&deleteArray_SortableObject);
      instance.SetDestructor(&destruct_SortableObject);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::SortableObject*)
   {
      return GenerateInitInstanceLocal((::SortableObject*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::SortableObject*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_Event(void *p = 0);
   static void *newArray_Event(Long_t size, void *p);
   static void delete_Event(void *p);
   static void deleteArray_Event(void *p);
   static void destruct_Event(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::Event*)
   {
      ::Event *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::Event >(0);
      static ::ROOT::TGenericClassInfo 
         instance("Event", ::Event::Class_Version(), "classes/DelphesClasses.h", 46,
                  typeid(::Event), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::Event::Dictionary, isa_proxy, 4,
                  sizeof(::Event) );
      instance.SetNew(&new_Event);
      instance.SetNewArray(&newArray_Event);
      instance.SetDelete(&delete_Event);
      instance.SetDeleteArray(&deleteArray_Event);
      instance.SetDestructor(&destruct_Event);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::Event*)
   {
      return GenerateInitInstanceLocal((::Event*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::Event*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_LHCOEvent(void *p = 0);
   static void *newArray_LHCOEvent(Long_t size, void *p);
   static void delete_LHCOEvent(void *p);
   static void deleteArray_LHCOEvent(void *p);
   static void destruct_LHCOEvent(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::LHCOEvent*)
   {
      ::LHCOEvent *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::LHCOEvent >(0);
      static ::ROOT::TGenericClassInfo 
         instance("LHCOEvent", ::LHCOEvent::Class_Version(), "classes/DelphesClasses.h", 59,
                  typeid(::LHCOEvent), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::LHCOEvent::Dictionary, isa_proxy, 4,
                  sizeof(::LHCOEvent) );
      instance.SetNew(&new_LHCOEvent);
      instance.SetNewArray(&newArray_LHCOEvent);
      instance.SetDelete(&delete_LHCOEvent);
      instance.SetDeleteArray(&deleteArray_LHCOEvent);
      instance.SetDestructor(&destruct_LHCOEvent);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::LHCOEvent*)
   {
      return GenerateInitInstanceLocal((::LHCOEvent*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::LHCOEvent*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_LHEFEvent(void *p = 0);
   static void *newArray_LHEFEvent(Long_t size, void *p);
   static void delete_LHEFEvent(void *p);
   static void deleteArray_LHEFEvent(void *p);
   static void destruct_LHEFEvent(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::LHEFEvent*)
   {
      ::LHEFEvent *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::LHEFEvent >(0);
      static ::ROOT::TGenericClassInfo 
         instance("LHEFEvent", ::LHEFEvent::Class_Version(), "classes/DelphesClasses.h", 69,
                  typeid(::LHEFEvent), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::LHEFEvent::Dictionary, isa_proxy, 4,
                  sizeof(::LHEFEvent) );
      instance.SetNew(&new_LHEFEvent);
      instance.SetNewArray(&newArray_LHEFEvent);
      instance.SetDelete(&delete_LHEFEvent);
      instance.SetDeleteArray(&deleteArray_LHEFEvent);
      instance.SetDestructor(&destruct_LHEFEvent);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::LHEFEvent*)
   {
      return GenerateInitInstanceLocal((::LHEFEvent*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::LHEFEvent*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_LHEFWeight(void *p = 0);
   static void *newArray_LHEFWeight(Long_t size, void *p);
   static void delete_LHEFWeight(void *p);
   static void deleteArray_LHEFWeight(void *p);
   static void destruct_LHEFWeight(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::LHEFWeight*)
   {
      ::LHEFWeight *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::LHEFWeight >(0);
      static ::ROOT::TGenericClassInfo 
         instance("LHEFWeight", ::LHEFWeight::Class_Version(), "classes/DelphesClasses.h", 85,
                  typeid(::LHEFWeight), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::LHEFWeight::Dictionary, isa_proxy, 4,
                  sizeof(::LHEFWeight) );
      instance.SetNew(&new_LHEFWeight);
      instance.SetNewArray(&newArray_LHEFWeight);
      instance.SetDelete(&delete_LHEFWeight);
      instance.SetDeleteArray(&deleteArray_LHEFWeight);
      instance.SetDestructor(&destruct_LHEFWeight);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::LHEFWeight*)
   {
      return GenerateInitInstanceLocal((::LHEFWeight*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::LHEFWeight*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_HepMCEvent(void *p = 0);
   static void *newArray_HepMCEvent(Long_t size, void *p);
   static void delete_HepMCEvent(void *p);
   static void deleteArray_HepMCEvent(void *p);
   static void destruct_HepMCEvent(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::HepMCEvent*)
   {
      ::HepMCEvent *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::HepMCEvent >(0);
      static ::ROOT::TGenericClassInfo 
         instance("HepMCEvent", ::HepMCEvent::Class_Version(), "classes/DelphesClasses.h", 96,
                  typeid(::HepMCEvent), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::HepMCEvent::Dictionary, isa_proxy, 4,
                  sizeof(::HepMCEvent) );
      instance.SetNew(&new_HepMCEvent);
      instance.SetNewArray(&newArray_HepMCEvent);
      instance.SetDelete(&delete_HepMCEvent);
      instance.SetDeleteArray(&deleteArray_HepMCEvent);
      instance.SetDestructor(&destruct_HepMCEvent);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::HepMCEvent*)
   {
      return GenerateInitInstanceLocal((::HepMCEvent*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::HepMCEvent*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_GenParticle(void *p = 0);
   static void *newArray_GenParticle(Long_t size, void *p);
   static void delete_GenParticle(void *p);
   static void deleteArray_GenParticle(void *p);
   static void destruct_GenParticle(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::GenParticle*)
   {
      ::GenParticle *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::GenParticle >(0);
      static ::ROOT::TGenericClassInfo 
         instance("GenParticle", ::GenParticle::Class_Version(), "classes/DelphesClasses.h", 126,
                  typeid(::GenParticle), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::GenParticle::Dictionary, isa_proxy, 4,
                  sizeof(::GenParticle) );
      instance.SetNew(&new_GenParticle);
      instance.SetNewArray(&newArray_GenParticle);
      instance.SetDelete(&delete_GenParticle);
      instance.SetDeleteArray(&deleteArray_GenParticle);
      instance.SetDestructor(&destruct_GenParticle);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::GenParticle*)
   {
      return GenerateInitInstanceLocal((::GenParticle*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::GenParticle*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_Vertex(void *p = 0);
   static void *newArray_Vertex(Long_t size, void *p);
   static void delete_Vertex(void *p);
   static void deleteArray_Vertex(void *p);
   static void destruct_Vertex(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::Vertex*)
   {
      ::Vertex *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::Vertex >(0);
      static ::ROOT::TGenericClassInfo 
         instance("Vertex", ::Vertex::Class_Version(), "classes/DelphesClasses.h", 170,
                  typeid(::Vertex), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::Vertex::Dictionary, isa_proxy, 4,
                  sizeof(::Vertex) );
      instance.SetNew(&new_Vertex);
      instance.SetNewArray(&newArray_Vertex);
      instance.SetDelete(&delete_Vertex);
      instance.SetDeleteArray(&deleteArray_Vertex);
      instance.SetDestructor(&destruct_Vertex);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::Vertex*)
   {
      return GenerateInitInstanceLocal((::Vertex*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::Vertex*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_MissingET(void *p = 0);
   static void *newArray_MissingET(Long_t size, void *p);
   static void delete_MissingET(void *p);
   static void deleteArray_MissingET(void *p);
   static void destruct_MissingET(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::MissingET*)
   {
      ::MissingET *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::MissingET >(0);
      static ::ROOT::TGenericClassInfo 
         instance("MissingET", ::MissingET::Class_Version(), "classes/DelphesClasses.h", 203,
                  typeid(::MissingET), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::MissingET::Dictionary, isa_proxy, 4,
                  sizeof(::MissingET) );
      instance.SetNew(&new_MissingET);
      instance.SetNewArray(&newArray_MissingET);
      instance.SetDelete(&delete_MissingET);
      instance.SetDeleteArray(&deleteArray_MissingET);
      instance.SetDestructor(&destruct_MissingET);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::MissingET*)
   {
      return GenerateInitInstanceLocal((::MissingET*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::MissingET*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_ScalarHT(void *p = 0);
   static void *newArray_ScalarHT(Long_t size, void *p);
   static void delete_ScalarHT(void *p);
   static void deleteArray_ScalarHT(void *p);
   static void destruct_ScalarHT(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::ScalarHT*)
   {
      ::ScalarHT *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::ScalarHT >(0);
      static ::ROOT::TGenericClassInfo 
         instance("ScalarHT", ::ScalarHT::Class_Version(), "classes/DelphesClasses.h", 217,
                  typeid(::ScalarHT), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::ScalarHT::Dictionary, isa_proxy, 4,
                  sizeof(::ScalarHT) );
      instance.SetNew(&new_ScalarHT);
      instance.SetNewArray(&newArray_ScalarHT);
      instance.SetDelete(&delete_ScalarHT);
      instance.SetDeleteArray(&deleteArray_ScalarHT);
      instance.SetDestructor(&destruct_ScalarHT);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::ScalarHT*)
   {
      return GenerateInitInstanceLocal((::ScalarHT*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::ScalarHT*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_Rho(void *p = 0);
   static void *newArray_Rho(Long_t size, void *p);
   static void delete_Rho(void *p);
   static void deleteArray_Rho(void *p);
   static void destruct_Rho(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::Rho*)
   {
      ::Rho *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::Rho >(0);
      static ::ROOT::TGenericClassInfo 
         instance("Rho", ::Rho::Class_Version(), "classes/DelphesClasses.h", 227,
                  typeid(::Rho), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::Rho::Dictionary, isa_proxy, 4,
                  sizeof(::Rho) );
      instance.SetNew(&new_Rho);
      instance.SetNewArray(&newArray_Rho);
      instance.SetDelete(&delete_Rho);
      instance.SetDeleteArray(&deleteArray_Rho);
      instance.SetDestructor(&destruct_Rho);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::Rho*)
   {
      return GenerateInitInstanceLocal((::Rho*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::Rho*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_Weight(void *p = 0);
   static void *newArray_Weight(Long_t size, void *p);
   static void delete_Weight(void *p);
   static void deleteArray_Weight(void *p);
   static void destruct_Weight(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::Weight*)
   {
      ::Weight *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::Weight >(0);
      static ::ROOT::TGenericClassInfo 
         instance("Weight", ::Weight::Class_Version(), "classes/DelphesClasses.h", 238,
                  typeid(::Weight), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::Weight::Dictionary, isa_proxy, 4,
                  sizeof(::Weight) );
      instance.SetNew(&new_Weight);
      instance.SetNewArray(&newArray_Weight);
      instance.SetDelete(&delete_Weight);
      instance.SetDeleteArray(&deleteArray_Weight);
      instance.SetDestructor(&destruct_Weight);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::Weight*)
   {
      return GenerateInitInstanceLocal((::Weight*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::Weight*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_Photon(void *p = 0);
   static void *newArray_Photon(Long_t size, void *p);
   static void delete_Photon(void *p);
   static void deleteArray_Photon(void *p);
   static void destruct_Photon(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::Photon*)
   {
      ::Photon *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::Photon >(0);
      static ::ROOT::TGenericClassInfo 
         instance("Photon", ::Photon::Class_Version(), "classes/DelphesClasses.h", 248,
                  typeid(::Photon), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::Photon::Dictionary, isa_proxy, 4,
                  sizeof(::Photon) );
      instance.SetNew(&new_Photon);
      instance.SetNewArray(&newArray_Photon);
      instance.SetDelete(&delete_Photon);
      instance.SetDeleteArray(&deleteArray_Photon);
      instance.SetDestructor(&destruct_Photon);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::Photon*)
   {
      return GenerateInitInstanceLocal((::Photon*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::Photon*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_Electron(void *p = 0);
   static void *newArray_Electron(Long_t size, void *p);
   static void delete_Electron(void *p);
   static void deleteArray_Electron(void *p);
   static void destruct_Electron(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::Electron*)
   {
      ::Electron *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::Electron >(0);
      static ::ROOT::TGenericClassInfo 
         instance("Electron", ::Electron::Class_Version(), "classes/DelphesClasses.h", 282,
                  typeid(::Electron), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::Electron::Dictionary, isa_proxy, 4,
                  sizeof(::Electron) );
      instance.SetNew(&new_Electron);
      instance.SetNewArray(&newArray_Electron);
      instance.SetDelete(&delete_Electron);
      instance.SetDeleteArray(&deleteArray_Electron);
      instance.SetDestructor(&destruct_Electron);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::Electron*)
   {
      return GenerateInitInstanceLocal((::Electron*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::Electron*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_Muon(void *p = 0);
   static void *newArray_Muon(Long_t size, void *p);
   static void delete_Muon(void *p);
   static void deleteArray_Muon(void *p);
   static void destruct_Muon(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::Muon*)
   {
      ::Muon *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::Muon >(0);
      static ::ROOT::TGenericClassInfo 
         instance("Muon", ::Muon::Class_Version(), "classes/DelphesClasses.h", 319,
                  typeid(::Muon), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::Muon::Dictionary, isa_proxy, 4,
                  sizeof(::Muon) );
      instance.SetNew(&new_Muon);
      instance.SetNewArray(&newArray_Muon);
      instance.SetDelete(&delete_Muon);
      instance.SetDeleteArray(&deleteArray_Muon);
      instance.SetDestructor(&destruct_Muon);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::Muon*)
   {
      return GenerateInitInstanceLocal((::Muon*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::Muon*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_Jet(void *p = 0);
   static void *newArray_Jet(Long_t size, void *p);
   static void delete_Jet(void *p);
   static void deleteArray_Jet(void *p);
   static void destruct_Jet(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::Jet*)
   {
      ::Jet *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::Jet >(0);
      static ::ROOT::TGenericClassInfo 
         instance("Jet", ::Jet::Class_Version(), "classes/DelphesClasses.h", 354,
                  typeid(::Jet), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::Jet::Dictionary, isa_proxy, 4,
                  sizeof(::Jet) );
      instance.SetNew(&new_Jet);
      instance.SetNewArray(&newArray_Jet);
      instance.SetDelete(&delete_Jet);
      instance.SetDeleteArray(&deleteArray_Jet);
      instance.SetDestructor(&destruct_Jet);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::Jet*)
   {
      return GenerateInitInstanceLocal((::Jet*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::Jet*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_Track(void *p = 0);
   static void *newArray_Track(Long_t size, void *p);
   static void delete_Track(void *p);
   static void deleteArray_Track(void *p);
   static void destruct_Track(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::Track*)
   {
      ::Track *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::Track >(0);
      static ::ROOT::TGenericClassInfo 
         instance("Track", ::Track::Class_Version(), "classes/DelphesClasses.h", 428,
                  typeid(::Track), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::Track::Dictionary, isa_proxy, 4,
                  sizeof(::Track) );
      instance.SetNew(&new_Track);
      instance.SetNewArray(&newArray_Track);
      instance.SetDelete(&delete_Track);
      instance.SetDeleteArray(&deleteArray_Track);
      instance.SetDestructor(&destruct_Track);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::Track*)
   {
      return GenerateInitInstanceLocal((::Track*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::Track*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_Tower(void *p = 0);
   static void *newArray_Tower(Long_t size, void *p);
   static void delete_Tower(void *p);
   static void deleteArray_Tower(void *p);
   static void destruct_Tower(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::Tower*)
   {
      ::Tower *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::Tower >(0);
      static ::ROOT::TGenericClassInfo 
         instance("Tower", ::Tower::Class_Version(), "classes/DelphesClasses.h", 503,
                  typeid(::Tower), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::Tower::Dictionary, isa_proxy, 4,
                  sizeof(::Tower) );
      instance.SetNew(&new_Tower);
      instance.SetNewArray(&newArray_Tower);
      instance.SetDelete(&delete_Tower);
      instance.SetDeleteArray(&deleteArray_Tower);
      instance.SetDestructor(&destruct_Tower);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::Tower*)
   {
      return GenerateInitInstanceLocal((::Tower*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::Tower*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_ParticleFlowCandidate(void *p = 0);
   static void *newArray_ParticleFlowCandidate(Long_t size, void *p);
   static void delete_ParticleFlowCandidate(void *p);
   static void deleteArray_ParticleFlowCandidate(void *p);
   static void destruct_ParticleFlowCandidate(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::ParticleFlowCandidate*)
   {
      ::ParticleFlowCandidate *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::ParticleFlowCandidate >(0);
      static ::ROOT::TGenericClassInfo 
         instance("ParticleFlowCandidate", ::ParticleFlowCandidate::Class_Version(), "classes/DelphesClasses.h", 532,
                  typeid(::ParticleFlowCandidate), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::ParticleFlowCandidate::Dictionary, isa_proxy, 4,
                  sizeof(::ParticleFlowCandidate) );
      instance.SetNew(&new_ParticleFlowCandidate);
      instance.SetNewArray(&newArray_ParticleFlowCandidate);
      instance.SetDelete(&delete_ParticleFlowCandidate);
      instance.SetDeleteArray(&deleteArray_ParticleFlowCandidate);
      instance.SetDestructor(&destruct_ParticleFlowCandidate);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::ParticleFlowCandidate*)
   {
      return GenerateInitInstanceLocal((::ParticleFlowCandidate*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::ParticleFlowCandidate*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_HectorHit(void *p = 0);
   static void *newArray_HectorHit(Long_t size, void *p);
   static void delete_HectorHit(void *p);
   static void deleteArray_HectorHit(void *p);
   static void destruct_HectorHit(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::HectorHit*)
   {
      ::HectorHit *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::HectorHit >(0);
      static ::ROOT::TGenericClassInfo 
         instance("HectorHit", ::HectorHit::Class_Version(), "classes/DelphesClasses.h", 617,
                  typeid(::HectorHit), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::HectorHit::Dictionary, isa_proxy, 4,
                  sizeof(::HectorHit) );
      instance.SetNew(&new_HectorHit);
      instance.SetNewArray(&newArray_HectorHit);
      instance.SetDelete(&delete_HectorHit);
      instance.SetDeleteArray(&deleteArray_HectorHit);
      instance.SetDestructor(&destruct_HectorHit);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::HectorHit*)
   {
      return GenerateInitInstanceLocal((::HectorHit*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::HectorHit*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_Candidate(void *p = 0);
   static void *newArray_Candidate(Long_t size, void *p);
   static void delete_Candidate(void *p);
   static void deleteArray_Candidate(void *p);
   static void destruct_Candidate(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::Candidate*)
   {
      ::Candidate *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::Candidate >(0);
      static ::ROOT::TGenericClassInfo 
         instance("Candidate", ::Candidate::Class_Version(), "classes/DelphesClasses.h", 641,
                  typeid(::Candidate), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::Candidate::Dictionary, isa_proxy, 4,
                  sizeof(::Candidate) );
      instance.SetNew(&new_Candidate);
      instance.SetNewArray(&newArray_Candidate);
      instance.SetDelete(&delete_Candidate);
      instance.SetDeleteArray(&deleteArray_Candidate);
      instance.SetDestructor(&destruct_Candidate);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::Candidate*)
   {
      return GenerateInitInstanceLocal((::Candidate*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::Candidate*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

//______________________________________________________________________________
atomic_TClass_ptr DelphesModule::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *DelphesModule::Class_Name()
{
   return "DelphesModule";
}

//______________________________________________________________________________
const char *DelphesModule::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::DelphesModule*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int DelphesModule::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::DelphesModule*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *DelphesModule::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::DelphesModule*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *DelphesModule::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::DelphesModule*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr DelphesFactory::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *DelphesFactory::Class_Name()
{
   return "DelphesFactory";
}

//______________________________________________________________________________
const char *DelphesFactory::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::DelphesFactory*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int DelphesFactory::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::DelphesFactory*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *DelphesFactory::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::DelphesFactory*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *DelphesFactory::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::DelphesFactory*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr SortableObject::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *SortableObject::Class_Name()
{
   return "SortableObject";
}

//______________________________________________________________________________
const char *SortableObject::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::SortableObject*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int SortableObject::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::SortableObject*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *SortableObject::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::SortableObject*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *SortableObject::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::SortableObject*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr Event::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *Event::Class_Name()
{
   return "Event";
}

//______________________________________________________________________________
const char *Event::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::Event*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int Event::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::Event*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *Event::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::Event*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *Event::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::Event*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr LHCOEvent::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *LHCOEvent::Class_Name()
{
   return "LHCOEvent";
}

//______________________________________________________________________________
const char *LHCOEvent::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::LHCOEvent*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int LHCOEvent::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::LHCOEvent*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *LHCOEvent::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::LHCOEvent*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *LHCOEvent::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::LHCOEvent*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr LHEFEvent::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *LHEFEvent::Class_Name()
{
   return "LHEFEvent";
}

//______________________________________________________________________________
const char *LHEFEvent::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::LHEFEvent*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int LHEFEvent::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::LHEFEvent*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *LHEFEvent::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::LHEFEvent*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *LHEFEvent::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::LHEFEvent*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr LHEFWeight::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *LHEFWeight::Class_Name()
{
   return "LHEFWeight";
}

//______________________________________________________________________________
const char *LHEFWeight::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::LHEFWeight*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int LHEFWeight::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::LHEFWeight*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *LHEFWeight::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::LHEFWeight*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *LHEFWeight::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::LHEFWeight*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr HepMCEvent::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *HepMCEvent::Class_Name()
{
   return "HepMCEvent";
}

//______________________________________________________________________________
const char *HepMCEvent::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::HepMCEvent*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int HepMCEvent::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::HepMCEvent*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *HepMCEvent::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::HepMCEvent*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *HepMCEvent::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::HepMCEvent*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr GenParticle::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *GenParticle::Class_Name()
{
   return "GenParticle";
}

//______________________________________________________________________________
const char *GenParticle::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::GenParticle*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int GenParticle::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::GenParticle*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *GenParticle::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::GenParticle*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *GenParticle::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::GenParticle*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr Vertex::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *Vertex::Class_Name()
{
   return "Vertex";
}

//______________________________________________________________________________
const char *Vertex::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::Vertex*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int Vertex::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::Vertex*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *Vertex::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::Vertex*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *Vertex::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::Vertex*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr MissingET::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *MissingET::Class_Name()
{
   return "MissingET";
}

//______________________________________________________________________________
const char *MissingET::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::MissingET*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int MissingET::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::MissingET*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *MissingET::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::MissingET*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *MissingET::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::MissingET*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr ScalarHT::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *ScalarHT::Class_Name()
{
   return "ScalarHT";
}

//______________________________________________________________________________
const char *ScalarHT::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::ScalarHT*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int ScalarHT::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::ScalarHT*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *ScalarHT::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::ScalarHT*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *ScalarHT::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::ScalarHT*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr Rho::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *Rho::Class_Name()
{
   return "Rho";
}

//______________________________________________________________________________
const char *Rho::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::Rho*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int Rho::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::Rho*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *Rho::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::Rho*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *Rho::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::Rho*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr Weight::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *Weight::Class_Name()
{
   return "Weight";
}

//______________________________________________________________________________
const char *Weight::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::Weight*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int Weight::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::Weight*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *Weight::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::Weight*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *Weight::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::Weight*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr Photon::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *Photon::Class_Name()
{
   return "Photon";
}

//______________________________________________________________________________
const char *Photon::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::Photon*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int Photon::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::Photon*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *Photon::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::Photon*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *Photon::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::Photon*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr Electron::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *Electron::Class_Name()
{
   return "Electron";
}

//______________________________________________________________________________
const char *Electron::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::Electron*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int Electron::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::Electron*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *Electron::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::Electron*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *Electron::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::Electron*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr Muon::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *Muon::Class_Name()
{
   return "Muon";
}

//______________________________________________________________________________
const char *Muon::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::Muon*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int Muon::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::Muon*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *Muon::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::Muon*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *Muon::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::Muon*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr Jet::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *Jet::Class_Name()
{
   return "Jet";
}

//______________________________________________________________________________
const char *Jet::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::Jet*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int Jet::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::Jet*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *Jet::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::Jet*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *Jet::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::Jet*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr Track::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *Track::Class_Name()
{
   return "Track";
}

//______________________________________________________________________________
const char *Track::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::Track*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int Track::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::Track*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *Track::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::Track*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *Track::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::Track*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr Tower::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *Tower::Class_Name()
{
   return "Tower";
}

//______________________________________________________________________________
const char *Tower::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::Tower*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int Tower::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::Tower*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *Tower::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::Tower*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *Tower::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::Tower*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr ParticleFlowCandidate::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *ParticleFlowCandidate::Class_Name()
{
   return "ParticleFlowCandidate";
}

//______________________________________________________________________________
const char *ParticleFlowCandidate::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::ParticleFlowCandidate*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int ParticleFlowCandidate::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::ParticleFlowCandidate*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *ParticleFlowCandidate::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::ParticleFlowCandidate*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *ParticleFlowCandidate::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::ParticleFlowCandidate*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr HectorHit::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *HectorHit::Class_Name()
{
   return "HectorHit";
}

//______________________________________________________________________________
const char *HectorHit::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::HectorHit*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int HectorHit::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::HectorHit*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *HectorHit::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::HectorHit*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *HectorHit::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::HectorHit*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr Candidate::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *Candidate::Class_Name()
{
   return "Candidate";
}

//______________________________________________________________________________
const char *Candidate::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::Candidate*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int Candidate::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::Candidate*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *Candidate::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::Candidate*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *Candidate::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::Candidate*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
void DelphesModule::Streamer(TBuffer &R__b)
{
   // Stream an object of class DelphesModule.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(DelphesModule::Class(),this);
   } else {
      R__b.WriteClassBuffer(DelphesModule::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_DelphesModule(void *p) {
      return  p ? new(p) ::DelphesModule : new ::DelphesModule;
   }
   static void *newArray_DelphesModule(Long_t nElements, void *p) {
      return p ? new(p) ::DelphesModule[nElements] : new ::DelphesModule[nElements];
   }
   // Wrapper around operator delete
   static void delete_DelphesModule(void *p) {
      delete ((::DelphesModule*)p);
   }
   static void deleteArray_DelphesModule(void *p) {
      delete [] ((::DelphesModule*)p);
   }
   static void destruct_DelphesModule(void *p) {
      typedef ::DelphesModule current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::DelphesModule

//______________________________________________________________________________
void DelphesFactory::Streamer(TBuffer &R__b)
{
   // Stream an object of class DelphesFactory.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(DelphesFactory::Class(),this);
   } else {
      R__b.WriteClassBuffer(DelphesFactory::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_DelphesFactory(void *p) {
      return  p ? new(p) ::DelphesFactory : new ::DelphesFactory;
   }
   static void *newArray_DelphesFactory(Long_t nElements, void *p) {
      return p ? new(p) ::DelphesFactory[nElements] : new ::DelphesFactory[nElements];
   }
   // Wrapper around operator delete
   static void delete_DelphesFactory(void *p) {
      delete ((::DelphesFactory*)p);
   }
   static void deleteArray_DelphesFactory(void *p) {
      delete [] ((::DelphesFactory*)p);
   }
   static void destruct_DelphesFactory(void *p) {
      typedef ::DelphesFactory current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::DelphesFactory

//______________________________________________________________________________
void SortableObject::Streamer(TBuffer &R__b)
{
   // Stream an object of class SortableObject.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(SortableObject::Class(),this);
   } else {
      R__b.WriteClassBuffer(SortableObject::Class(),this);
   }
}

namespace ROOT {
   // Wrapper around operator delete
   static void delete_SortableObject(void *p) {
      delete ((::SortableObject*)p);
   }
   static void deleteArray_SortableObject(void *p) {
      delete [] ((::SortableObject*)p);
   }
   static void destruct_SortableObject(void *p) {
      typedef ::SortableObject current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::SortableObject

//______________________________________________________________________________
void Event::Streamer(TBuffer &R__b)
{
   // Stream an object of class Event.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(Event::Class(),this);
   } else {
      R__b.WriteClassBuffer(Event::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_Event(void *p) {
      return  p ? new(p) ::Event : new ::Event;
   }
   static void *newArray_Event(Long_t nElements, void *p) {
      return p ? new(p) ::Event[nElements] : new ::Event[nElements];
   }
   // Wrapper around operator delete
   static void delete_Event(void *p) {
      delete ((::Event*)p);
   }
   static void deleteArray_Event(void *p) {
      delete [] ((::Event*)p);
   }
   static void destruct_Event(void *p) {
      typedef ::Event current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::Event

//______________________________________________________________________________
void LHCOEvent::Streamer(TBuffer &R__b)
{
   // Stream an object of class LHCOEvent.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(LHCOEvent::Class(),this);
   } else {
      R__b.WriteClassBuffer(LHCOEvent::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_LHCOEvent(void *p) {
      return  p ? new(p) ::LHCOEvent : new ::LHCOEvent;
   }
   static void *newArray_LHCOEvent(Long_t nElements, void *p) {
      return p ? new(p) ::LHCOEvent[nElements] : new ::LHCOEvent[nElements];
   }
   // Wrapper around operator delete
   static void delete_LHCOEvent(void *p) {
      delete ((::LHCOEvent*)p);
   }
   static void deleteArray_LHCOEvent(void *p) {
      delete [] ((::LHCOEvent*)p);
   }
   static void destruct_LHCOEvent(void *p) {
      typedef ::LHCOEvent current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::LHCOEvent

//______________________________________________________________________________
void LHEFEvent::Streamer(TBuffer &R__b)
{
   // Stream an object of class LHEFEvent.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(LHEFEvent::Class(),this);
   } else {
      R__b.WriteClassBuffer(LHEFEvent::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_LHEFEvent(void *p) {
      return  p ? new(p) ::LHEFEvent : new ::LHEFEvent;
   }
   static void *newArray_LHEFEvent(Long_t nElements, void *p) {
      return p ? new(p) ::LHEFEvent[nElements] : new ::LHEFEvent[nElements];
   }
   // Wrapper around operator delete
   static void delete_LHEFEvent(void *p) {
      delete ((::LHEFEvent*)p);
   }
   static void deleteArray_LHEFEvent(void *p) {
      delete [] ((::LHEFEvent*)p);
   }
   static void destruct_LHEFEvent(void *p) {
      typedef ::LHEFEvent current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::LHEFEvent

//______________________________________________________________________________
void LHEFWeight::Streamer(TBuffer &R__b)
{
   // Stream an object of class LHEFWeight.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(LHEFWeight::Class(),this);
   } else {
      R__b.WriteClassBuffer(LHEFWeight::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_LHEFWeight(void *p) {
      return  p ? new(p) ::LHEFWeight : new ::LHEFWeight;
   }
   static void *newArray_LHEFWeight(Long_t nElements, void *p) {
      return p ? new(p) ::LHEFWeight[nElements] : new ::LHEFWeight[nElements];
   }
   // Wrapper around operator delete
   static void delete_LHEFWeight(void *p) {
      delete ((::LHEFWeight*)p);
   }
   static void deleteArray_LHEFWeight(void *p) {
      delete [] ((::LHEFWeight*)p);
   }
   static void destruct_LHEFWeight(void *p) {
      typedef ::LHEFWeight current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::LHEFWeight

//______________________________________________________________________________
void HepMCEvent::Streamer(TBuffer &R__b)
{
   // Stream an object of class HepMCEvent.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(HepMCEvent::Class(),this);
   } else {
      R__b.WriteClassBuffer(HepMCEvent::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_HepMCEvent(void *p) {
      return  p ? new(p) ::HepMCEvent : new ::HepMCEvent;
   }
   static void *newArray_HepMCEvent(Long_t nElements, void *p) {
      return p ? new(p) ::HepMCEvent[nElements] : new ::HepMCEvent[nElements];
   }
   // Wrapper around operator delete
   static void delete_HepMCEvent(void *p) {
      delete ((::HepMCEvent*)p);
   }
   static void deleteArray_HepMCEvent(void *p) {
      delete [] ((::HepMCEvent*)p);
   }
   static void destruct_HepMCEvent(void *p) {
      typedef ::HepMCEvent current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::HepMCEvent

//______________________________________________________________________________
void GenParticle::Streamer(TBuffer &R__b)
{
   // Stream an object of class GenParticle.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(GenParticle::Class(),this);
   } else {
      R__b.WriteClassBuffer(GenParticle::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_GenParticle(void *p) {
      return  p ? new(p) ::GenParticle : new ::GenParticle;
   }
   static void *newArray_GenParticle(Long_t nElements, void *p) {
      return p ? new(p) ::GenParticle[nElements] : new ::GenParticle[nElements];
   }
   // Wrapper around operator delete
   static void delete_GenParticle(void *p) {
      delete ((::GenParticle*)p);
   }
   static void deleteArray_GenParticle(void *p) {
      delete [] ((::GenParticle*)p);
   }
   static void destruct_GenParticle(void *p) {
      typedef ::GenParticle current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::GenParticle

//______________________________________________________________________________
void Vertex::Streamer(TBuffer &R__b)
{
   // Stream an object of class Vertex.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(Vertex::Class(),this);
   } else {
      R__b.WriteClassBuffer(Vertex::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_Vertex(void *p) {
      return  p ? new(p) ::Vertex : new ::Vertex;
   }
   static void *newArray_Vertex(Long_t nElements, void *p) {
      return p ? new(p) ::Vertex[nElements] : new ::Vertex[nElements];
   }
   // Wrapper around operator delete
   static void delete_Vertex(void *p) {
      delete ((::Vertex*)p);
   }
   static void deleteArray_Vertex(void *p) {
      delete [] ((::Vertex*)p);
   }
   static void destruct_Vertex(void *p) {
      typedef ::Vertex current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::Vertex

//______________________________________________________________________________
void MissingET::Streamer(TBuffer &R__b)
{
   // Stream an object of class MissingET.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(MissingET::Class(),this);
   } else {
      R__b.WriteClassBuffer(MissingET::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_MissingET(void *p) {
      return  p ? new(p) ::MissingET : new ::MissingET;
   }
   static void *newArray_MissingET(Long_t nElements, void *p) {
      return p ? new(p) ::MissingET[nElements] : new ::MissingET[nElements];
   }
   // Wrapper around operator delete
   static void delete_MissingET(void *p) {
      delete ((::MissingET*)p);
   }
   static void deleteArray_MissingET(void *p) {
      delete [] ((::MissingET*)p);
   }
   static void destruct_MissingET(void *p) {
      typedef ::MissingET current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::MissingET

//______________________________________________________________________________
void ScalarHT::Streamer(TBuffer &R__b)
{
   // Stream an object of class ScalarHT.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(ScalarHT::Class(),this);
   } else {
      R__b.WriteClassBuffer(ScalarHT::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_ScalarHT(void *p) {
      return  p ? new(p) ::ScalarHT : new ::ScalarHT;
   }
   static void *newArray_ScalarHT(Long_t nElements, void *p) {
      return p ? new(p) ::ScalarHT[nElements] : new ::ScalarHT[nElements];
   }
   // Wrapper around operator delete
   static void delete_ScalarHT(void *p) {
      delete ((::ScalarHT*)p);
   }
   static void deleteArray_ScalarHT(void *p) {
      delete [] ((::ScalarHT*)p);
   }
   static void destruct_ScalarHT(void *p) {
      typedef ::ScalarHT current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::ScalarHT

//______________________________________________________________________________
void Rho::Streamer(TBuffer &R__b)
{
   // Stream an object of class Rho.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(Rho::Class(),this);
   } else {
      R__b.WriteClassBuffer(Rho::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_Rho(void *p) {
      return  p ? new(p) ::Rho : new ::Rho;
   }
   static void *newArray_Rho(Long_t nElements, void *p) {
      return p ? new(p) ::Rho[nElements] : new ::Rho[nElements];
   }
   // Wrapper around operator delete
   static void delete_Rho(void *p) {
      delete ((::Rho*)p);
   }
   static void deleteArray_Rho(void *p) {
      delete [] ((::Rho*)p);
   }
   static void destruct_Rho(void *p) {
      typedef ::Rho current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::Rho

//______________________________________________________________________________
void Weight::Streamer(TBuffer &R__b)
{
   // Stream an object of class Weight.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(Weight::Class(),this);
   } else {
      R__b.WriteClassBuffer(Weight::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_Weight(void *p) {
      return  p ? new(p) ::Weight : new ::Weight;
   }
   static void *newArray_Weight(Long_t nElements, void *p) {
      return p ? new(p) ::Weight[nElements] : new ::Weight[nElements];
   }
   // Wrapper around operator delete
   static void delete_Weight(void *p) {
      delete ((::Weight*)p);
   }
   static void deleteArray_Weight(void *p) {
      delete [] ((::Weight*)p);
   }
   static void destruct_Weight(void *p) {
      typedef ::Weight current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::Weight

//______________________________________________________________________________
void Photon::Streamer(TBuffer &R__b)
{
   // Stream an object of class Photon.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(Photon::Class(),this);
   } else {
      R__b.WriteClassBuffer(Photon::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_Photon(void *p) {
      return  p ? new(p) ::Photon : new ::Photon;
   }
   static void *newArray_Photon(Long_t nElements, void *p) {
      return p ? new(p) ::Photon[nElements] : new ::Photon[nElements];
   }
   // Wrapper around operator delete
   static void delete_Photon(void *p) {
      delete ((::Photon*)p);
   }
   static void deleteArray_Photon(void *p) {
      delete [] ((::Photon*)p);
   }
   static void destruct_Photon(void *p) {
      typedef ::Photon current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::Photon

//______________________________________________________________________________
void Electron::Streamer(TBuffer &R__b)
{
   // Stream an object of class Electron.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(Electron::Class(),this);
   } else {
      R__b.WriteClassBuffer(Electron::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_Electron(void *p) {
      return  p ? new(p) ::Electron : new ::Electron;
   }
   static void *newArray_Electron(Long_t nElements, void *p) {
      return p ? new(p) ::Electron[nElements] : new ::Electron[nElements];
   }
   // Wrapper around operator delete
   static void delete_Electron(void *p) {
      delete ((::Electron*)p);
   }
   static void deleteArray_Electron(void *p) {
      delete [] ((::Electron*)p);
   }
   static void destruct_Electron(void *p) {
      typedef ::Electron current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::Electron

//______________________________________________________________________________
void Muon::Streamer(TBuffer &R__b)
{
   // Stream an object of class Muon.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(Muon::Class(),this);
   } else {
      R__b.WriteClassBuffer(Muon::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_Muon(void *p) {
      return  p ? new(p) ::Muon : new ::Muon;
   }
   static void *newArray_Muon(Long_t nElements, void *p) {
      return p ? new(p) ::Muon[nElements] : new ::Muon[nElements];
   }
   // Wrapper around operator delete
   static void delete_Muon(void *p) {
      delete ((::Muon*)p);
   }
   static void deleteArray_Muon(void *p) {
      delete [] ((::Muon*)p);
   }
   static void destruct_Muon(void *p) {
      typedef ::Muon current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::Muon

//______________________________________________________________________________
void Jet::Streamer(TBuffer &R__b)
{
   // Stream an object of class Jet.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(Jet::Class(),this);
   } else {
      R__b.WriteClassBuffer(Jet::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_Jet(void *p) {
      return  p ? new(p) ::Jet : new ::Jet;
   }
   static void *newArray_Jet(Long_t nElements, void *p) {
      return p ? new(p) ::Jet[nElements] : new ::Jet[nElements];
   }
   // Wrapper around operator delete
   static void delete_Jet(void *p) {
      delete ((::Jet*)p);
   }
   static void deleteArray_Jet(void *p) {
      delete [] ((::Jet*)p);
   }
   static void destruct_Jet(void *p) {
      typedef ::Jet current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::Jet

//______________________________________________________________________________
void Track::Streamer(TBuffer &R__b)
{
   // Stream an object of class Track.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(Track::Class(),this);
   } else {
      R__b.WriteClassBuffer(Track::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_Track(void *p) {
      return  p ? new(p) ::Track : new ::Track;
   }
   static void *newArray_Track(Long_t nElements, void *p) {
      return p ? new(p) ::Track[nElements] : new ::Track[nElements];
   }
   // Wrapper around operator delete
   static void delete_Track(void *p) {
      delete ((::Track*)p);
   }
   static void deleteArray_Track(void *p) {
      delete [] ((::Track*)p);
   }
   static void destruct_Track(void *p) {
      typedef ::Track current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::Track

//______________________________________________________________________________
void Tower::Streamer(TBuffer &R__b)
{
   // Stream an object of class Tower.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(Tower::Class(),this);
   } else {
      R__b.WriteClassBuffer(Tower::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_Tower(void *p) {
      return  p ? new(p) ::Tower : new ::Tower;
   }
   static void *newArray_Tower(Long_t nElements, void *p) {
      return p ? new(p) ::Tower[nElements] : new ::Tower[nElements];
   }
   // Wrapper around operator delete
   static void delete_Tower(void *p) {
      delete ((::Tower*)p);
   }
   static void deleteArray_Tower(void *p) {
      delete [] ((::Tower*)p);
   }
   static void destruct_Tower(void *p) {
      typedef ::Tower current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::Tower

//______________________________________________________________________________
void ParticleFlowCandidate::Streamer(TBuffer &R__b)
{
   // Stream an object of class ParticleFlowCandidate.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(ParticleFlowCandidate::Class(),this);
   } else {
      R__b.WriteClassBuffer(ParticleFlowCandidate::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_ParticleFlowCandidate(void *p) {
      return  p ? new(p) ::ParticleFlowCandidate : new ::ParticleFlowCandidate;
   }
   static void *newArray_ParticleFlowCandidate(Long_t nElements, void *p) {
      return p ? new(p) ::ParticleFlowCandidate[nElements] : new ::ParticleFlowCandidate[nElements];
   }
   // Wrapper around operator delete
   static void delete_ParticleFlowCandidate(void *p) {
      delete ((::ParticleFlowCandidate*)p);
   }
   static void deleteArray_ParticleFlowCandidate(void *p) {
      delete [] ((::ParticleFlowCandidate*)p);
   }
   static void destruct_ParticleFlowCandidate(void *p) {
      typedef ::ParticleFlowCandidate current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::ParticleFlowCandidate

//______________________________________________________________________________
void HectorHit::Streamer(TBuffer &R__b)
{
   // Stream an object of class HectorHit.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(HectorHit::Class(),this);
   } else {
      R__b.WriteClassBuffer(HectorHit::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_HectorHit(void *p) {
      return  p ? new(p) ::HectorHit : new ::HectorHit;
   }
   static void *newArray_HectorHit(Long_t nElements, void *p) {
      return p ? new(p) ::HectorHit[nElements] : new ::HectorHit[nElements];
   }
   // Wrapper around operator delete
   static void delete_HectorHit(void *p) {
      delete ((::HectorHit*)p);
   }
   static void deleteArray_HectorHit(void *p) {
      delete [] ((::HectorHit*)p);
   }
   static void destruct_HectorHit(void *p) {
      typedef ::HectorHit current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::HectorHit

//______________________________________________________________________________
void Candidate::Streamer(TBuffer &R__b)
{
   // Stream an object of class Candidate.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(Candidate::Class(),this);
   } else {
      R__b.WriteClassBuffer(Candidate::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_Candidate(void *p) {
      return  p ? new(p) ::Candidate : new ::Candidate;
   }
   static void *newArray_Candidate(Long_t nElements, void *p) {
      return p ? new(p) ::Candidate[nElements] : new ::Candidate[nElements];
   }
   // Wrapper around operator delete
   static void delete_Candidate(void *p) {
      delete ((::Candidate*)p);
   }
   static void deleteArray_Candidate(void *p) {
      delete [] ((::Candidate*)p);
   }
   static void destruct_Candidate(void *p) {
      typedef ::Candidate current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::Candidate

namespace ROOT {
   static TClass *vectorlEpairlEfloatcOfloatgRsPgR_Dictionary();
   static void vectorlEpairlEfloatcOfloatgRsPgR_TClassManip(TClass*);
   static void *new_vectorlEpairlEfloatcOfloatgRsPgR(void *p = 0);
   static void *newArray_vectorlEpairlEfloatcOfloatgRsPgR(Long_t size, void *p);
   static void delete_vectorlEpairlEfloatcOfloatgRsPgR(void *p);
   static void deleteArray_vectorlEpairlEfloatcOfloatgRsPgR(void *p);
   static void destruct_vectorlEpairlEfloatcOfloatgRsPgR(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const vector<pair<float,float> >*)
   {
      vector<pair<float,float> > *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(vector<pair<float,float> >));
      static ::ROOT::TGenericClassInfo 
         instance("vector<pair<float,float> >", -2, "vector", 216,
                  typeid(vector<pair<float,float> >), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &vectorlEpairlEfloatcOfloatgRsPgR_Dictionary, isa_proxy, 0,
                  sizeof(vector<pair<float,float> >) );
      instance.SetNew(&new_vectorlEpairlEfloatcOfloatgRsPgR);
      instance.SetNewArray(&newArray_vectorlEpairlEfloatcOfloatgRsPgR);
      instance.SetDelete(&delete_vectorlEpairlEfloatcOfloatgRsPgR);
      instance.SetDeleteArray(&deleteArray_vectorlEpairlEfloatcOfloatgRsPgR);
      instance.SetDestructor(&destruct_vectorlEpairlEfloatcOfloatgRsPgR);
      instance.AdoptCollectionProxyInfo(TCollectionProxyInfo::Generate(TCollectionProxyInfo::Pushback< vector<pair<float,float> > >()));
      return &instance;
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const vector<pair<float,float> >*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *vectorlEpairlEfloatcOfloatgRsPgR_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const vector<pair<float,float> >*)0x0)->GetClass();
      vectorlEpairlEfloatcOfloatgRsPgR_TClassManip(theClass);
   return theClass;
   }

   static void vectorlEpairlEfloatcOfloatgRsPgR_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   // Wrappers around operator new
   static void *new_vectorlEpairlEfloatcOfloatgRsPgR(void *p) {
      return  p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) vector<pair<float,float> > : new vector<pair<float,float> >;
   }
   static void *newArray_vectorlEpairlEfloatcOfloatgRsPgR(Long_t nElements, void *p) {
      return p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) vector<pair<float,float> >[nElements] : new vector<pair<float,float> >[nElements];
   }
   // Wrapper around operator delete
   static void delete_vectorlEpairlEfloatcOfloatgRsPgR(void *p) {
      delete ((vector<pair<float,float> >*)p);
   }
   static void deleteArray_vectorlEpairlEfloatcOfloatgRsPgR(void *p) {
      delete [] ((vector<pair<float,float> >*)p);
   }
   static void destruct_vectorlEpairlEfloatcOfloatgRsPgR(void *p) {
      typedef vector<pair<float,float> > current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class vector<pair<float,float> >

namespace {
  void TriggerDictionaryInitialization_ClassesDict_Impl() {
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
#line 1 "ClassesDict dictionary forward declarations' payload"
#pragma clang diagnostic ignored "-Wkeyword-compat"
#pragma clang diagnostic ignored "-Wignored-attributes"
#pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
extern int __Cling_Autoloading_Map;
class __attribute__((annotate("$clingAutoload$classes/DelphesModule.h")))  DelphesModule;
class __attribute__((annotate("$clingAutoload$classes/DelphesFactory.h")))  DelphesFactory;
class __attribute__((annotate("$clingAutoload$classes/SortableObject.h")))  SortableObject;
class __attribute__((annotate("$clingAutoload$classes/DelphesClasses.h")))  Event;
class __attribute__((annotate("$clingAutoload$classes/DelphesClasses.h")))  LHCOEvent;
class __attribute__((annotate("$clingAutoload$classes/DelphesClasses.h")))  LHEFEvent;
class __attribute__((annotate("$clingAutoload$classes/DelphesClasses.h")))  LHEFWeight;
class __attribute__((annotate("$clingAutoload$classes/DelphesClasses.h")))  HepMCEvent;
class __attribute__((annotate("$clingAutoload$classes/DelphesClasses.h")))  GenParticle;
class __attribute__((annotate("$clingAutoload$classes/DelphesClasses.h")))  Vertex;
class __attribute__((annotate("$clingAutoload$classes/DelphesClasses.h")))  MissingET;
class __attribute__((annotate("$clingAutoload$classes/DelphesClasses.h")))  ScalarHT;
class __attribute__((annotate("$clingAutoload$classes/DelphesClasses.h")))  Rho;
class __attribute__((annotate("$clingAutoload$classes/DelphesClasses.h")))  Weight;
class __attribute__((annotate("$clingAutoload$classes/DelphesClasses.h")))  Photon;
class __attribute__((annotate("$clingAutoload$classes/DelphesClasses.h")))  Electron;
class __attribute__((annotate("$clingAutoload$classes/DelphesClasses.h")))  Muon;
class __attribute__((annotate("$clingAutoload$classes/DelphesClasses.h")))  Jet;
class __attribute__((annotate("$clingAutoload$classes/DelphesClasses.h")))  Track;
class __attribute__((annotate("$clingAutoload$classes/DelphesClasses.h")))  Tower;
class __attribute__((annotate("$clingAutoload$classes/DelphesClasses.h")))  ParticleFlowCandidate;
class __attribute__((annotate("$clingAutoload$classes/DelphesClasses.h")))  HectorHit;
class __attribute__((annotate("$clingAutoload$classes/DelphesClasses.h")))  Candidate;
)DICTFWDDCLS";
    static const char* payloadCode = R"DICTPAYLOAD(
#line 1 "ClassesDict dictionary payload"

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


/** ExRootAnalysisLinkDef
 *
 *  Lists classes to be included in cint dicitonary
 *
 *  \author P. Demin - UCL, Louvain-la-Neuve
 *
 */

#include "classes/DelphesModule.h"
#include "classes/DelphesFactory.h"

#include "classes/SortableObject.h"
#include "classes/DelphesClasses.h"

#ifdef __CINT__

#pragma link off all globals;
#pragma link off all classes;
#pragma link off all functions;

#pragma link C++ class DelphesModule+;
#pragma link C++ class DelphesFactory+;

#pragma link C++ class SortableObject+;

#pragma link C++ class Event+;
#pragma link C++ class LHCOEvent+;
#pragma link C++ class LHEFEvent+;
#pragma link C++ class LHEFWeight+;
#pragma link C++ class HepMCEvent+;
#pragma link C++ class GenParticle+;
#pragma link C++ class Vertex+;
#pragma link C++ class MissingET+;
#pragma link C++ class ScalarHT+;
#pragma link C++ class Rho+;
#pragma link C++ class Weight+;
#pragma link C++ class Photon+;
#pragma link C++ class Electron+;
#pragma link C++ class Muon+;
#pragma link C++ class Jet+;
#pragma link C++ class Track+;
#pragma link C++ class Tower+;
#pragma link C++ class ParticleFlowCandidate+;
#pragma link C++ class HectorHit+;

#pragma link C++ class Candidate+;

#endif


#undef  _BACKWARD_BACKWARD_WARNING_H
)DICTPAYLOAD";
    static const char* classesHeaders[]={
"Candidate", payloadCode, "@",
"DelphesFactory", payloadCode, "@",
"DelphesModule", payloadCode, "@",
"Electron", payloadCode, "@",
"Event", payloadCode, "@",
"GenParticle", payloadCode, "@",
"HectorHit", payloadCode, "@",
"HepMCEvent", payloadCode, "@",
"Jet", payloadCode, "@",
"LHCOEvent", payloadCode, "@",
"LHEFEvent", payloadCode, "@",
"LHEFWeight", payloadCode, "@",
"MissingET", payloadCode, "@",
"Muon", payloadCode, "@",
"ParticleFlowCandidate", payloadCode, "@",
"Photon", payloadCode, "@",
"Rho", payloadCode, "@",
"ScalarHT", payloadCode, "@",
"SortableObject", payloadCode, "@",
"Tower", payloadCode, "@",
"Track", payloadCode, "@",
"Vertex", payloadCode, "@",
"Weight", payloadCode, "@",
nullptr};

    static bool isInitialized = false;
    if (!isInitialized) {
      TROOT::RegisterModule("ClassesDict",
        headers, includePaths, payloadCode, fwdDeclCode,
        TriggerDictionaryInitialization_ClassesDict_Impl, {}, classesHeaders, /*has no C++ module*/false);
      isInitialized = true;
    }
  }
  static struct DictInit {
    DictInit() {
      TriggerDictionaryInitialization_ClassesDict_Impl();
    }
  } __TheDictionaryInitializer;
}
void TriggerDictionaryInitialization_ClassesDict() {
  TriggerDictionaryInitialization_ClassesDict_Impl();
}
