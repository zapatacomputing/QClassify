from scipy.optimize import minimize
from numpy.random import uniform
from math import pi

from pyquil.api import get_qc

from encoder import *
from processor import *
from xor_example import *
from training import *

class QClassifier(object):

	"""
	Base class for quantum classifier.
	"""
	
	# default setting for different components of the classifier
	QCLASSIFIER_OPTIONS_DEFAULT={
		'encoder_options':QEncoder.QENCODER_OPTIONS_DEFAULT,
		'proc_options':QProcessor.QPROC_OPTIONS_DEFAULT,
	}

	def __init__(self, qubits_chosen, options=QCLASSIFIER_OPTIONS_DEFAULT):

		"""
		Initializes an instance of quantum classifier.

		Args:
			qubits_chosen: list[int]
				List of indices for the qubits that the circuit
                                acts on.
			options: dictionary
				Further information about the construction of
				the quantum classifier.
		"""

		self.qubits_chosen = qubits_chosen
		self.qencoder_options = options['encoder_options']
		self.qproc_options = options['proc_options']

		self.postprocessing = self.qproc_options['postprocessing']
		self.classical_post = self.postprocessing['classical']

	def circuit(self, input_vec, params):

		"""
		Generates the quantum circuit for the classifier.

		Args:
                        input_vec: list[float]
                                A vector of input data.
                        params: list[float]
                                A vector of parameters for the processor.
		"""

		self.params = params
		self.qencoder = QEncoder(self.qubits_chosen,\
					self.qencoder_options)
		self.qproc = QProcessor(params, self.qubits_chosen,\
					self.qproc_options)

		self.qcircuit = self.qencoder.circuit(input_vec) +\
			self.qproc.circuit(params)

		return self.qcircuit

	# setting for executing the circuit
	execute_options={
		'nruns':10000
	}

	def execute(self, options=execute_options):

		"""
		Executes the classifier protocol, including
			* preprocessing
			* data encoding
			* data processing
			* postprocessing

		Returns:
			label: float
				Value between 0 and 1 representing the output
				of the binary classifier.
		"""

		# Set up connection
		forest_cxn = get_qc('9q-generic-qvm')

		nruns = options['nruns']

		# Compile circuit
		qnn_wrapped_circuit = self.qcircuit.wrap_in_numshots_loop(nruns)
		qnn_native_circuit = forest_cxn.compiler.quil_to_native_quil(qnn_wrapped_circuit)
		qnn_circuit_executable = forest_cxn.compiler.native_quil_to_executable(qnn_native_circuit)

		# Execute circuit
		result = forest_cxn.run(qnn_circuit_executable)

		# Postprocess the measurement outcomes
		output = self.classical_post(result)

		return output

	# settings for training the variational classifier
	train_options={
		'training_data':gen_xor(),	# Example. See xor_example.py
		'objective_func':crossentropy,	# See training.py
		'training_method':'nelder-mead',
		'init_params':[3.0672044712460114, 3.3311348339721203],
		'maxiter':5,
		'xatol':1e-3,
		'fatol':1e-3,
		'verbose':True		# Print intermediate values
	}

	def train(self, options=train_options):

		"""
		Train the variational quantum classifier by tuning the
		parameters to optimize an objective function.

		Args:
			options: dictionary
				Information about the implementation of training
				which includes
				training_data: list[(list,{0,1})]
					Training set. List of tuples
						(features, label)
					with features being a list of floats and
					label being a 0, 1 variable.
				objective_func: function handle
					Function which evaluates how well the
					classifier performs on the data set.
				training_method: string
					Name of the method for training the
					parameters.
				...the remaining parameters are dependent on
				training method employed.
		"""

		training_data = options['training_data']
		objective_func = options['objective_func']
		training_method = options['training_method']
		init_params = options['init_params']

		# Wrapper for the optimization
		def targetfunc(params):
			training_data_computed = []		
			for i, tuple in enumerate(training_data):
				input_vec = tuple[0]
				self.circuit(input_vec, params)
				output = self.execute()
				new_tuple = (input_vec, tuple[1], output)
				training_data_computed.append(new_tuple)
			out = objective_func(training_data_computed)
			return out

		# Callback function for displaying progress
		self.Nfeval = 1
		self.min_loss_history = []

		def callback_func(input_params):
			loss = targetfunc(input_params)
			if options['verbose'] == True:
				print(("%4d" % self.Nfeval)+("   %.3f" % loss))
			self.Nfeval = self.Nfeval + 1
			self.min_loss_history.append(loss)

		# Other parameters for optimization
		maxiter = options['maxiter']
		xatol = options['xatol']
		fatol = options['fatol']	   

		if options['verbose'] == True:
			top_bar = 'Iter   Obj'
			print(top_bar)
 
		if training_method == 'bfgs':

			# Optimize the target function
			res = minimize(targetfunc, init_params, args=(),
                                       method='bfgs', tol=1e-2,
                                       callback=callback_func,\
                                       options={'disp': False,
                                                'maxiter': maxiter,
                                                'xatol': xatol,
                                                'return_all': False,
                                                'fatol': fatol})

		if training_method == 'nelder-mead':

			# Compute an initial simplex
			init_simplex = [init_params]
			nparams = len(init_params)
			for x in range(0, nparams):
    				perturbed_params = [y+uniform(-pi, pi)\
						for y in init_params]
    				init_simplex = init_simplex + [perturbed_params]		
			# Optimize the target function
			res = minimize(targetfunc, init_params, args=(),
				       method='Nelder-Mead', tol=1e-2, 
				       callback=callback_func,\
					options={'disp': False,
						'initial_simplex': init_simplex,
						'maxiter': maxiter,
						'xatol': xatol,
						'return_all': False,
						'fatol': fatol})

		# Update the optimized parameters
		self.params = res.x		
