
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
XOR dataset example.
"""

import numpy as np

from math import pi

# Training data points labelled 0
group0 = [[-1.8014030885341425, 0.07049090664351776],
          [-1.301866318505309, -0.09006021655705085],
          [-1.2995311803877012, 0.17179375194954777],
          [-1.6844614700570668, 0.26300082528677904],
          [-1.581826822227654, 0.2210431121474794],
          [1.526782533409962, 3.227296155921321],
          [1.6081456320334693, 3.3248683153683958],
          [1.4118513018150587, 3.436121923699187],
          [1.5620769416428386, 3.384965966733096],
          [1.3020823312222616, 3.3163245524916936]]

# Training data points labelled 1
group1 = [[-1.6269012492495667, 2.8732368479226293],
          [-1.5530830764355592, 3.1738353675554416],
          [-1.8513100742724584, 3.2237767325843545],
          [-1.6272074871316728, 3.28878799481208],
          [-1.6612433455383213, 2.879163347517711],
          [1.3798060401258543, -0.09979143378370409],
          [1.6151621300228456, 0.04571164290639079],
          [1.426884637605485, -0.06169454299108834],
          [1.5019812981463012, -0.16369059365023533],
          [1.6204586467622049, -0.10966267374801358]]

XOR_TRAINING_DATA = [(x,0) for x in group0] + [(x,1) for x in group1]

# Function which generates XOR-like test data
def gen_xor(num_points, delta):

	"""
	Function for generating XOR-like test data.

	Args:
		num_points: int
			Number of data points to be generated. Half of them
			will be labelled 0 and the other half 1.
		delta: float
			Range of perturbation. This determines how spread out
			the data points are.

	Returns:
		A list of tuples (list, {0,1}) where the list is the feature
		vector and {0,1} is the label.
	"""

	Ndata = int(num_points/2) # Number of data points per point group
	delta = pi/10 # range of perturbation
	group0 = [[-pi/2 + np.random.uniform(-delta, delta),\
			np.random.uniform(-delta, delta)]\
			for x in range(0, Ndata)] +\
		[[pi/2 + np.random.uniform(-delta,delta),\
			pi+np.random.uniform(-delta, delta)]\
			for x in range(0, Ndata)]
	group1 = [[-pi/2 + np.random.uniform(-delta,delta),\
			pi+np.random.uniform(-delta, delta)]\
			for x in range(0, Ndata)] +\
		[[pi/2 + np.random.uniform(-delta,delta),\
			np.random.uniform(-delta, delta)]\
			for x in range(0, Ndata)]
	return [(x, 0) for x in group0] + [(x, 1) for x in group1]
