
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

from qclassify.preprocessing import *
from qclassify.encoding_circ import *

class QEncoder(object):

	"""
	Base class for a quantum circuit which encodes classical data into a
	quantum state.
	"""

	# Default setting for the quantum encoder. See __init__ for detailed
	# explanations
	QENCODER_OPTIONS_DEFAULT={
		'preprocessing':id_func, 	# see preprocessing.py
		'encoding_circ':x_product,     	# see encoding_circ.py
	}

	def __init__(self, qubits_chosen, options=QENCODER_OPTIONS_DEFAULT):

		"""
		Initializes an instance of quantum encoder.

		Args:
			qubits_chosen: list[int]
				List of indices for the qubits that the circuit
				acts on.
			options: dictionary
				Further information about the choice of the
				quantum encoding scheme. Entries include
				preprocessing: function handle
					Name of a function which preprocesses
					the input vector into another vector
					which is perhaps more suitable for
					quantum circuit construction.
				encoding_circ: function handle
					Name of a function which takes a
					vector and returns a circuit (a pyquil
					Program object).

		"""

		self.qubits_chosen = qubits_chosen
		self.preprocessor = options['preprocessing']
		self.generator = options['encoding_circ']

	def circuit(self, input_vec):

		"""
		Generates the circuit for a particular input vector.

		Args:
			input_vec: list[float]
				An input vector representing the classical data
				point to be encoded.

		"""

		self.__input_vec = self.preprocessor(input_vec)
		self.qcircuit = self.generator(self.__input_vec,\
					self.qubits_chosen)
		return self.qcircuit
