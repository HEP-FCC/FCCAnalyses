#ifndef TMVAHelper_TMVAHelper_h
#define TMVAHelper_TMVAHelper_h

#include <tbb/task_arena.h>
#include "ROOT/RVec.hxx"
#include "TMVA/RBDT.hxx"


class tmva_helper_xgb {
    public:
        explicit tmva_helper_xgb(const std::string &filename, const std::string &name, const unsigned &nvars, const unsigned int nslots = 1);
        virtual ~tmva_helper_xgb();
        ROOT::VecOps::RVec<float> operator()(const ROOT::VecOps::RVec<float> vars);

    private:
        unsigned int nvars_;
        TMVA::Experimental::RBDT<> model_;
        std::vector<TMVA::Experimental::RBDT<>> interpreters_;
};


#endif