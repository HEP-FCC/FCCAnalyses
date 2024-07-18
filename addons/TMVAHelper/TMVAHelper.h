#ifndef TMVAHelper_TMVAHelper_h
#define TMVAHelper_TMVAHelper_h

// ROOT
#include "ROOT/RVec.hxx"
#include "TMVA/RBDT.hxx"

// TBB
#include <tbb/task_arena.h>

// std
#include <string>
#include <vector>

class tmva_helper_xgb {
public:
  tmva_helper_xgb(const std::string &filename, const std::string &name,
                  const unsigned int nslots = 1);
  ~tmva_helper_xgb() {};
  ROOT::VecOps::RVec<float> operator()(const ROOT::VecOps::RVec<float> vars);

private:
  // Default backend (template parameter) is:
  // TMVA::Experimental::BranchlessJittedForest<float>
  std::vector<TMVA::Experimental::RBDT<>> m_interpreters;
};

#endif
