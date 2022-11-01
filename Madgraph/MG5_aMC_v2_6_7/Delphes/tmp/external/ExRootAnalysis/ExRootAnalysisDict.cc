
/** \class ExRootAnalysisLinkDef
 *
 *  Lists classes to be included in cint dicitonary
 *
 *  \author P. Demin - UCL, Louvain-la-Neuve
 *
 */

#include "ExRootAnalysis/ExRootTreeReader.h"
#include "ExRootAnalysis/ExRootTreeWriter.h"
#include "ExRootAnalysis/ExRootTreeBranch.h"
#include "ExRootAnalysis/ExRootResult.h"
#include "ExRootAnalysis/ExRootUtilities.h"
#include "ExRootAnalysis/ExRootClassifier.h"
#include "ExRootAnalysis/ExRootFilter.h"

#include "ExRootAnalysis/ExRootProgressBar.h"
#include "ExRootAnalysis/ExRootConfReader.h"
#include "ExRootAnalysis/ExRootTask.h"

#ifdef __CINT__

#pragma link off all globals;
#pragma link off all classes;
#pragma link off all functions;

#pragma link C++ class ExRootTreeReader+;
#pragma link C++ class ExRootTreeBranch+;
#pragma link C++ class ExRootTreeWriter+;
#pragma link C++ class ExRootResult+;
#pragma link C++ class ExRootClassifier+;
#pragma link C++ class ExRootFilter+;

#pragma link C++ class ExRootProgressBar+;
#pragma link C++ class ExRootConfReader+;
#pragma link C++ class ExRootConfParam+;
#pragma link C++ class ExRootTask+;

#pragma link C++ function HistStyle;
#pragma link C++ function FillChain;

#endif

// Do NOT change. Changes will be lost next time file is generated

#define R__DICTIONARY_FILENAME tmpdIexternaldIExRootAnalysisdIExRootAnalysisDict

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
#include "ExRootAnalysis/ExRootTreeReader.h"
#include "ExRootAnalysis/ExRootTreeWriter.h"
#include "ExRootAnalysis/ExRootTreeBranch.h"
#include "ExRootAnalysis/ExRootResult.h"
#include "ExRootAnalysis/ExRootUtilities.h"
#include "ExRootAnalysis/ExRootClassifier.h"
#include "ExRootAnalysis/ExRootFilter.h"
#include "ExRootAnalysis/ExRootProgressBar.h"
#include "ExRootAnalysis/ExRootConfReader.h"
#include "ExRootAnalysis/ExRootTask.h"

// Header files passed via #pragma extra_include

