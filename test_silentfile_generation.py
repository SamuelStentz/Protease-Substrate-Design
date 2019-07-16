import os
import argparse
import itertools

parser = argparse.ArgumentParser()

parser.add_argument("-p","--protease", required = True, help = "name of the protease/folder name")
parser.add_argument("-df","--destination_folder", required = True, help = "where to put the folders")
parser.add_argument("-s","--substrate",required = True, help = "substrate full name in correct format, with _ implying variable regions. Should be contiguous")
parser.add_argument("-st", "--substrate_text", help="text file of all intended substrates that should have been generated")


args = parser.parse_args()

if args.substrate_text is not None:
	ll = open(args.substrate_text).readlines()
	ll = [x.strip() for x in ll]
else:
	ll = []

if not os.path.exists(args.destination_folder):
	raise ValueError("Path {} not valid".format(args.destination_folder))

prot_path = os.path.join(args.destination_folder, args.protease)

if "." not in args.substrate:
	raise ValueError("Cleavage site not indicated")

start_variable = -1
end_variable = -1
cleavage = -1
for counter,char in enumerate(args.substrate):
	if start_variable == -1 and char == "_":
		start_variable = counter
	if start_variable != -1 and end_variable == -1 and char != "_" and char != ".":
		end_variable = counter
	if char == ".":
		cleavage = counter
	if end_variable != -1 and start_variable != -1:
		break

if end_variable == -1 or start_variable == -1:
	raise ValueError("The variable region was not found for substrate {}, start {}, end {}".format(args.substrate, start_variable, end_variable))
 
if cleavage < end_variable and cleavage > start_variable:
	print("Cleavage in variable domain {}..{}..{}".format(start_variable, cleavage, end_variable))
	var_mag = end_variable - start_variable - 1
else:
	var_mag = end_variable - start_variable


aa = "ACDEFGHIKLMNPQRSTVWY"

sf_missing = []

#change all substrate names into their silent file names and make those a set
sf_required = set()
for x in ll:
	x = list(x)
	x[end_variable - 1] = "_"
	x[end_variable - 2] = "_"
	sf_required.add("".join(x))

#check all necessary folders
for variable_region in itertools.product(*[aa for i in range(var_mag-2)]):
	variable_counter = 0
	directory = list(args.substrate)
	for counter,char in enumerate(args.substrate):
		if char == "_" and variable_counter < var_mag - 2:
			#change variable region in directory name to the currently considered possible substrate
			directory[counter] = variable_region[variable_counter]
			variable_counter += 1
	if args.substrate_text is None or "".join(directory) in sf_required:
		sf_dir_path = os.path.join(prot_path, "".join(directory))
		sf_path = os.path.join(sf_dir_path, "".join(directory))
		if not os.path.isfile(sf_path):
			sf_missing.append(sf_path)

print("Number of silent files missing:     {}".format(len(sf_missing)))
print("Missing the following silent files: {}".format(sf_missing))

