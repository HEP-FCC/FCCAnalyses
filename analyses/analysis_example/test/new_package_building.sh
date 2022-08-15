#!/bin/env bash

source setup.sh

# prepare the environment
OUTPUT_DIR=${LOCAL_DIR}/dummy_analysis
LD_LIBRARY_PATH=${LOCAL_DIR}/install:${LD_LIBRARY_PATH}
PYTHONPATH=${LOCAL_DIR}:${PYTHONPATH}
PATH=${LOCAL_DIR}/bin:${LOCAL_DIR}:${PATH}
ROOT_INCLUDE_PATH=${LOCAL_DIR}/install:${ROOT_INCLUDE_PATH}

if [ -d ${OUTPUT_DIR} ] ; then
  rm -rf ${OUTPUT_DIR};
fi

# first, initialise a new dummy analysis package
fccanalysis init my_dummy_analysis \
  --output-dir ${OUTPUT_DIR} \
  --standalone

# next, build the standalone analyser
PWD=${PWD}
mkdir -p ${OUTPUT_DIR}/build && cd ${OUTPUT_DIR}/build
cmake .. && make && make install

# finally, run a simple analysis test
cd ${PWD}
fccanalysis run ${OUTPUT_DIR}/scripts/analysis_cfg.py \
  --test \
  --nevents 100 \
  --bench
