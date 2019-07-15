"""
example script:
python text_to_slurm.py -txt /projects/f_sdk94_1/EnzymeModelling/Protease-Substrate-Design/HCV_R170K_A171T_D183A_commands.txt -job_name HCV_R170K_A171T_D183A -mem 12000 -path_operation /projects/f_sdk94_1/EnzymeModelling/Protease-Substrate-Design -path_sh /projects/f_sdk94_1/EnzymeModelling/Commands -batch 20 -time 2-00:00:00
"""

import os
import argparse
import itertools

parser = argparse.ArgumentParser()
parser.add_argument("-txt","--text_file", type = str, help = "name of text file")
parser.add_argument("-p","--protease", type = str, help = "name of the protease")
parser.add_argument("-st", "--substrate_txt", type = str, help= "name of text file containing substrates to include")

args = parser.parse_args()

if args.protease is None:
	protease = "HCV"
else:
	protease = args.protease

if args.text_file is None:
	txt = "commands.txt"
else:
	txt = args.text_file

if args.substrate_txt is None:
	st = ""
else:
	st = "-st {}".format(args.substrate_txt)

od = "/projects/f_sdk94_1/EnzymeModelling/SilentFiles/{}"
s = "/projects/f_sdk94_1/EnzymeModelling/CrystalStructure/{}.pdb"
substrate_HCV = "A{}__C.ASHL"
p1 = 203

template = "python design_protease.py -s {} -od {} -sf {} -site 198 -ps \"198-202\" -cons ly104.cst -cr 72 96 154 -dprot 0 -dpep 0 -p1 {} {}" 

aa = "ACDEFGHIKLMNPQRSTVWY"

fh = open(txt, "w")

for (i,j,k) in itertools.product(*[aa for i in range(3)]):
	var = i + j + k
	sf = substrate_HCV.format(var)
	command = template.format(s.format(protease),
		od.format(protease), sf, p1, st)
	fh.write("{}\n".format(command))
fh.close()

