from lxml import etree
import subprocess # for R
import importlib  # for python
import tempfile, shutil, os # for copying files over
import sys
from warnings import warn


# Goal is to read all possible modules

class Module:
	def __init__(self, xml_file):
		self.xml_file = xml_file

		self.setup_tree()
		self.setup_namespace()	
		self.setup_root()

		self.parse_information_from_xml()
	def setup_tree(self):
		self.tree = etree.parse(self.xml_file)

		return self.tree

	def setup_namespace(self):
		temp_namespace = self.tree.getroot().nsmap
		#formats it properly and assigns it to self
		self.namespace = "{" + temp_namespace[None] + "}"

		return self.namespace

	def setup_root(self):
		self.root = self.tree.getroot()
		return self.root

	def parse_information_from_xml(self):
		self.source_file = self.search_inside_tag("source","ref")
		self.platform = self.search_inside_tag("platform","name")
		self.inputs = self.root.findall(self.namespace + "input")
		self.outputs = self.root.findall(self.namespace + "output")


	def search_inside_tag(self, tag, attribute):
		return self.root.find(self.namespace + tag).get(attribute)
	
	def __str__(self):
		return etree.tostring(self.tree,pretty_print=True)


def createWrittenFile():
	
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



#if __name__ == "__main__":
x = Module("test.xml")
print(str(x))
#	print("TEST: " + str(readModule("test.xml",
#		['CUSTOM_DF','CUSTOM_NZP','CUSTOM_COLOURS'])))



    
