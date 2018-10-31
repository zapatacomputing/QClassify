"""
Functions used for preprocessing classical data into forms amenable for quantum
processing.
"""

import sys

def normalize(input_vec):
	norm_constant = sum(input_vec)
	if norm_constant != 0:
		return np.multiply(np.array(state_vec), 1.0/norm_constant)
	else:
		sys.exit("Input vector cannot be normalized. Try a different preprocessing scheme.")
