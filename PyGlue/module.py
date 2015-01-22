from lxml import etree
import subprocess

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

	shell_command = platform + " " + run_file
	shell_command2 = [platform, run_file]
	#p = subprocess.Popen(shell_command, 
	#			shell=True,stdout=subprocess.PIPE)

	#out, err = p.communicate()
	return subprocess.check_output(shell_command2, shell=True)


	# Python's call is 'python [file]'
	# R is 'Rscript [file]'


