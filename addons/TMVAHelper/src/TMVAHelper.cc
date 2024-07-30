#include "TMVAHelper/TMVAHelper.h"

#include "RVersion.h"

tmva_helper_xgb::tmva_helper_xgb(const std::string &filename,
                                 const std::string &name,
                                 const unsigned int nslots) {

  const unsigned int nslots_actual = std::max(nslots, 1U);
  m_interpreters.reserve(nslots_actual);
  for (unsigned int islot = 0; islot < nslots_actual; ++islot) {

#if ROOT_VERSION_CODE >= ROOT_VERSION(6, 32, 0)
    m_interpreters.emplace_back(TMVA::Experimental::RBDT(name, filename));
#else
    m_interpreters.emplace_back(TMVA::Experimental::RBDT<>(name, filename));
#endif
  }
}

ROOT::VecOps::RVec<float>
tmva_helper_xgb::operator()(const ROOT::VecOps::RVec<float> vars) {
  auto const tbb_slot =
      std::max(tbb::this_task_arena::current_thread_index(), 0);
  if (tbb_slot >= m_interpreters.size()) {
    throw std::runtime_error(
        "Not enough interpreters allocated for number of tbb threads");
  }
  auto &interpreter_data = m_interpreters[tbb_slot];
  return interpreter_data.Compute(vars);
}
