#!/bin/env bash

# This test steers the analysis of an example input file using the helper function
# defined in the case study namespace.

fccanalysis run case-studies/analysis_example/scripts/analysis_example.py \
  --test \
  --nevents 100 \
  --bench
