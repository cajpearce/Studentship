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

	for p in all_pipes:
		print etree.tostring(p,pretty_print=True)

	# create an empty dictionary, this will store the NODE GRAPH
	pipe_node_graph = dict()

	# populate the pattern dictionary so that we know what each node is
	for key in component_dictionary:
		pipe_node_graph[key] = []


	# THIS WORKS IN PLACE
	# pipe_node_graph gets changed IN PLACE!!!!
	create_graph(all_pipes, namespace, pipe_node_graph)
	

	topograph = sort_topologically(pipe_node_graph)
	
	# put it in order of INPUT to OUTPUT	
	topograph.reverse()

	
	print "ALL_PIPES " + str(pipe_node_graph)
	print "DIRECTION " + str(topograph)
	
	return topograph


def recursive_read_pipeline(topograph, current_index):
	pass

def create_graph(all_pipes, namespace, ret_dict = dict()):
	
	for pipe in all_pipes:
		start = pipe.find(namespace + "start")
		end = pipe.find(namespace + "end")
		
		o_component = start.get("component")
		i_component = end.get("component")

		o_variable = start.get("output")
		i_variable = end.get("input")

		if o_component in ret_dict:
			# append to existing array
		        ret_dict[o_component].append(i_component)
		else:
			# create a new array in this slot
			ret_dict[o_component] = [i_component]

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

y = readPipeline("pipe.xml")
