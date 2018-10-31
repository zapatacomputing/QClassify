from encoder import *
from processor import *

class QClassifier(object):

	"""
	Base class for quantum classifier.
	"""
	
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

	def circuit(self, input_vec, params):

		"""
		Generates the quantum circuit for the classifier.

		Args:
                        input_vec: list[float]
                                A vector of input data.
                        params: list[float]
                                A vector of parameters for the processor.
		"""

		self.qencoder = QEncoder(self.qubits_chosen,\
					self.qencoder_options)
		self.qproc = QProcessor(params, self.qubits_chosen,\
					self.qproc_options)

		self.circuit = self.qencoder.circuit(input_vec) +\
			self.qproc.circuit(params)

		return self.circuit	
