#!/bin/bash

mkdir -p ./man/html
cd ./man/man1
for MANFILE in *; do
  mandoc -Thtml -Ostyle=../../css/mandoc.css "${MANFILE}" > "../html/${MANFILE::-1}html"
done
cd ../man7
for MANFILE in *; do
  mandoc -Thtml -Ostyle=../../css/mandoc.css "${MANFILE}" > "../html/${MANFILE::-1}html"
done
