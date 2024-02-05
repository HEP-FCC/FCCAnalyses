#!/usr/bin/env bash

set -euo pipefail
TEST_INPUT_DATA_DIR=$(mktemp -d -p $(pwd) test_input_data_XXXXXXXX)
export TEST_INPUT_DATA_DIR

cd $TEST_INPUT_DATA_DIR

# retrieve Weaver tests inputs
curl -O -L https://fccsw.web.cern.ch/fccsw/testsamples/fccanalyses/weaver-inference/preprocess.json > /dev/null 2>&1
curl -O -L https://fccsw.web.cern.ch/fccsw/testsamples/fccanalyses/weaver-inference/fccee_flavtagging_dummy.onnx > /dev/null 2>&1

# announce where we store variables to the outside
echo -n $TEST_INPUT_DATA_DIR
