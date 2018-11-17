
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

from qclassify.proc_circ import *
from qclassify.postprocessing import *

class QProcessor(object):

	"""
	Base class for quantum processor which extracts information from a 
	quantum state and produces a classical output, as part of the quantum
	classifier.
	"""

	# Default setting for the quantum processor. See __init__ for detailed
	# explanations
	QPROC_OPTIONS_DEFAULT={
		'proc_circ':layer_xz,	# see proc_circ.py
		'postprocessing':{
			'quantum':measure_top, # see postprocessing.py
			'classical':prob_one, # see postprocessing.py
		}
	}

	def __init__(self, params, qubits_chosen,
	             options=QPROC_OPTIONS_DEFAULT):

		"""
		Initializes an instance of quantum processor.

		Args:
			params: list[float]
				A list of parameters used for the processing
				circuit.
			qubits_chosen: list[int]
				List of indices for the qubits that the circuit
                                acts on.
			options: dictionary
				Further information about the choice of the
				quantum encoding scheme. Entries include
				proc_circ: function handle
					Name of a function which processes the
					quantum state encoding the input data
					into another state which is amenable for
					further information extraction.
				postprocessing: dictionary
					Set of functions which extract
					classical information from the output
					state of the processor. This contains
					quantum: function handle 
						The measurement operations.
					classical: function handle 
						Any function that processes
						the measurement outcomes.

		"""
		
		self.qubits_chosen = qubits_chosen	
		self.processor = options['proc_circ']
		self.postprocessing = options['postprocessing']

		self.quantum_post = self.postprocessing['quantum']
		self.classical_post = self.postprocessing['classical']

	def circuit(self, params):
		
		"""
		Generates the circuit for a given parameter assignment.

                Args:
                        params: list[float]
                                A list of parameters used for the processing
                                circuit.
		"""

		self.params = params
		self.qcircuit = self.processor(params,self.qubits_chosen) + self.quantum_post(self.qubits_chosen[0])

		return self.qcircuit