namespace ROOT {
   static void *new_ExRootTreeReader(void *p = 0);
   static void *newArray_ExRootTreeReader(Long_t size, void *p);
   static void delete_ExRootTreeReader(void *p);
   static void deleteArray_ExRootTreeReader(void *p);
   static void destruct_ExRootTreeReader(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::ExRootTreeReader*)
   {
      ::ExRootTreeReader *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::ExRootTreeReader >(0);
      static ::ROOT::TGenericClassInfo 
         instance("ExRootTreeReader", ::ExRootTreeReader::Class_Version(), "ExRootAnalysis/ExRootTreeReader.h", 19,
                  typeid(::ExRootTreeReader), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::ExRootTreeReader::Dictionary, isa_proxy, 4,
                  sizeof(::ExRootTreeReader) );
      instance.SetNew(&new_ExRootTreeReader);
      instance.SetNewArray(&newArray_ExRootTreeReader);
      instance.SetDelete(&delete_ExRootTreeReader);
      instance.SetDeleteArray(&deleteArray_ExRootTreeReader);
      instance.SetDestructor(&destruct_ExRootTreeReader);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::ExRootTreeReader*)
   {
      return GenerateInitInstanceLocal((::ExRootTreeReader*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::ExRootTreeReader*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_ExRootTreeWriter(void *p = 0);
   static void *newArray_ExRootTreeWriter(Long_t size, void *p);
   static void delete_ExRootTreeWriter(void *p);
   static void deleteArray_ExRootTreeWriter(void *p);
   static void destruct_ExRootTreeWriter(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::ExRootTreeWriter*)
   {
      ::ExRootTreeWriter *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::ExRootTreeWriter >(0);
      static ::ROOT::TGenericClassInfo 
         instance("ExRootTreeWriter", ::ExRootTreeWriter::Class_Version(), "ExRootAnalysis/ExRootTreeWriter.h", 21,
                  typeid(::ExRootTreeWriter), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::ExRootTreeWriter::Dictionary, isa_proxy, 4,
                  sizeof(::ExRootTreeWriter) );
      instance.SetNew(&new_ExRootTreeWriter);
      instance.SetNewArray(&newArray_ExRootTreeWriter);
      instance.SetDelete(&delete_ExRootTreeWriter);
      instance.SetDeleteArray(&deleteArray_ExRootTreeWriter);
      instance.SetDestructor(&destruct_ExRootTreeWriter);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::ExRootTreeWriter*)
   {
      return GenerateInitInstanceLocal((::ExRootTreeWriter*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::ExRootTreeWriter*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static TClass *ExRootTreeBranch_Dictionary();
   static void ExRootTreeBranch_TClassManip(TClass*);
   static void delete_ExRootTreeBranch(void *p);
   static void deleteArray_ExRootTreeBranch(void *p);
   static void destruct_ExRootTreeBranch(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::ExRootTreeBranch*)
   {
      ::ExRootTreeBranch *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(::ExRootTreeBranch));
      static ::ROOT::TGenericClassInfo 
         instance("ExRootTreeBranch", "ExRootAnalysis/ExRootTreeBranch.h", 18,
                  typeid(::ExRootTreeBranch), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &ExRootTreeBranch_Dictionary, isa_proxy, 4,
                  sizeof(::ExRootTreeBranch) );
      instance.SetDelete(&delete_ExRootTreeBranch);
      instance.SetDeleteArray(&deleteArray_ExRootTreeBranch);
      instance.SetDestructor(&destruct_ExRootTreeBranch);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::ExRootTreeBranch*)
   {
      return GenerateInitInstanceLocal((::ExRootTreeBranch*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::ExRootTreeBranch*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *ExRootTreeBranch_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const ::ExRootTreeBranch*)0x0)->GetClass();
      ExRootTreeBranch_TClassManip(theClass);
   return theClass;
   }

   static void ExRootTreeBranch_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   static TClass *ExRootResult_Dictionary();
   static void ExRootResult_TClassManip(TClass*);
   static void *new_ExRootResult(void *p = 0);
   static void *newArray_ExRootResult(Long_t size, void *p);
   static void delete_ExRootResult(void *p);
   static void deleteArray_ExRootResult(void *p);
   static void destruct_ExRootResult(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::ExRootResult*)
   {
      ::ExRootResult *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(::ExRootResult));
      static ::ROOT::TGenericClassInfo 
         instance("ExRootResult", "ExRootAnalysis/ExRootResult.h", 21,
                  typeid(::ExRootResult), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &ExRootResult_Dictionary, isa_proxy, 4,
                  sizeof(::ExRootResult) );
      instance.SetNew(&new_ExRootResult);
      instance.SetNewArray(&newArray_ExRootResult);
      instance.SetDelete(&delete_ExRootResult);
      instance.SetDeleteArray(&deleteArray_ExRootResult);
      instance.SetDestructor(&destruct_ExRootResult);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::ExRootResult*)
   {
      return GenerateInitInstanceLocal((::ExRootResult*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::ExRootResult*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *ExRootResult_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const ::ExRootResult*)0x0)->GetClass();
      ExRootResult_TClassManip(theClass);
   return theClass;
   }

   static void ExRootResult_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   static TClass *ExRootClassifier_Dictionary();
   static void ExRootClassifier_TClassManip(TClass*);
   static void delete_ExRootClassifier(void *p);
   static void deleteArray_ExRootClassifier(void *p);
   static void destruct_ExRootClassifier(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::ExRootClassifier*)
   {
      ::ExRootClassifier *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(::ExRootClassifier));
      static ::ROOT::TGenericClassInfo 
         instance("ExRootClassifier", "ExRootAnalysis/ExRootClassifier.h", 8,
                  typeid(::ExRootClassifier), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &ExRootClassifier_Dictionary, isa_proxy, 4,
                  sizeof(::ExRootClassifier) );
      instance.SetDelete(&delete_ExRootClassifier);
      instance.SetDeleteArray(&deleteArray_ExRootClassifier);
      instance.SetDestructor(&destruct_ExRootClassifier);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::ExRootClassifier*)
   {
      return GenerateInitInstanceLocal((::ExRootClassifier*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::ExRootClassifier*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *ExRootClassifier_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const ::ExRootClassifier*)0x0)->GetClass();
      ExRootClassifier_TClassManip(theClass);
   return theClass;
   }

   static void ExRootClassifier_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   static TClass *ExRootFilter_Dictionary();
   static void ExRootFilter_TClassManip(TClass*);
   static void delete_ExRootFilter(void *p);
   static void deleteArray_ExRootFilter(void *p);
   static void destruct_ExRootFilter(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::ExRootFilter*)
   {
      ::ExRootFilter *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(::ExRootFilter));
      static ::ROOT::TGenericClassInfo 
         instance("ExRootFilter", "ExRootAnalysis/ExRootFilter.h", 13,
                  typeid(::ExRootFilter), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &ExRootFilter_Dictionary, isa_proxy, 4,
                  sizeof(::ExRootFilter) );
      instance.SetDelete(&delete_ExRootFilter);
      instance.SetDeleteArray(&deleteArray_ExRootFilter);
      instance.SetDestructor(&destruct_ExRootFilter);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::ExRootFilter*)
   {
      return GenerateInitInstanceLocal((::ExRootFilter*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::ExRootFilter*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *ExRootFilter_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const ::ExRootFilter*)0x0)->GetClass();
      ExRootFilter_TClassManip(theClass);
   return theClass;
   }

   static void ExRootFilter_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   static TClass *ExRootProgressBar_Dictionary();
   static void ExRootProgressBar_TClassManip(TClass*);
   static void delete_ExRootProgressBar(void *p);
   static void deleteArray_ExRootProgressBar(void *p);
   static void destruct_ExRootProgressBar(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::ExRootProgressBar*)
   {
      ::ExRootProgressBar *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(::ExRootProgressBar));
      static ::ROOT::TGenericClassInfo 
         instance("ExRootProgressBar", "ExRootAnalysis/ExRootProgressBar.h", 6,
                  typeid(::ExRootProgressBar), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &ExRootProgressBar_Dictionary, isa_proxy, 4,
                  sizeof(::ExRootProgressBar) );
      instance.SetDelete(&delete_ExRootProgressBar);
      instance.SetDeleteArray(&deleteArray_ExRootProgressBar);
      instance.SetDestructor(&destruct_ExRootProgressBar);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::ExRootProgressBar*)
   {
      return GenerateInitInstanceLocal((::ExRootProgressBar*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::ExRootProgressBar*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *ExRootProgressBar_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const ::ExRootProgressBar*)0x0)->GetClass();
      ExRootProgressBar_TClassManip(theClass);
   return theClass;
   }

   static void ExRootProgressBar_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   static TClass *ExRootConfParam_Dictionary();
   static void ExRootConfParam_TClassManip(TClass*);
   static void *new_ExRootConfParam(void *p = 0);
   static void *newArray_ExRootConfParam(Long_t size, void *p);
   static void delete_ExRootConfParam(void *p);
   static void deleteArray_ExRootConfParam(void *p);
   static void destruct_ExRootConfParam(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::ExRootConfParam*)
   {
      ::ExRootConfParam *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(::ExRootConfParam));
      static ::ROOT::TGenericClassInfo 
         instance("ExRootConfParam", "ExRootAnalysis/ExRootConfReader.h", 20,
                  typeid(::ExRootConfParam), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &ExRootConfParam_Dictionary, isa_proxy, 4,
                  sizeof(::ExRootConfParam) );
      instance.SetNew(&new_ExRootConfParam);
      instance.SetNewArray(&newArray_ExRootConfParam);
      instance.SetDelete(&delete_ExRootConfParam);
      instance.SetDeleteArray(&deleteArray_ExRootConfParam);
      instance.SetDestructor(&destruct_ExRootConfParam);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::ExRootConfParam*)
   {
      return GenerateInitInstanceLocal((::ExRootConfParam*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::ExRootConfParam*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *ExRootConfParam_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const ::ExRootConfParam*)0x0)->GetClass();
      ExRootConfParam_TClassManip(theClass);
   return theClass;
   }

