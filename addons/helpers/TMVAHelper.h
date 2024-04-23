#ifndef HELPER_TMVA_H
#define HELPER_TMVA_H

#include <tbb/task_arena.h>

namespace FCCAnalyses {

class tmva_helper_xgb {
    public:
        tmva_helper_xgb(const std::string &filename, const std::string &name, const unsigned &nvars, const unsigned int nslots = 1) :
            model_(name, filename), nvars_(nvars) {

            const unsigned int nslots_actual = std::max(nslots, 1U);
            interpreters_.reserve(nslots_actual);
            for (unsigned int islot = 0; islot < nslots_actual; ++islot) {
                interpreters_.emplace_back(model_);
            }
        }

        Vec_f operator()(const Vec_f vars) {
            auto const tbb_slot = std::max(tbb::this_task_arena::current_thread_index(), 0);
            if (tbb_slot >= interpreters_.size()) {
                throw std::runtime_error("Not enough interpreters allocated for number of tbb threads");
            }
            auto &interpreter_data = interpreters_[tbb_slot];
            return interpreter_data.Compute(vars);
        }

    private:
        unsigned int nvars_;
        TMVA::Experimental::RBDT<> model_;
        std::vector<TMVA::Experimental::RBDT<>> interpreters_;
};


// https://root.cern/doc/master/RReader_8hxx_source.html
class tmva_xml {

    public:
        tmva_xml(const std::string &filename) {
            
            auto c = TMVA::Experimental::Internal::ParseXMLConfig(filename);
            fVariables = c.variables;
            fExpressions = c.expressions;
            fAnalysisType = c.analysisType;
            fNumClasses = c.numClasses;

            fReader = std::make_unique<TMVA::Reader>("Silent");
            const auto numVars = fVariables.size();
            fValues = std::vector<float>(numVars);

            for(std::size_t i = 0; i < numVars; i++) {
                fReader->AddVariable(TString(fExpressions[i]), &fValues[i]);
            }
            fReader->BookMVA(name, filename.c_str());

        }

        std::vector<float> Compute(const Vec_f &x) {
            
            if (x.size() != fVariables.size())
                throw std::runtime_error("Size of input vector is not equal to number of variables.");

            // Copy over inputs to memory used by TMVA reader
            for (std::size_t i = 0; i < x.size(); i++) {
                fValues[i] = x[i];
            }

            // Evaluate TMVA model
            // Classification
            if (fAnalysisType == TMVA::Experimental::Internal::AnalysisType::Classification) {
                return std::vector<float>({static_cast<float>(fReader->EvaluateMVA(name))});
            }
            // Regression
            else if (fAnalysisType == TMVA::Experimental::Internal::AnalysisType::Regression) {
                return fReader->EvaluateRegression(name);
            }
            // Multiclass
            else if (fAnalysisType == TMVA::Experimental::Internal::AnalysisType::Multiclass) {
                return fReader->EvaluateMulticlass(name);
            }
            // Throw error
            else {
                throw std::runtime_error("RReader has undefined analysis type.");
                return std::vector<float>();
            }
        }

    private:
        std::unique_ptr<TMVA::Reader> fReader;
        std::vector<float> fValues;
        std::vector<std::string> fVariables;
        std::vector<std::string> fExpressions;
        unsigned int fNumClasses;
        const char *name = "RReader";
        TMVA::Experimental::Internal::AnalysisType fAnalysisType;
};


class tmva_helper_xml {
    public:
        tmva_helper_xml(const std::string &filename, const unsigned int nslots = 1) {

            const unsigned int nslots_actual = std::max(nslots, 1U);

            for (unsigned int islot = 0; islot < nslots_actual; ++islot) {
                tmva_xml *tmp = new tmva_xml(filename);
                interpreters_.emplace_back(tmp);
            }
        }

        std::vector<float> operator()(const Vec_f vars) {
            auto const tbb_slot = std::max(tbb::this_task_arena::current_thread_index(), 0);
            if (tbb_slot >= interpreters_.size()) {
                throw std::runtime_error("Not enough interpreters allocated for number of tbb threads");
            }
            auto &interpreter_data = interpreters_[tbb_slot];
            return interpreter_data->Compute(vars);
        }

    private:
        std::vector<tmva_xml *> interpreters_;
};

}

#endif