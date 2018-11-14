
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
Methods for extracting classical information from the output state of the
quantum processor.
"""

from pyquil.gates import *
from pyquil.quil import Program

import numpy as np

## Quantum step ##

def measure_top(qubit_chosen):

	"""
	Extract information from a quantm state by measuring the probability
	that the chosen qubit is in |0> state.

	Args:
		qubit_chosen: int
			Index of the qubit to be measured.

	Returns:
		Measurement operation.
	"""

	out = Program()
	ro = out.declare('ro', memory_type='BIT', memory_size=1)
	out = out + MEASURE(qubit_chosen, ro[0])
	return out

## Classical steps for processing measurement outcomes ##
# Here we assume that the outcomes are a list of lists containing 0, 1 values

def prob_one(qubit_outcome):

	"""
	Computes the probability of measuring |1> in a given qubit.

	Args:
		qubit_outcome: list[{0,1}]
			A list of 0, 1 values representing the outcomes of
			repeated measurement.
	"""

	# in case the input is not a list but a list of lists
	input_vec = np.asarray(qubit_outcome)
	input_vec.shape = input_vec.size

	return sum(input_vec)/len(input_vec)
