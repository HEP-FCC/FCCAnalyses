#include "TMVAHelper/TMVAHelper.h"


tmva_helper_xgb::tmva_helper_xgb(const std::string &filename, const std::string &name, const unsigned &nvars, const unsigned int nslots) :
    model_(name, filename), nvars_(nvars) {

    const unsigned int nslots_actual = std::max(nslots, 1U);
    interpreters_.reserve(nslots_actual);
    for (unsigned int islot = 0; islot < nslots_actual; ++islot) {
        interpreters_.emplace_back(model_);
    }
}

ROOT::VecOps::RVec<float> tmva_helper_xgb::operator()(const ROOT::VecOps::RVec<float> vars) {
    auto const tbb_slot = std::max(tbb::this_task_arena::current_thread_index(), 0);
    if (tbb_slot >= interpreters_.size()) {
        throw std::runtime_error("Not enough interpreters allocated for number of tbb threads");
    }
    auto &interpreter_data = interpreters_[tbb_slot];
    return interpreter_data.Compute(vars);
}

tmva_helper_xgb::~tmva_helper_xgb() {}