   static void ExRootConfParam_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   static void *new_ExRootConfReader(void *p = 0);
   static void *newArray_ExRootConfReader(Long_t size, void *p);
   static void delete_ExRootConfReader(void *p);
   static void deleteArray_ExRootConfReader(void *p);
   static void destruct_ExRootConfReader(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::ExRootConfReader*)
   {
      ::ExRootConfReader *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::ExRootConfReader >(0);
      static ::ROOT::TGenericClassInfo 
         instance("ExRootConfReader", ::ExRootConfReader::Class_Version(), "ExRootAnalysis/ExRootConfReader.h", 42,
                  typeid(::ExRootConfReader), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::ExRootConfReader::Dictionary, isa_proxy, 4,
                  sizeof(::ExRootConfReader) );
      instance.SetNew(&new_ExRootConfReader);
      instance.SetNewArray(&newArray_ExRootConfReader);
      instance.SetDelete(&delete_ExRootConfReader);
      instance.SetDeleteArray(&deleteArray_ExRootConfReader);
      instance.SetDestructor(&destruct_ExRootConfReader);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::ExRootConfReader*)
   {
      return GenerateInitInstanceLocal((::ExRootConfReader*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::ExRootConfReader*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_ExRootTask(void *p = 0);
   static void *newArray_ExRootTask(Long_t size, void *p);
   static void delete_ExRootTask(void *p);
   static void deleteArray_ExRootTask(void *p);
   static void destruct_ExRootTask(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::ExRootTask*)
   {
      ::ExRootTask *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::ExRootTask >(0);
      static ::ROOT::TGenericClassInfo 
         instance("ExRootTask", ::ExRootTask::Class_Version(), "ExRootAnalysis/ExRootTask.h", 19,
                  typeid(::ExRootTask), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::ExRootTask::Dictionary, isa_proxy, 4,
                  sizeof(::ExRootTask) );
      instance.SetNew(&new_ExRootTask);
      instance.SetNewArray(&newArray_ExRootTask);
      instance.SetDelete(&delete_ExRootTask);
      instance.SetDeleteArray(&deleteArray_ExRootTask);
      instance.SetDestructor(&destruct_ExRootTask);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::ExRootTask*)
   {
      return GenerateInitInstanceLocal((::ExRootTask*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::ExRootTask*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

//______________________________________________________________________________
atomic_TClass_ptr ExRootTreeReader::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *ExRootTreeReader::Class_Name()
{
   return "ExRootTreeReader";
}

//______________________________________________________________________________
const char *ExRootTreeReader::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::ExRootTreeReader*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int ExRootTreeReader::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::ExRootTreeReader*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *ExRootTreeReader::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::ExRootTreeReader*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *ExRootTreeReader::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::ExRootTreeReader*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr ExRootTreeWriter::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *ExRootTreeWriter::Class_Name()
{
   return "ExRootTreeWriter";
}

//______________________________________________________________________________
const char *ExRootTreeWriter::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::ExRootTreeWriter*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int ExRootTreeWriter::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::ExRootTreeWriter*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *ExRootTreeWriter::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::ExRootTreeWriter*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *ExRootTreeWriter::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::ExRootTreeWriter*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr ExRootConfReader::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *ExRootConfReader::Class_Name()
{
   return "ExRootConfReader";
}

//______________________________________________________________________________
const char *ExRootConfReader::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::ExRootConfReader*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int ExRootConfReader::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::ExRootConfReader*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *ExRootConfReader::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::ExRootConfReader*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *ExRootConfReader::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::ExRootConfReader*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr ExRootTask::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *ExRootTask::Class_Name()
{
   return "ExRootTask";
}

//______________________________________________________________________________
const char *ExRootTask::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::ExRootTask*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int ExRootTask::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::ExRootTask*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *ExRootTask::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::ExRootTask*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *ExRootTask::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::ExRootTask*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
void ExRootTreeReader::Streamer(TBuffer &R__b)
{
   // Stream an object of class ExRootTreeReader.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(ExRootTreeReader::Class(),this);
   } else {
      R__b.WriteClassBuffer(ExRootTreeReader::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_ExRootTreeReader(void *p) {
      return  p ? new(p) ::ExRootTreeReader : new ::ExRootTreeReader;
   }
   static void *newArray_ExRootTreeReader(Long_t nElements, void *p) {
      return p ? new(p) ::ExRootTreeReader[nElements] : new ::ExRootTreeReader[nElements];
   }
   // Wrapper around operator delete
   static void delete_ExRootTreeReader(void *p) {
      delete ((::ExRootTreeReader*)p);
   }
   static void deleteArray_ExRootTreeReader(void *p) {
      delete [] ((::ExRootTreeReader*)p);
   }
   static void destruct_ExRootTreeReader(void *p) {
      typedef ::ExRootTreeReader current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::ExRootTreeReader

//______________________________________________________________________________
void ExRootTreeWriter::Streamer(TBuffer &R__b)
{
   // Stream an object of class ExRootTreeWriter.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(ExRootTreeWriter::Class(),this);
   } else {
      R__b.WriteClassBuffer(ExRootTreeWriter::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_ExRootTreeWriter(void *p) {
      return  p ? new(p) ::ExRootTreeWriter : new ::ExRootTreeWriter;
   }
   static void *newArray_ExRootTreeWriter(Long_t nElements, void *p) {
      return p ? new(p) ::ExRootTreeWriter[nElements] : new ::ExRootTreeWriter[nElements];
   }
   // Wrapper around operator delete
   static void delete_ExRootTreeWriter(void *p) {
      delete ((::ExRootTreeWriter*)p);
   }
   static void deleteArray_ExRootTreeWriter(void *p) {
      delete [] ((::ExRootTreeWriter*)p);
   }
   static void destruct_ExRootTreeWriter(void *p) {
      typedef ::ExRootTreeWriter current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::ExRootTreeWriter

namespace ROOT {
   // Wrapper around operator delete
   static void delete_ExRootTreeBranch(void *p) {
      delete ((::ExRootTreeBranch*)p);
   }
   static void deleteArray_ExRootTreeBranch(void *p) {
      delete [] ((::ExRootTreeBranch*)p);
   }
   static void destruct_ExRootTreeBranch(void *p) {
      typedef ::ExRootTreeBranch current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::ExRootTreeBranch

namespace ROOT {
   // Wrappers around operator new
   static void *new_ExRootResult(void *p) {
      return  p ? new(p) ::ExRootResult : new ::ExRootResult;
   }
   static void *newArray_ExRootResult(Long_t nElements, void *p) {
      return p ? new(p) ::ExRootResult[nElements] : new ::ExRootResult[nElements];
   }
   // Wrapper around operator delete
   static void delete_ExRootResult(void *p) {
      delete ((::ExRootResult*)p);
   }
   static void deleteArray_ExRootResult(void *p) {
      delete [] ((::ExRootResult*)p);
   }
   static void destruct_ExRootResult(void *p) {
      typedef ::ExRootResult current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::ExRootResult

namespace ROOT {
   // Wrapper around operator delete
   static void delete_ExRootClassifier(void *p) {
      delete ((::ExRootClassifier*)p);
   }
   static void deleteArray_ExRootClassifier(void *p) {
      delete [] ((::ExRootClassifier*)p);
   }
   static void destruct_ExRootClassifier(void *p) {
      typedef ::ExRootClassifier current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::ExRootClassifier

namespace ROOT {
   // Wrapper around operator delete
   static void delete_ExRootFilter(void *p) {
      delete ((::ExRootFilter*)p);
   }
   static void deleteArray_ExRootFilter(void *p) {
      delete [] ((::ExRootFilter*)p);
   }
   static void destruct_ExRootFilter(void *p) {
      typedef ::ExRootFilter current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::ExRootFilter

namespace ROOT {
   // Wrapper around operator delete
   static void delete_ExRootProgressBar(void *p) {
      delete ((::ExRootProgressBar*)p);
   }
   static void deleteArray_ExRootProgressBar(void *p) {
      delete [] ((::ExRootProgressBar*)p);
   }
   static void destruct_ExRootProgressBar(void *p) {
      typedef ::ExRootProgressBar current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::ExRootProgressBar

namespace ROOT {
   // Wrappers around operator new
   static void *new_ExRootConfParam(void *p) {
      return  p ? new(p) ::ExRootConfParam : new ::ExRootConfParam;
   }
   static void *newArray_ExRootConfParam(Long_t nElements, void *p) {
      return p ? new(p) ::ExRootConfParam[nElements] : new ::ExRootConfParam[nElements];
   }
   // Wrapper around operator delete
   static void delete_ExRootConfParam(void *p) {
      delete ((::ExRootConfParam*)p);
   }
   static void deleteArray_ExRootConfParam(void *p) {
      delete [] ((::ExRootConfParam*)p);
   }
   static void destruct_ExRootConfParam(void *p) {
      typedef ::ExRootConfParam current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::ExRootConfParam

//______________________________________________________________________________
void ExRootConfReader::Streamer(TBuffer &R__b)
{
   // Stream an object of class ExRootConfReader.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(ExRootConfReader::Class(),this);
   } else {
      R__b.WriteClassBuffer(ExRootConfReader::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_ExRootConfReader(void *p) {
      return  p ? new(p) ::ExRootConfReader : new ::ExRootConfReader;
   }
   static void *newArray_ExRootConfReader(Long_t nElements, void *p) {
      return p ? new(p) ::ExRootConfReader[nElements] : new ::ExRootConfReader[nElements];
   }
   // Wrapper around operator delete
   static void delete_ExRootConfReader(void *p) {
      delete ((::ExRootConfReader*)p);
   }
   static void deleteArray_ExRootConfReader(void *p) {
      delete [] ((::ExRootConfReader*)p);
   }
   static void destruct_ExRootConfReader(void *p) {
      typedef ::ExRootConfReader current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::ExRootConfReader

//______________________________________________________________________________
void ExRootTask::Streamer(TBuffer &R__b)
{
   // Stream an object of class ExRootTask.

   if (R__b.IsReading()) {
      R__b.ReadClassBuffer(ExRootTask::Class(),this);
   } else {
      R__b.WriteClassBuffer(ExRootTask::Class(),this);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_ExRootTask(void *p) {
      return  p ? new(p) ::ExRootTask : new ::ExRootTask;
   }
   static void *newArray_ExRootTask(Long_t nElements, void *p) {
      return p ? new(p) ::ExRootTask[nElements] : new ::ExRootTask[nElements];
   }
   // Wrapper around operator delete
   static void delete_ExRootTask(void *p) {
      delete ((::ExRootTask*)p);
   }
   static void deleteArray_ExRootTask(void *p) {
      delete [] ((::ExRootTask*)p);
   }
   static void destruct_ExRootTask(void *p) {
      typedef ::ExRootTask current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::ExRootTask

namespace {
  void TriggerDictionaryInitialization_ExRootAnalysisDict_Impl() {
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
#line 1 "ExRootAnalysisDict dictionary forward declarations' payload"
#pragma clang diagnostic ignored "-Wkeyword-compat"
#pragma clang diagnostic ignored "-Wignored-attributes"
#pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
extern int __Cling_Autoloading_Map;
class __attribute__((annotate("$clingAutoload$ExRootAnalysis/ExRootTreeReader.h")))  ExRootTreeReader;
class __attribute__((annotate("$clingAutoload$ExRootAnalysis/ExRootTreeWriter.h")))  ExRootTreeWriter;
class __attribute__((annotate("$clingAutoload$ExRootAnalysis/ExRootTreeBranch.h")))  ExRootTreeBranch;
class __attribute__((annotate("$clingAutoload$ExRootAnalysis/ExRootResult.h")))  ExRootResult;
class __attribute__((annotate("$clingAutoload$ExRootAnalysis/ExRootClassifier.h")))  ExRootClassifier;
class __attribute__((annotate("$clingAutoload$ExRootAnalysis/ExRootFilter.h")))  ExRootFilter;
class __attribute__((annotate("$clingAutoload$ExRootAnalysis/ExRootProgressBar.h")))  ExRootProgressBar;
class __attribute__((annotate("$clingAutoload$ExRootAnalysis/ExRootConfReader.h")))  ExRootConfParam;
class __attribute__((annotate("$clingAutoload$ExRootAnalysis/ExRootConfReader.h")))  ExRootConfReader;
class __attribute__((annotate("$clingAutoload$ExRootAnalysis/ExRootTask.h")))  ExRootTask;
)DICTFWDDCLS";
    static const char* payloadCode = R"DICTPAYLOAD(
#line 1 "ExRootAnalysisDict dictionary payload"

#ifndef G__VECTOR_HAS_CLASS_ITERATOR
  #define G__VECTOR_HAS_CLASS_ITERATOR 1
#endif

#define _BACKWARD_BACKWARD_WARNING_H

/** \class ExRootAnalysisLinkDef
 *
 *  Lists classes to be included in cint dicitonary
 *
 *  \author P. Demin - UCL, Louvain-la-Neuve
 *
 */

#include "ExRootAnalysis/ExRootTreeReader.h"
#include "ExRootAnalysis/ExRootTreeWriter.h"
#include "ExRootAnalysis/ExRootTreeBranch.h"
#include "ExRootAnalysis/ExRootResult.h"
#include "ExRootAnalysis/ExRootUtilities.h"
#include "ExRootAnalysis/ExRootClassifier.h"
#include "ExRootAnalysis/ExRootFilter.h"

#include "ExRootAnalysis/ExRootProgressBar.h"
#include "ExRootAnalysis/ExRootConfReader.h"
#include "ExRootAnalysis/ExRootTask.h"

#ifdef __CINT__

#pragma link off all globals;
#pragma link off all classes;
#pragma link off all functions;

#pragma link C++ class ExRootTreeReader+;
#pragma link C++ class ExRootTreeBranch+;
#pragma link C++ class ExRootTreeWriter+;
#pragma link C++ class ExRootResult+;
#pragma link C++ class ExRootClassifier+;
#pragma link C++ class ExRootFilter+;

#pragma link C++ class ExRootProgressBar+;
#pragma link C++ class ExRootConfReader+;
#pragma link C++ class ExRootConfParam+;
#pragma link C++ class ExRootTask+;

#pragma link C++ function HistStyle;
#pragma link C++ function FillChain;

#endif


#undef  _BACKWARD_BACKWARD_WARNING_H
)DICTPAYLOAD";
    static const char* classesHeaders[]={
"ExRootClassifier", payloadCode, "@",
"ExRootConfParam", payloadCode, "@",
"ExRootConfReader", payloadCode, "@",
"ExRootFilter", payloadCode, "@",
"ExRootProgressBar", payloadCode, "@",
"ExRootResult", payloadCode, "@",
"ExRootTask", payloadCode, "@",
"ExRootTreeBranch", payloadCode, "@",
"ExRootTreeReader", payloadCode, "@",
"ExRootTreeWriter", payloadCode, "@",
"FillChain", payloadCode, "@",
"HistStyle", payloadCode, "@",
nullptr};

    static bool isInitialized = false;
    if (!isInitialized) {
      TROOT::RegisterModule("ExRootAnalysisDict",
        headers, includePaths, payloadCode, fwdDeclCode,
        TriggerDictionaryInitialization_ExRootAnalysisDict_Impl, {}, classesHeaders, /*has no C++ module*/false);
      isInitialized = true;
    }
  }
  static struct DictInit {
    DictInit() {
      TriggerDictionaryInitialization_ExRootAnalysisDict_Impl();
    }
  } __TheDictionaryInitializer;
}
void TriggerDictionaryInitialization_ExRootAnalysisDict() {
  TriggerDictionaryInitialization_ExRootAnalysisDict_Impl();
}
