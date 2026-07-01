#!/bin/bash

for (( i=0; i<=50; i++ ))
do
  echo "Processing chunk: $i"
  bash run_the_skim.sh $i
done
