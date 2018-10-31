"""
Methods for extracting classical information from the output state of the
quantum processor.
"""

from pyquil.gates import *
from pyquil.quil import Program

def measure_top0(qubit_chosen):

	"""
	Extract information from a quantm state by measuring the probability
	that the chosen qubit is in |0> state.

	Args:
		qubit_chosen: int
			Index of the qubit to be measured.

	Returns:
		Measurement operation.
	"""

	ro = out.declare('ro', memory_type='BIT', memory_size=1)
	return MEASURE(qubit_chosen, ro[0])
