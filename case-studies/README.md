# Analyses packages for case studies

[![experimental](http://badges.github.io/stability-badges/dist/experimental.svg)](http://github.com/badges/stability-badges)

For various physics case studies, standard RDF tools might not be sufficient and require a backing library of helper objects and static functions exposed to ROOT.

An analysis package creation tool is developed to provide the minimal building blocks for such extensions and uniformise such developments.

## Analysis package generation

Two modes are currently supported for the linking of these extensions to the analysis framework:

- scan at CMake+compilation time a _standard_ extensions directory (in `case-studies`) where the analysis package can be deployed. It requires an `includes` and `src` subdirectory, along with a `classes_def.xml` and `classes.h` files in the latter for the ROOT dictionary definition.
- generate a _standalone_ package which can be compiled independently, given the path to this `FCCAnalyses` installation is found. It allows to generate a minimal set of files required to connect this extension to the RDF utilitaries.

The generation of such a package can be done using the following recipe:

```bash
fccanalysis init [-h] [--name NAME] [--author AUTHOR] [--description DESCRIPTION] [--standalone] [--output-dir OUTPUT_DIR] package
```
where the mandatory parameter, `package`, refers to the analysis package name (along with the namespace it will define ; should be unique at runtime).
Additionally, several optional parameters are handled:
- `NAME` specifies the analyser helpers filename (where all static functions exposed to the RDF framework through the ROOT dictionary will be stored) ;
- `AUTHOR`, preferably following the "`name <email@address>`" convention, and `DESCRIPTION`, will be added into the C++ files boilerplates to keep track of the author(s) and purpose(s) of this package ;
- `--standalone` to switch to the standalone package described above. In combination with the `OUTPUT_DIR` parameter, it allows to store the minimal working example in a completely arbitrary path (instead of the standard `case-studies` subdirectory) with its own CMake directive.

In the _standalone_ mode, the analysis package can be built using the standard CMake recipe, given the FCCAnalyses environment in `setup.sh` is properly sourced:

```bash
mkdir build && cd build
cmake ${OUTPUT_DIR} && make
make install
```
The latter ensures that the headers and shared library/ROOT translation dictionaries are installed in a location reachable by FCCAnalyses.

## Analysis package exposure to RDF

To allow an arbitrary multiplicity of analysis packages to be handled at the level of a configuration script runnable with "`fccanalysis run`", an additional (optional) `analysesList` list-type object can be parsed.

On top of the usual `FCCAnalyses` shared object, includes, and corresponding dictionary, the custom case study analysis package name will be parsed, and automatically loaded in the ROOT runtime environment to be exposed to the RDF interface.
