
import os
from setuptools import setup, find_packages

# This reads the __version__ variable
exec(open('src/qclassify/_version.py').read())

# README file as long_description
long_description = open('README.md').read()

# Read in requirements.txt
requirements = open('requirements.txt').readlines()
requirements = [r.strip() for r in requirements]

setup(
    name='qclassify',
    version=__version__,
    description='A Python framework for the variational quantum classifier',
    long_description=long_description,
    install_requires=requirements,
    url='https://github.com/zapatacomputing/QClassify',
    author='caoyudong',
    author_email='yudong@zapatacomputing.com',
    license='Apache-2.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    zip_safe=False,
    include_package_data=True,
    package_data={
        '': [os.path.join('images', '*.png'),
             os.path.join('images', '*.py')]
    },
    python_requires=">=3.6"
    )
