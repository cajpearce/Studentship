from lxml import etree
from topological_sort import sort_topologically
import rpy2.robjects as robjects
import os


class GetXMLStuff(object):
	'''
	This is a class that sets up the very basic necessities of the XML.
	I created it as a class because the set up for an XML object is the same
	For both a Pipeline and a Module in OpenAPI.
	'''
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

	def setup_namespace(self):
		temp_namespace = self.tree.getroot().nsmap
		self.namespace = "{" + temp_namespace[None] + "}"

	def setup_root(self):
		self.root = self.tree.getroot()



class Pipeline(GetXMLStuff):
	def __init__(self, xml_file):
		GetXMLStuff.__init__(self, xml_file)
		
		self.parse_information_from_xml()
		

	def collapse_module_order_list(self, module_order):
		# after topological sort, it is set up as a list of sets
		# this method collapses down to a single (ordered) list
		return [m for subset in module_order for m in subset]
			
	def read_in_modules(self, components):
		# read in modules as a dictionary, with the xml file name
		# pointing to the object -> 'module1.xml': Module()
		modules = {}
		for c in components:
			if c.get('type') == 'module':
				xml_file = c.get('ref')
				modules[xml_file] = Module(xml_file)
		
		return modules

	def component_dictionary(self, components):
		# creates a really simple dictionary -> maps m1 to module1.xml
		ret_dict = dict()
		for component in components:
			if component.get('type') == "module":
				key = component.get('name')
				reference = component.get('ref')
			
				ret_dict[key] = reference
		return ret_dict

	def parse_information_from_xml(self):
		# 1. gets all the components and pipes
		components = self.root.findall(self.namespace+"component")
		pipes = self.root.findall(self.namespace + "pipe")
		
		# 2. reads in the modules
		self.modules = self.read_in_modules(components)
		
		# 3. gets the order and the pipeline connections
		graph, self.all_input_pipes, self.all_output_pipes = self.create_graph(pipes, components)	
		# 4. for all modules passes them their pipes
		self.set_module_pipes(self.modules)		

		# 5. reverses, sorts, and collapses the order
		order = sort_topologically(graph)
		order.reverse()		
		self.module_order = self.collapse_module_order_list(order)

	def set_module_pipes(self, modules):
		# passes the complete set of pipes to each module (each module
		# sorts them themselves)
		for xml_file, m in modules.items():
			m.set_pipes(dict(self.all_input_pipes), 
				dict(self.all_output_pipes))

	def create_graph(self, pipes, components):
		# creates the pipe connections and the node graph
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

	def validate_pipeline(self):
		# only checks XML validity
		# checks it by checking pipes against the modules
		# TODO: back check modules against pipes
		test = []
		for me, them in self.all_input_pipes.items():
			test.append(me[1] in me[0].input_dict)
			test.append(them[1] in them[0].output_dict)

		for me, them in self.all_output_pipes.items():
			test.append(me[1] in me[0].output_dict)
			test.append(them[1] in them[0].input_dict)
	
		return all(test)


	def run_pipeline(self):
		# checks the validity, then in order runs the modules
		if self.validate_pipeline():

			for m in self.module_order:
				m.run()


class Module(GetXMLStuff):
	def __init__(self, xml_file):
		GetXMLStuff.__init__(self, xml_file)
		
		self.parse_information_from_xml()

		# logical indicator
		self.has_file_been_run = False
	
	def create_dictionary_marker(self, variable_name):
		# combines self reference with variable name
		# input/output pipes are stored as (Module(), 'variable')
		return (self, variable_name)
	
	def get_variable_from_other_module(self, variable_name):
		ref = self.create_dictionary_marker(variable_name)
		other = self.input_pipes[ref]
		
		return other[0].get_variable_from_locals(other[1])

	def get_all_input_variables(self):
		return {i: self.get_variable_from_other_module(i) for i in self.input_dict}
		
	def set_pipes(self, input_pipes, output_pipes):
		''' this function must be used'''
		self.input_pipes = self.filter_pipes(input_pipes)
		self.output_pipes = self.filter_pipes(output_pipes)

		self.incoming_modules= self.which_modules_are_providing_inputs()
		self.outgoing_modules = self.which_modules_am_i_passing_outputs_to()

	def filter_pipes(self, pipes):
		new_pipes = {}
		for key, value in pipes.items():
			if key[0] is self:
				new_pipes[key] = value
		return new_pipes

	def parse_information_from_xml(self):
		self.run_file = self.search_inside_tag("source","ref")
		self.platform = self.search_inside_tag("platform","name")
		
		input_elements = self.root.findall(self.namespace + "input")
		output_elements = self.root.findall(self.namespace + "output")
		
		self.input_dict = self.create_var_type_dict(input_elements)
		self.output_dict = self.create_var_type_dict(output_elements)


	def which_modules_are_providing_inputs(self):
		unique_modules = set()
	
		for me, them in self.input_pipes.items():
			unique_modules.add(them[0])


		return list(unique_modules)

	def which_modules_am_i_passing_outputs_to(self):
		unique_modules = set()
	
		for me, them in self.output_pipes.items():
			unique_modules.add(them[0])

		return list(unique_modules)

	def run(self):
		if self.platform.lower() == "python":
			self.run_py_script(self.run_file,self.get_all_input_variables())
		elif self.platform.lower() == "r":
			self.run_R_script(self.run_file, self.get_all_input_variables())


	def run_R_script(self, run_file, pre_locals):		
		r_file = open(run_file, 'r')
		r_script = r_file.read()
		r_file.close()
	
		robjects.r("rm(list=ls())")

		for key in pre_locals:
			robjects.globalenv[key] = pre_locals[key]

		robjects.r(r_script)

		self.save_locals = {i: robjects.globalenv[i] for i in self.output_dict}
		self.has_file_been_run = True


	def run_py_script(self, run_file, pre_locals):
		print "running " + run_file + "..."
		for key in pre_locals:
			locals()[key] = pre_locals[key]

		# run the file!
		try:
			execfile(run_file)
		except NameError, e:
			err_string = "ERROR: You have not provided all inputs: " 
			print err_string + str(e)
		except TypeError, e:
			err_string = "ERROR: You may have connected the wrong pipes: "
			print err_string + str(e)
		
		self.save_locals = locals()		
		self.has_file_been_run = True
			
	def get_variable_from_locals(self, variable_name):
		if self.has_file_been_run:
			return self.save_locals[variable_name]
		else:
			raise AttributeError("You need to run the file first.")



	def create_var_type_dict(self, elements):
		''' 	for future expansion
			will be useful when I start to allow external inputs '''
		return {e.get("name"): e.get("type") for e in elements}


simple_pipe  = Pipeline("pipe_R.xml")
simple_pipe.run_pipeline()
