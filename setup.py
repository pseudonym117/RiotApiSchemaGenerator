from setuptools import setup, find_packages
import os.path

import sys

__version__ = '0.1.0'

descr_file = os.path.join(os.path.dirname(__file__), 'README.rst')

requirements = [
    'requests'
]

setup(
    name='RiotApiSchemaGenerator',
    version=__version__,

    packages=find_packages(exclude=['test']),

    description='RiotApiSchemaGenerator creates JSON schemas by scraping the Riot Games API Refernce page',
    long_description=open(descr_file).read(),
    author='AG Stephan',
    url='https://github.com/pseudonym117/RiotApiSchemaGenerator',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing',
        'Topic :: Games/Entertainment :: Real Time Strategy',
        'Topic :: Games/Entertainment :: Role-Playing'
    ],
    license='MIT',
    install_requires=requirements,
 )
