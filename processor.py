from proc_circ import *
from postprocessing import *

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
		'postprocessing':measure_top0, # see postprocessing.py
	}

	def __init__(self, params, qubits_chosen,\
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
				postprocessing: function handle
					Name of a function which extracts 
					classical information from the output
					state of the processor.

		"""
		
		self.processor = options['proc_circ']
		self.postprocessing = options['postprocessing']
		self.params = params
		self.circuit = self.processor(params, nqubits)+\
				self.postprocessing(qubits_chosen[0])

