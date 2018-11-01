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

	out = 0
	for tuple in training_data_computed:
		label = tuple[1]
		output = tuple[2]
		out = out + (-label * log(output) - (1-label) * log(1-output))
	out = out / len(training_data_computed)

	return out
