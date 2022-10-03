#!/usr/bin/env bash

set -euo pipefail
TEST_INPUT_DATA_DIR=$(mktemp -d -p $(pwd) test_input_data_XXXXXXXX)
export TEST_INPUT_DATA_DIR

cd $TEST_INPUT_DATA_DIR

# retrieve Weaver tests inputs
wget https://key4hep.web.cern.ch/key4hep/testFiles/weaverInference/preprocess.json > /dev/null 2>&1
wget https://key4hep.web.cern.ch/key4hep/testFiles/weaverInference/fccee_flavtagging_dummy.onnx > /dev/null 2>&1

# announce where we store variables to the outside
echo -n $TEST_INPUT_DATA_DIR
