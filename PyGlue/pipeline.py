from lxml import etree
from warnings import warn
from topological_sort import sort_topologically
import os
#import module

class Pipeline:
	def __init__(self, xml_file):
		self.xml_file = xml_file

		self.setup_tree()
		self.setup_namespace()	
		self.setup_root()

		self.parse_information_from_xml()
		self.read_in_modules()

		self.running_order = self.collapse_list_of_sets_into_module_order()

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

	# above completed		

	def collapse_list_of_sets_into_module_order(self):
		return [m for subset in self.module_order for m in subset]
		
	def run_pipeline(self):
		has_been = list()
		#TODO
		for m in self.running_order:
			has_been.append(m)
			
			what_i_need_inputs_from = m.which_modules_are_providing_inputs()
			
			for i in what_i_need_inputs_from:
				pass
				#TODO
						


	def parse_information_from_xml(self):
		self.components = self.root.findall(self.namespace+"component")
		self.pipes = self.root.findall(self.namespace + "pipe")


		self.components_dict = self.create_component_dictionary()
		graph, self.all_input_pipes, self.all_output_pipes = self.create_graphs()		
		self.module_order = sort_topologically(graph)
		self.module_order.reverse()

		# NOTE ON VARIABLE_PIPE_pipes
		# IT IS 'OUTPUT' POINTING TO 'INPUT'
			
	
	def read_in_modules(self):
		self.modules = {}
		for c in self.components:
			if c.get('type') == 'module':
				module_file_name = c.get('ref')
				self.modules[module_file_name] = Module(module_file_name, 
				dict(self.all_input_pipes), dict(self.all_output_pipes))
				# creates new dictionaries


	def create_component_dictionary(self):
		# creates a dictionary
		# really simply, just maps m1 to module1.xml
		ret_dict = dict()
		for component in self.components:
			if component.get('type') == "module":
				key = component.get('name')
				reference = component.get('ref')
			
				ret_dict[key] = reference
		return ret_dict

	def create_graphs(self):
		graph = dict()
		all_input_pipes = dict()
		all_output_pipes = dict()

		for pipe in self.pipes:
			start = pipe.find(self.namespace + "start")
			end = pipe.find(self.namespace + "end")
		
			o_component = start.get("component")
			i_component = end.get("component")
			
			o_component = self.components_dict[o_component]
			i_component = self.components_dict[i_component]

			o_variable = start.get("output")
			i_variable = end.get("input")

			all_input_pipes[(i_component, i_variable)] = (o_component, o_variable)
			all_output_pipes[(o_component, o_variable)] = (i_component, i_variable)

			if o_component in graph:
				# append to existing array
				graph[o_component].append(i_component)
			else:
				# create a new array in this slot
				graph[o_component] = [i_component]

		return graph, all_input_pipes, all_output_pipes


class Module:
	def __init__(self, xml_file, input_pipes, output_pipes):
		if not os.path.isfile(xml_file):
			raise IOError("That is not a file you fucking jerk.")

		self.xml_file = xml_file

		self.setup_tree()
		self.setup_namespace()	
		self.setup_root()

		self.parse_information_from_xml()

		self.input_pipes = self.filter_pipes(input_pipes)
		self.output_pipes = self.filter_pipes(output_pipes)

		# makes them specific to Modules!
		self.filter_pipes(self.input_pipes)
		self.filter_pipes(self.output_pipes)		
		
		
	def filter_pipes(self, pipes):
		new_pipes = {}
		for key, value in pipes.items():
			if key[0] == self.xml_file:
				new_pipes[key] = value
		return new_pipes

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
		
		# These are still elements tho
		self.inputs = self.root.findall(self.namespace + "input")
		self.outputs = self.root.findall(self.namespace + "output")
		
		self.input_types, self.input_names = self.create_types_and_names(self.inputs)
		self.output_types, self.output_names = self.create_types_and_names(self.outputs)

		

	def search_inside_tag(self, tag, attribute):
		return self.root.find(self.namespace + tag).get(attribute)
	
	def __str__(self):
		return etree.tostring(self.tree,pretty_print=True)

	def create_types_and_names(self, elements):
		types = []
		names = []
		for e in elements:
			types.append(e.get("type"))
			names.append(e.get("name"))

		return types, names


	def which_modules_are_providing_inputs(self):
		unique_modules = set()
	
		for me, them in self.input_pipes:
			unique_modules.add(them[0])

		return list(unique_modules)

	def which_modules_am_i_passing_outputs_to(self):
		unique_modules = set()
	
		for me, them in self.output_pipes:
			unique_modules.add(them[0])

		return list(unique_modules)


	# TODO 	
	def run_file(self, run_file, other=None):
		# get in the 'input' variables from pipes!
		pre_locals = {}

		
		# filter pre_locals
		
		# combine them locals!
		for key in pre_locals:
			locals()[key] = pre_locals[key]

		# run the file!
		execfile(run_file)
	
		self.save_locals = locals()
				

	


simple_pipe  = Pipeline("pipe.xml")
m1 = simple_pipe.modules['module1.xml']

