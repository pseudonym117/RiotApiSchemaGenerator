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

    description='RiotApiSchemaGenerator creates JSON schema files by scraping the Riot Games API Reference page',
    long_description=open(descr_file).read(),
    author='AG Stephan',
    url='https://github.com/pseudonym117/RiotApiSchemaGenerator',
    classifiers=[
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    license='Mozilla Public License 2.0 (MPL 2.0)',
    install_requires=requirements,
 )
