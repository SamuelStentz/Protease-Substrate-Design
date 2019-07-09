import os
import argparse
import itertools

parser = argparse.ArgumentParser()
parser.add_argument("-txt","--text_file", help = "name of text file")
parser.add_argument("-p","--protease", help = "name of the protease")
args = parser.parse_args()

if args.protease is None:
	protease = "HCV"
else:
	protease = args.protease

if args.text_file is None:
	txt = "commands.txt"
else:
	txt = args.text_file

od = "/projects/f_sdk94_1/EnzymeModelling/SilentFiles/{}/{}"
s = "/projects/f_sdk94_1/EnzymeModelling/CrystalStructure/{}.pdb"

template = "python design_protease.py -s {} -od {} -sf {} -site 198 -ps \"198-202\" -cons ly104.cst -cr 72 96 154 -dprot 0 -dpep 0" 

aa = "ACDEFGHIKLMNPQRSTVWY"

fh = open(txt, "w")

for (i,j,k) in itertools.product(*[aa for i in range(3)]):
	sf = i + j + k
	command = template.format(s.format(protease), od.format(protease, sf), sf)
	fh.write("{}\n".format(command))
fh.close()

