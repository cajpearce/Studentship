from lxml import etree
import subprocess # for R
import importlib  # for python
import tempfile, shutil, os # for copying files over
import sys
from warnings import warn


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
	tree, namespace = readXML(xml_file)
	root = tree.getroot()

	all_components = root.findall(namespace + "component")
	component_dictionary = create_component_dictionary(all_components)

	all_pipes = root.findall(namespace + "pipe")
	
	pipe_graph = dict()

	# populate the pattern dictionary so that we know what each node is
	for key in component_dictionary:
		pipe_graph[key] = []

	print create_graph(all_pipes, namespace, pipe_graph)

	print find_all_paths(pipe_graph, 'start', 'plot')


def create_graph(all_pipes, namespace, ret_dict = dict()):
	
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

def find_all_paths(graph, start, end, path=[]):
	# rewrite this so that it can find LITERALLY all paths manually
	'''
	https://www.python.org/doc/essays/graphs/
	'''
	path = path + [start]
	if start == end:
		return [path]
	if not graph.has_key(start):
		return []
	paths = []
	for node in graph[start]:
		if node not in path:
			newpaths = find_all_paths(graph, node, end, path)
			for newpath in newpaths:
				paths.append(newpath)
        return paths


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

readPipeline("pipe.xml")
