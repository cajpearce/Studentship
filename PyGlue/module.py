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


	prepend = []

	
	input_name = input_xml.replace(".","_").replace(" ","_")
	output_name = output_xml.replace(".","_").replace(" ","_")
	current_name = xml_file.replace(".","_").replace(" ","_")


	for index, i in enumerate(input_elements):
		if i.get("type") == "internal": 
			temp_var = input_name + "_" + current_name

			#temp_var += "_" + i.get("name")
			temp_var += "_" + input_variable_names[index]

			temp_var = i.get("name") + " = " + temp_var
				
			prepend.append(temp_var)

		elif i.get("type") == "external":
			warn("You cannot pass variables externally.")
		else:
			# will be raised when a tag is not specified
			raise Exception("You have not specified a type for " + 
					str(i.attrib))

	addend = []
	output_variable_names = []

	for o in output_elements:
		if o.get("type") == "internal": 
			output_variable_names.append(o.get("name"))

			temp_var = current_name + "_" + output_name

			temp_var += "_" + o.get("name")

			temp_var += " = " + o.get("name")
				
			addend.append(temp_var)

		elif o.get("type") == "external":
			warn("You cannot pass variables externally.")
		else:
			# will be raised when a tag is not specified
			raise Exception("You have not specified a type for " + 
					str(o.attrib))
	
	ret = line_var_transferer(run_file, prepend, addend)
	return ret

def line_var_transferer(filename, add_to_start='\n',add_to_end='\n'):
	ret = ''
        with open(filename, 'r+') as f:
                content = f.read()

                #f.seek(0, 0)
		write_start = ''
		if type(add_to_start) is list:
			write_start = '\n'.join(add_to_start)
		else:
			write_start = add_to_start

		write_end = ''
		if type(add_to_end) is list:
			write_end = '\n'.join(add_to_end)
		else:
			write_end = add_to_end
		
		prior = "\n# the previous are importing from another module\n"
		follow = "\n# the following are exporting to another module\n"

		#f.write(write_start + prior + content + follow + write_end)
		
		ret = write_start + prior + content + follow + write_end
	return ret



if __name__ == "__main__":
	print("TEST: " + str(readModule("test.xml",
		['CUSTOM_DF','CUSTOM_NZP','CUSTOM_COLOURS'])))



    
