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
	def parse_information_from_xml(self):
		self.components = self.root.findall(self.namespace+"component")
		self.pipes = self.root.findall(self.namespace + "pipe")


		self.components_dict = self.create_component_dictionary()
		graph, self.variable_pipe_links = self.create_graphs()		
		self.module_order = sort_topologically(graph)
		self.module_order.reverse()
		
		################################################################
		# now we have the module_order: directions
		# we have the variable_pipe_links: refers to inputs
	
	def read_in_modules(self):
		self.modules = []
		for c in self.components:
			if c.get('type') == 'module':
				file_name = c.get('ref')
				self.modules.append(Module(file_name))


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
		pipe_links = dict()

		for pipe in self.pipes:
			start = pipe.find(self.namespace + "start")
			end = pipe.find(self.namespace + "end")
		
			o_component = start.get("component")
			i_component = end.get("component")
			
			o_component = self.components_dict[o_component]
			i_component = self.components_dict[i_component]

			o_variable = start.get("output")
			i_variable = end.get("input")

			pipe_links[(i_component, i_variable)] = (o_component, o_variable)

			if o_component in graph:
				# append to existing array
				graph[o_component].append(i_component)
			else:
				# create a new array in this slot
				graph[o_component] = [i_component]

		return graph, pipe_links


class Module:
	def __init__(self, xml_file):
		if not os.path.isfile(xml_file):
			raise IOError("That is not a file you fucking jerk.")

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
		self.inputs = []
		for i in self.root.findall(self.namespace + "input"):
			self.inputs.append(Input(i))
		self.outputs = []
		for o in self.root.findall(self.namespace + "output"):
			self.outputs.append(Output(o))


	def search_inside_tag(self, tag, attribute):
		return self.root.find(self.namespace + tag).get(attribute)
	
	def __str__(self):
		return etree.tostring(self.tree,pretty_print=True)


	def incoming_pipe(self, other):
		pass
		#TODO
	def outgoing_pipe(self, other):
		pass
		# TODO

		#('plot', 'df'): ('start', 'df')


class Var:
	def __init__(self, element):
		self.breakdown_element(element)

	def breakdown_element(self, e):
		self.variable_type = e.get("type")
		self.variable_name = e.get("name")

	def is_internal(self):
		return self.variable_type == "internal"

	def __str__(self):
		return self.variable_name + "--|--" + self.variable_type

class Input(Var):
	# Easy wrapper
	pass

	def coming_from(self, other):
		if instanceof(other, Output):
			self.connection = other

class Output(Var):
	# Easy wrapper
	def going_to(self, other):
		if instanceof(other, Input):
			self.connection = other



class ModulePy:
	def __init__(self, run_file,input_var_names,output_var_names):
		# python file to run
		self.run_file = run_file

		# create a small list of the incoming and outgoing variables
		# TODO: write these as a dictionary???
		self.input_variable_names = input_var_names
		self.output_variable_names = output_var_names

	def filter_inputs(self, other_dict, input_variable_names):
		# Have to think about how I'm going to process this
		self.start_locals = { k: other_dict[k] for k in input_variable_names}

	def run_file(self, file_name):
		locals()['dataframe1'] = DATAFRAME_FROM_M1
		execfile(file_name)
		self.save_vars = locals()

	def compare_outputs_to_locals(self):
		
simple_pipe  = Pipeline("pipe.xml")
