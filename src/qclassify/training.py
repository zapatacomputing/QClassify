
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

from math import log

def crossentropy(training_data_computed):

	"""
	For a given training data set where the classifier has already been
	executed for each data point, producing probability of being 1.

	Args:
		training_data_computed: list[(list,{0,1},float)]
			A list of 3-tuples (feature, label, classifier output)
			where the feature is list of floats, label is a 0-1
			variable and classifier output is a float between 0 and
			1 representing the probability of returning 1.
	
	Returns:
		Cross entropy loss: 
			-t ln y - (1-t) ln(1-y)
		where t={0,1} is the label and y is a float between 0 and 1 that
		is the output of the classifier.
	"""

	def log_(input):
		if input<=0:
			return log(0.0001)
		else:
			return log(input)

	out = 0
	for tuple in training_data_computed:
		label = tuple[1]
		output = tuple[2]
		out = out + (-label * log_(output) - (1-label) * log_(1-output))
	out = out / len(training_data_computed)

	return out
