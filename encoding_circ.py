"""
Generators of quantum circuits which encodes a classical input vector into a
quantum state.
"""

from pyquil.gates import *
from pyquil.quil import Program

def x_product(input_vec, qubits_chosen):

	"""
	Encoding circuit which represents a classical vector
		(t1, t2, ..., tn)
	with an n-qubit product state
		Rx(t1)|0> Rx(t2)|0> ... Rx(tn)|0>.

	Args:
		input_vec: list[float]
			Classical input vector.
		qubits_chosen: list[int]
			List of indices of qubits that are chosen for the
			circuit to act on.

	Returns:
		A pyquil Program representing the circuit.
	"""

	out = Program()
	for i in range(0, len(qubits_chosen)):
		out = out + Program(RX(input_vec[i], qubits_chosen[i]))
	return out
