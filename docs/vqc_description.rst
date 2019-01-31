
.. _vqc_description:

Introduction to Quantum Classifiers
===================================

Main Components
^^^^^^^^^^^^^^^

The main data structure describing the quantum classifier setting is in `qclassifier.py`. The implementation allows for modular design of the following components of a quantum classifier (Figure 1): 

1. **Encoder**: transforms a classical data vector into a quantum state. See `encoder.py`.

	+ 1.1 **Classical preprocessor**: maps an input data vector to circuit parameters. See `preprocessing.py`.
    
    + 1.2 **Quantum state preparation**: applies the parametrized circuit to an all-zero input state to generate a quantum state encoding the input data. See `encoding_circ.py`.
    
2. **Processor**: extracts classical information from the encoded quantum state. See `processor.py`.

    + 2.1 **Quantum state transformation**: applies a parametrized circuit to the encoded quantum state to transform it into a form more amenable for information extraction by measurement and classical postprocessing. See `proc_circ.py`.
    
    + 2.2 **Information extraction**: extract classical information from the output quantum state. See `postprocessing.py`.
    
      - 2.2.1 **Measurement**: repeatedly run the quantum circuit, perform measurements and collect measurement statistics
        
      - 2.2.2 **Classical postprocessing**: Glean information from the measurement statistics and produce the output label of the quantum classifier.


Examples
^^^^^^^^

We provide a Jupyter notebook to demonstrate the utility of QClassify. 

.. csv-table::
   :header: Notebook, Feature(s)

   `qclassify_demo.ipynb <https://github.com/zapatacomputing/QClassify/blob/master/examples/qclassify_demo.ipynb>`__, Uses a simple two-qubit circuit to learn the XOR dataset. 


How to cite QClassify
^^^^^^^^^^^^^^^^^^^^^

When using QClassify for research projects, please cite:

	Sukin Sim, Yudong Cao, Jonathan Romero, Peter D. Johnson and Alán Aspuru-Guzik.
	*A framework for algorithm deployment on cloud-based quantum computers*.
	`arXiv:1810.10576 <https://arxiv.org/abs/1810.10576>`__. 2018.