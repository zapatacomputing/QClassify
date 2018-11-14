
# QClassify


## Description

QClassify is a Python framework for implementing variational quantum classifiers. The goal is to provide a generally customizable way of performing classification tasks using gate-model quantum devices. The quantum devices can be either simulated by a quantum simulator or a cloud-based quantum processor accessible via Rigetti Computing's [Quantum Cloud Services](https://www.rigetti.com/qcs).

Variational quantum classification is a paradigm of supervised quantum machine learning that has been investigated actively in the quantum computing community (See for instance [Farhi and Neven](https://arxiv.org/abs/1802.06002), [Schuld et al.](https://arxiv.org/abs/1804.00633), [Mitarai et al.](https://arxiv.org/abs/1803.00745) and [Havlicek et al.](https://arxiv.org/abs/1804.11326)). The general framework adopted in the design of QClassify follows from these contributions in the literature. The workflow can be summarized in Figure 1 below. 

![Flow chart](https://github.com/zapatacomputing/QClassify/blob/master/images/qclassify.png)
*Figure 1: Diagram illustrating the workflow of QClassify. Each rectangle represents a data object and each oval represents a method.* 



## Main Components

The main data structure describing the quantum classifier setting is in `qclassifier.py`. The implementation allows for modular design of the following components of a quantum classifier (Figure 1): 

1. **Encoder**: transforms a classical data vector into a quantum state. See `encoder.py`.

    + 1.1 **Classical preprocessor**: maps an input data vector to circuit parameters. See `preprocessing.py`.
    
    + 1.2 **Quantum state preparation**: applies the parametrized circuit to an all-zero input state to generate a quantum state encoding the input data. See `encoding_circ.py`.
    
2. **Processor**: extracts classical information from the encoded quantum state. See `processor.py`.

    + 2.1 **Quantum state transformation**: applies a parametrized circuit to the encoded quantum state to transform it into a form more amenable for information extraction by measurement and classical postprocessing. See `proc_circ.py`.
    
    + 2.2 **Information extraction**: extract classical information from the output quantum state. See `postprocessing.py`.
    
      - 2.2.1 **Measurement**: repeatedly run the quantum circuit, perform measurements and collect measurement statistics
        
      - 2.2.2 **Classical postprocessing**: Glean information from the measurement statistics and produce the output label of the quantum classifier.



## Installation

To install QClassify using ``pip``:


	pip install qclassify


Try executing ``import qclassify`` to test the installation in your terminal.


To instead install QClassify from source, clone this repository, ``cd`` into it, and run:

	git clone https://github.com/zapatacomputing/QClassify
	cd QClassify
	python -m pip install -e .

Note that the pyQuil version used requires Python 3.6 or later. For installation on a user QMI, please click [here](https://github.com/hsim13372/QCompress/blob/master/qmi_instructions.rst).


## Examples


We provide a Jupyter notebook to demonstrate the utility of QClassify. 

Notebook | Feature(s)
---------|---------------
   [qclassify_demo.ipynb](https://github.com/zapatacomputing/QClassify/blob/master/examples/qclassify_demo.ipynb) | Uses a simple two-qubit circuit to learn the XOR dataset. 


## Disclaimer

We note that there is a lot of room for improvement and fixes. Please feel free to submit issues and/or pull requests!


## How to cite

When using QClassify for research projects, please cite:

>	Sukin Sim, Yudong Cao, Jonathan Romero, Peter D. Johnson and Alán Aspuru-Guzik.
	*A framework for algorithm deployment on cloud-based quantum computers*.
	[arXiv:1810.10576](https://arxiv.org/abs/1810.10576). 2018.


## Authors

[Yudong Cao](https://github.com/yudongcao),
[Sukin (Hannah) Sim](https://github.com/hsim13372) (Harvard)
