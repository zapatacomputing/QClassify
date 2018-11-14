
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

"""
Generators of quantum circuits which represents a method for transforming a
quantum state into a form suitable for further postprocessing.

Template assumed for each function:

function_name(params, qubits_chosen, nlayers, options)

	params: list[float]
		A list of parameters used for the circuit.
	qubits_chosen: list[int]
        	List of indices for the qubits that the circuit acts on.
	nlayers: int
                Number of layers.
        options: dictionary
                Further information specifying the details of the variational 
		circuit.
"""

from pyquil.gates import *
from pyquil.quil import Program

LAYER_XZ_OPTIONS_DEFAULT={
	'nlayers': 1,
	'dist': 1,
}

def layer_xz(params, qubits_chosen, options=LAYER_XZ_OPTIONS_DEFAULT):

	"""
	Variational circuit alternating between single-X rotations and constant
	distance controlled-Z gates (see Schuld et al. arXiv:1804.00633 
	[quant-ph]).

	Args:
		params: list[float]
			A list of parameters used for the circuit.
		qubits_chosen: list[int]
			List of indices for the qubits that the circuit acts on.
		options: dictionary
			Further information specifying the details of the
			variational circuit. Entries include
			nlayers: int
				Number of layers.
			dist: int
				Distance between the control and target qubits.
				See the 'r' parameter in (Fig. 4, Schuld et al).

	Return:
		A pyquil Program object representing the circuit.
	"""

	out = Program()
	nlayers = options['nlayers']
	dist = options['dist']

	# iterate through the layers
	for i in range(0, nlayers):

		# controlled-z gate layer
		out = out + layer_controlled_z(qubits_chosen, dist)

		# single-x gate layer
		out = out + layer_single_x(params, qubits_chosen)

	return out

def layer_single_x(params, qubits_chosen):

	"""
	A layer of single X rotations.

	Args:
		params: list[float]
			Rotation angles for each qubit.
		qubits_chosen: list[int]
			List of indices of the qubits that current layer acts
			on.

	Return:
		A pyquil Program object representing the circuit layer.
	"""

	output = Program()
	nqubits = len(qubits_chosen)

	for i in range(0, nqubits):
		output = output + Program(RX(params[i], qubits_chosen[i]))

	return output

def layer_controlled_z(qubits_chosen, distance):

	"""
	An entangling layer which applies CZ gate on pairs of qubits that are
	separated by a specified distance.

	Args:
		qubits_chosen: list[int]
			List of indices of qubits that current layer acts on.
		distance: int
			Distance between the control and the target qubit for
			each CZ gate.

	Return:
		A pyquil Program object representing the circuit layer.
	"""

	out = Program()
	nqubits = len(qubits_chosen)

	if nqubits == 2:
		return Program(CZ(qubits_chosen[0], qubits_chosen[1]))

	for i in range(0, nqubits):
		out = out + Program(CZ(qubits_chosen[i],
		                       qubits_chosen[(i+distance) % nqubits]))
	
	return out
