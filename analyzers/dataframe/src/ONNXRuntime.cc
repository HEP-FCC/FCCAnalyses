#include "ONNXRuntime.h"

ONNXRuntime::ONNXRuntime(const std::string& model_path) {}

ONNXRuntime::~ONNXRuntime() {}

ROOT::VecOps::RVec<ROOT::VecOps::RVec<float> > ONNXRuntime::run() const {
  ROOT::VecOps::RVec<ROOT::VecOps::RVec<float> > out;
  return out;
}

