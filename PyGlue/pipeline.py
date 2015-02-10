from lxml import etree
from topological_sort import sort_topologically
import os

class GetXMLStuff(object):
	def __init__(self, xml_file):
		if not os.path.isfile(xml_file):
			raise IOError("You have provided an invalid XML file.")
		self.xml_file = xml_file

		self.setup_tree()
		self.setup_namespace()	
		self.setup_root()

	def search_inside_tag(self, tag, attribute):
		return self.root.find(self.namespace + tag).get(attribute)

	def __str__(self):
		return self.xml_file

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



class Pipeline(GetXMLStuff):
	def __init__(self, xml_file):
		GetXMLStuff.__init__(self, xml_file)

		self.parse_information_from_xml()

		# self.module_order
		# self.modules
		# self.all_input_pipes
		# self.all_output_pipes
		

	def collapse_module_order_list(self, module_order):
		return [m for subset in module_order for m in subset]
			
	def read_in_modules(self, components):
		modules = {}
		for c in components:
			if c.get('type') == 'module':
				module_file_name = c.get('ref')
				print module_file_name
				modules[module_file_name] = Module(module_file_name)
				# creates new dictionaries
		
		return modules

	def component_dictionary(self, components):
		# creates a dictionary
		# really simply, just maps m1 to module1.xml
		ret_dict = dict()
		for component in components:
			if component.get('type') == "module":
				key = component.get('name')
				reference = component.get('ref')
			
				ret_dict[key] = reference
		return ret_dict

	def parse_information_from_xml(self):
		components = self.root.findall(self.namespace+"component")
		pipes = self.root.findall(self.namespace + "pipe")
		
		self.modules = self.read_in_modules(components)

		graph, self.all_input_pipes, self.all_output_pipes = self.create_graph(pipes, components)	

		self.set_module_pipes(self.modules)		

		order = sort_topologically(graph)
		order.reverse()
		
		self.module_order = self.collapse_module_order_list(order)

	def set_module_pipes(self, modules):
		for xml_file, m in modules.items():
			m.set_pipes(dict(self.all_input_pipes), 
				dict(self.all_output_pipes))

	def create_graph(self, pipes, components):
		graph = dict()
		all_input_pipes = dict()
		all_output_pipes = dict()

		ref_dict = self.component_dictionary(components)
		for pipe in pipes:
			# Elements
			start = pipe.find(self.namespace + "start")
			end = pipe.find(self.namespace + "end")
			
			# m1, m2, etc.
			o_component = start.get("component")
			i_component = end.get("component")
			
			# xml file names
			o_component = ref_dict[o_component]
			i_component = ref_dict[i_component]
			
			# actual module objects
			o_component = self.modules[o_component]
			i_component = self.modules[i_component]
			
	
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


class Module(GetXMLStuff):
	def __init__(self, xml_file):
		GetXMLStuff.__init__(self, xml_file)

		self.parse_information_from_xml()
	
	def set_pipes(self, input_pipes, output_pipes):
		# TODO MUST USE THIS
		#		
	
		self.input_pipes = self.filter_pipes(input_pipes)
		self.output_pipes = self.filter_pipes(output_pipes)
		
	def filter_pipes(self, pipes):
		new_pipes = {}
		for key, value in pipes.items():
			if key[0] is self:
				new_pipes[key] = value
		return new_pipes

	def parse_information_from_xml(self):
		self.run_file = self.search_inside_tag("source","ref")
		self.platform = self.search_inside_tag("platform","name")
		
		# These are still elements tho
		self.inputs = self.root.findall(self.namespace + "input")
		self.outputs = self.root.findall(self.namespace + "output")
		
		#self.input_types, self.input_names = self.create_types_and_names(self.inputs)
		#self.output_types, self.output_names = self.create_types_and_names(self.outputs)


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
				

	#def create_types_and_names(self, elements):
	#	types = []
	#	names = []
	#	for e in elements:
	#		types.append(e.get("type"))
	#		names.append(e.get("name"))
#
#		return types, names


simple_pipe  = Pipeline("pipe.xml")
m1 = simple_pipe.modules['module1.xml']

