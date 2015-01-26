from lxml import etree
import subprocess # for R
import importlib  # for python
import tempfile, shutil, os # for copying files over
import sys
from warnings import warn


# Goal is to read all possible modules


def readXML(xml_file):
	# read the ElementTree
	tree = etree.parse(xml_file)

	# assigns the namespace dictionary to NSMAP
	NSMAP = tree.getroot().nsmap

	# assigns our sole namespace to namespace
	namespace = "{" + NSMAP[None] + "}"

	return tree, namespace

def readModule(xml_file, input_variable_names=list(), input_xml='INPUT.XML', output_xml='OUTPUT.XML'):
	'''
	Currently you need to provide a list
	'''
	tree, namespace = readXML(xml_file)
	root = tree.getroot()

	# Get the file that we need to run
	run_file = root.find(namespace + "source").get("ref")

	# Get the platform
	platform = root.find(namespace + "platform").get("name")



	# get all potential input elements
	input_elements = root.findall(namespace + "input")

	if len(input_variable_names) != len(input_elements):
		raise Exception("You have provided incorrect input variables")

	# get all potential output elements
	output_elements = root.findall(namespace + "output")


	var_transfer = []

	
	input_name = input_xml.replace(".","_").replace(" ","_")
	output_name = output_xml.replace(".","_").replace(" ","_")
	current_name = xml_file.replace(".","_").replace(" ","_")


	for index, i in enumerate(input_elements):
		if i.get("type") == "internal": 
			position = 0
			
			temp_var = input_name + "_" + current_name

			#temp_var += "_" + i.get("name")
			temp_var += "_" + input_variable_names[index]

			temp_var = i.get("name") + " = " + temp_var
				
			var_transfer.append((temp_var,position))

		elif i.get("type") == "external":
			warn("You cannot pass variables externally.")
		else:
			# will be raised when a tag is not specified
			raise Exception("You have not specified a type for " + 
					str(i.attrib))



	for o in output_elements:
		if o.get("type") == "internal": 
			temp_var = current_name + "_" + output_name
			position = 1

			temp_var += "_" + o.get("name")

			temp_var = o.get("name") + " = " + temp_var
				
			var_transfer.append((temp_var,position))

		elif o.get("type") == "external":
			warn("You cannot pass variables externally.")
		else:
			# will be raised when a tag is not specified
			raise Exception("You have not specified a type for " + 
					str(o.attrib))
	


        if platform.lower() == "python":
		pass
                #TODO: make this work
                #temp = copy_file_to_temp_directory(run_file,"hello","bye")
                #run = importlib.import_module(temp)
	else:
		pass
		#TODO: make this work
		#shell_command = platform + " " + run_file
		#shell_command2 = [platform, run_file]
		#p = subprocess.Popen(shell_command, 
		#			shell=True,stdout=subprocess.PIPE)

		#out, err = p.communicate()
		#return subprocess.check_output(shell_command2, shell=True)
		# get variables???
		# Rscript for R

	return var_transfer

print("TEST3: " + str(readModule("test3.xml",['CUSTOM_INPUT'])))
print("NO INPUTS: " + str(readModule("test_no_inputs.xml")))




    
