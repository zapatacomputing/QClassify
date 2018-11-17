
##############################################################################
# Copyright 2018 Yudong Cao and Zapata Computing, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
##############################################################################

from scipy.optimize import minimize
from numpy.random import uniform
from math import pi

import matplotlib.pyplot as plt
from matplotlib import cm
from pyquil.api import get_qc

from qclassify.encoder import *
from qclassify.processor import *
from qclassify.training import *

# Training data set
from qclassify.xor_example import *

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
		Generates and updates the quantum circuit for the classifier.

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
		qnn_native_circuit = forest_cxn.compiler.\
				quil_to_native_quil(qnn_wrapped_circuit)
		qnn_circuit_executable = forest_cxn.compiler.\
				native_quil_to_executable(qnn_native_circuit)

		# Execute circuit
		result = forest_cxn.run(qnn_circuit_executable)

		# Postprocess the measurement outcomes
		output = self.classical_post(result)

		return output

	# setting for testing the classifier on a testing set
	test_options = {
		'objective_func': crossentropy, # See training.py
	}

	def test(self, data_set, options=test_options):

		"""
		Tests a classifier on a given set of testing data.

		Args:
			data_set: list[(list,{0,1})]
				A list of tuples (feature, label) where feature
				is a list of floats describing the data vector
				and label is a discrete output value which is
				0 or 1.
			options: dictionary
				More information about the testing process.
				Entries include
				objective_func: function handle
                                        Function which evaluates how well the
                                        classifier performs on the data set.
		"""

		objective_func = options['objective_func']

		data_computed = []
		for i, tuple in enumerate(data_set):
                        input_vec = tuple[0]
                        self.circuit(input_vec, self.params)
                        output = self.execute()
                        new_tuple = (input_vec, tuple[1], output)
                        data_computed.append(new_tuple)

		out = objective_func(data_computed)
                
		return out

	# settings for training the variational classifier
	train_options={
		'training_data':XOR_TRAINING_DATA, # Example. See xor_example.py
		'objective_func':crossentropy,	# See training.py
		'training_method':'nelder-mead',
		'init_params':[3.0672044712460114, 3.3311348339721203],
		'maxiter':20,
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

		self.training_data = options['training_data']
		self.objective_func = options['objective_func']
		self.training_method = options['training_method']
		self.init_params = options['init_params']

		training_data = self.training_data
		objective_func = self.objective_func
		training_method = self.training_method
		init_params = self.init_params

		# Wrapper for the optimization
		def targetfunc(params):
			self.params = params
			return self.test(training_data)

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

	# setting for plotting decision boundary of the classifier for a chosen
	# pair of features (limited to 2D plots)
	plot_db_options = {
		'nmesh':10,	# number of grid points
		'xmin':-pi,	# boundary
		'xmax':pi,
		'ymin':-pi/2,
		'ymax':3*pi/2
	}

	def plot_decision_boundary(self, input_vec, features_chosen,\
					filename, options=plot_db_options):

		"""
		For a pair of features, plot the decision boundary of the
		classifier at its current setting.

		Args:
			input_vec: list[float]
				List of floats representing the features of a
				data point.
			features_chosen: list[int]
				List of indices of the two features chosen for
				the plot.
			filename: string
				Name of the exported file for the plot. This
				includes file name extensions.
			options: dictionary
				More information specifying the plot, including
				nmesh: int
					Number of grid points in each dimension
					for generating the plot.
				xmin, xmax, ymin, ymax: float
					Range of the plot along each axis.
		"""

		nmesh = options['nmesh']
		xmin = options['xmin']
		xmax = options['xmax']
		ymin = options['ymin']
		ymax = options['ymax']

		rangex = np.linspace(xmin, xmax, nmesh)
		rangey = np.linspace(ymin, ymax, nmesh)

		range_inputs = []
		func_vals = []

		for y in rangey:
			for x in rangex:
				range_inputs = range_inputs + [[x,y]]
				input_vec[features_chosen[0]] = x
				input_vec[features_chosen[1]] = y
				self.circuit(input_vec, self.params)
				func_vals = func_vals + [self.execute()]

		# Plot the decision boundaries
		x = list(np.kron(rangey, [1 for i in range(0, nmesh)]))
		X, Y = np.meshgrid(rangex, rangey)
		Z = np.reshape(func_vals, [nmesh, nmesh])

		levels = np.arange(-3.5, 3.5, 0.1)
		norm = cm.colors.Normalize(vmax=abs(Z).max(),\
					vmin=-abs(Z).max())
		cmap = cm.PRGn
		plt.contourf(X, Y, Z, levels,\
			cmap=cm.get_cmap(cmap, len(levels) - 1), norm=norm)

		# Plot sets with different labels
		training_data = self.train_options['training_data']
		group0 = [x[0] for x in training_data if x[1]==0]
		group1 = [x[0] for x in training_data if x[1]==1] 

		plt.scatter([x[0] for x in group0], [x[1] for x in group0],\
			c="r")
		plt.scatter([x[0] for x in group1], [x[1] for x in group1],\
			c="b")

		#plt.rc('text', usetex=True)
		plt.rc('font', family='serif')

		plt.xlabel(r'$\theta_0$',fontsize=16)
		plt.ylabel(r'$\theta_1$',fontsize=16)

		plt.savefig(filename)
		plt.show()
		
