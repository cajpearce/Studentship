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

def readModule(xml_file, input_var_names=list(), input_xml='INPUT.XML', output_xml='OUTPUT.XML'):
	
	tree, namespace = readXML(xml_file)
	root = tree.getroot()

	# Get the file that we need to run
	run_file = root.find(namespace + "source").get("ref")

	# Get the platform
	platform = root.find(namespace + "platform").get("name")



	# get all potential input elements
	input_elements = root.findall(namespace + "input")

	if len(input_elements) != len(input_var_names):
		raise Exception("You have not provided valid input var names.")
	# get all potential output elements
	output_elements = root.findall(namespace + "output")


	prepend = []

	
	input_name = input_xml.replace(".","_").replace(" ","_")
	output_name = output_xml.replace(".","_").replace(" ","_")
	current_name = xml_file.replace(".","_").replace(" ","_")
	
	all_elements = input_elements+output_elements

	for index, i in enumerate(all_elements):
		if i.get("type") == "internal": 
			temp_var = ''
			position = 0
			
			if i.tag == namespace + "input":
				temp_var = input_name + "_" + current_name
			elif i.tag == namespace + "output":
				temp_var = current_name + "_" + output_name
				position = 1
			else:
				raise Exception("No input/output tag??")

			temp_var += "_" + i.get("name")
			temp_var = i.get("name") + " = " + temp_var
				
			prepend.append((temp_var,position))

		elif i.get("type") == "external":
			warn("You cannot pass variables externally.")
		else:
			# will be raised when a tag is not specified
			raise Exception("You have not specified a type for " + 
					str(i.attrib))

	print prepend

	

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



readModule("test2.xml")





def line_prepender(filename, line):
        with open(filename, 'r+') as f:
                content = f.read()
                f.seek(0, 0)
                f.write(line.rstrip('\r\n') + '\n' + content)
        
def copy_file_to_temp_directory(path,append_to_start='',append_to_end=''):
        '''
        with open("infile") as f1:
                with open("outfile", "w") as f2:
                        f2.write("#test firstline")
                        for line in f1:
                                f2.write(line)
        '''
        # modified from TorelTwiddler's code
        # http://stackoverflow.com/questions/6587516/how-to-concisely-create-a-temporary-file-that-is-a-copy-of-another-file-in-pytho
        if not os.path.isfile(path):
                raise Exception("You are trying to use a path instead of a file for your module.")
        temp_dir = tempfile.gettempdir()
        #temp_path = os.path.join(temp_dir, os.path.basename(path))
        temp_path = os.path.join(temp_dir, "test_python_script.py") #could techinically be less generic
        shutil.copy2(path, temp_path)

        # adds the temp directory to the system path to make it easier to import
        # does that mean I'll need to change the 
        sys.path.append(temp_dir)
        
#if len(append_to_start) > 0 or len(append_to_end) < 0:
                #do something fucking cool here m8
                         
        return temp_path
    
