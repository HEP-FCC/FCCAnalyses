import uproot
import argparse

default_input='/eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/p8_ee_ZZ_ecm240/events_057786065.root'

parser = argparse.ArgumentParser(description='Args')
parser.add_argument('--input', default=default_input)
args = parser.parse_args()

file = uproot.open(args.input)
podio_table = file['podio_metadata']['events___idTable']['m_names'].array()[0]

print("")
print("ID  ->  Collection")
print("==================")
for i,val in enumerate(podio_table):
    print("{} -> {}".format(i+1, val))
print("==================")
