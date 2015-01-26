from lxml import etree
import subprocess # for R
import importlib  # for python
import tempfile, shutil, os # for copying files over
import sys

# read the ElementTree
tree = etree.parse("test.xml")

#assigns the root element
root = tree.getroot()

# assigns the namespace dictionary to NSMAP
NSMAP = root.nsmap

# assigns our sole namespace to namespace
namespace = "{" + NSMAP[None] + "}"


def readModule(root, namespace):
	# Get the file that we need to run
	run_file = root.find(namespace + "source").get("ref")

	# Get the platform
	platform = root.find(namespace + "platform").get("name")



	# get all potential input elements
	input_elements = root.findall(namespace + "input")

	# get all potential output elements
	output_elements = root.findall(namespace + "output")

	for i in input_elements:
		print i.attrib

	for o in output_elements:
		print o.attrib

        run = None
        if platform.lower() == "python":
                # use copy file to temp...

                temp = copy_file_to_temp_directory(run_file,"hello","bye")
                
                run = importlib.import_module(temp)

        # get variables???
        print [item for item in dir(adfix) if not item.startswith("__")]
        
	#shell_command = platform + " " + run_file
	#shell_command2 = [platform, run_file]
	#p = subprocess.Popen(shell_command, 
	#			shell=True,stdout=subprocess.PIPE)

	#out, err = p.communicate()
	#return subprocess.check_output(shell_command2, shell=True)


	# Python's call is 'python [file]'
	# R is 'Rscript [file]'


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
        if len(append_to_start) > 0 or len(append_to_end) < 0:
                #do something fucking cool here m8
                         
        return temp_path
    
