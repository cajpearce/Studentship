from lxml import etree
import subprocess # for R
import importlib  # for python
import tempfile, shutil, os # for copying files over
import sys
from warnings import warn
from topological_sort import sort_topologically
import module

def readXML(xml_file):
	# read the ElementTree
	tree = etree.parse(xml_file)

	# assigns the namespace dictionary to NSMAP
	NSMAP = tree.getroot().nsmap

	# assigns our sole namespace to namespace
	namespace = "{" + NSMAP[None] + "}"

	return tree, namespace

def readPipeline(xml_file):
	'''
	Currently you need to provide a list
	'''
	# read in the xml Tree
	tree, namespace = readXML(xml_file)
	root = tree.getroot()
	
	# just gets all the COMPONENTS
	all_components = root.findall(namespace + "component")

	# creates a dictionary
	# really simply, just maps m1 to module1.xml
	# will use these later to know which modules to run!
	component_dictionary = create_component_dictionary(all_components)
	# LATER MATE


	# this finds all the pipe connections. Each pipe contains sub-elements
	all_pipes = root.findall(namespace + "pipe")


	# create the directioned node graph and assigns it to a dictionary
	pipe_node_graph = create_graph(all_pipes, namespace)
	

	topograph = sort_topologically(pipe_node_graph)
	
	# put it in order of INPUT to OUTPUT	
	topograph.reverse()

	
	#print "ALL_PIPES " + str(pipe_node_graph)
	#print "DIRECTION " + str(topograph)
	
	return topograph


def recursive_read_pipeline(topograph, current_index):
	pass

def create_graph(all_pipes, namespace, ret_dict = dict()):
	# this works fine
	# keep in mind that it is always going to be a linear process
	# getting the input variables will be the long term job
	for pipe in all_pipes:
		start = pipe.find(namespace + "start")
		end = pipe.find(namespace + "end")
		
		o = start.get("component")
		i = end.get("component")

		if o in ret_dict:
			# append to existing array
		        ret_dict[o].append(i)
		else:
			# create a new array in this slot
			ret_dict[o] = [i]

	return ret_dict


def create_component_dictionary(elements):
	'''
	Components are essentially reference pointers - x points to the xml file
	As such they are easily represented in the form of a dictionary
	This function creates the dictionary for easy access
	'''
	ret_dict = dict()
	for component in elements:
		if component.get('type') == "module":
			key = component.get('name')
			reference = component.get('ref')
			
			ret_dict[key] = reference
	return ret_dict


simple_pipe  = readPipeline("simple_pipe.xml")
complex_pipe = readPipeline("complex_pipe.xml")
#my_pipe = readPipeline("my_pipe.xml")

for i, direction in enumerate(simple_pipe):
	print str(i + 1) + ":"
	for p in direction:
		print str(p) + " ",
	print
