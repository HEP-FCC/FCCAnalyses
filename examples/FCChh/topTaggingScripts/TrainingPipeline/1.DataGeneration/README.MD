# 🛠️ FCC-hh Event Simulation with MadGraph, Pythia8, and Delphes

This guide walks you through setting up and running a basic Delphes simulation pipeline using MadGraph-generated LHE files on the FCC-hh framework.

---

## 📁 1. Set Up EOS Access

```bash
export EOS_MGM_URL="root://eospublic.cern.ch"
```

---

## 📦 2. Retrieve MadGraph LHE File

```bash
cp /eos/experiment/fcc/hh/generation/lhe/mg_pp_tttt_wmlep_Q_1000_3000_5f_84TeV/events_077321540.lhe.gz .
gunzip -c events_077321540.lhe.gz > events.lhe
```

---

## 📄 3. Get a Delphes Card

```bash
cp /cvmfs/sw.hsf.org/key4hep/releases/2025-01-28/x86_64-almalinux9-gcc14.2.0-opt/delphes/3.5.1pre12-e4qfky/cards/FCC/scenarios/FCChhTrackCov_II.tcl ./card.tcl
```

---

## 🧪 4. PythiaDelphes Files

```bash
cp /eos/experiment/fcc/hh/utils/pythiacards//p8_pp_default.cmd card.cmd
cp /eos/experiment/fcc/hh/utils/edm4hep_output_config.tcl .

```

---

## ✏️ 5. Configure Pythia

```bash
echo "Beams:LHEF = events.lhe" >> card.cmd
echo "Random:seed = 77321540" >> card.cmd
echo "Main:numberOfEvents = 1000" >> card.cmd
```

---

## ⚙️ 6. Prepare Your Environment

```bash
# Clean environment variables
unset LD_LIBRARY_PATH
unset PYTHONHOME
unset PYTHONPATH

# Load Key4HEP environment
source /cvmfs/sw.hsf.org/key4hep/setup.sh -r 2025-01-28
```

---

## 🚀 7. Run the Simulation

```bash
DelphesPythia8_EDM4HEP card.tcl edm4hep_output_config.tcl card.cmd events_077321540.root
```
