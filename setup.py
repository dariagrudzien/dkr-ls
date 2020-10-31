# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path
import sys

here = path.abspath(path.dirname(__file__))

dependencies = [
    'appdirs==1.4.4',
    'astroid==2.4.2',
    'certifi==2020.6.20',
    'distlib==0.3.1',
    'filelock==3.0.12',
    'isort==5.4.2',
    'lazy-object-proxy==1.4.3',
    'mccabe==0.6.1',
    'pipenv==2020.8.13',
    'pylint==2.6.0',
    'six==1.15.0',
    'toml==0.10.1',
    'virtualenv==20.0.31',
    'virtualenv-clone==0.5.4',
    'wrapt==1.12.1',
    'yapf==0.30.0'
]

setup(
    name='dkr-ls',
    version='0.0.1',
    description='CLI listing docker images in the local registry.',
    long_description='CLI listing docker images in the local registry.',

    # The project's main homepage.
    url='https://github.com/dariagrudzien/dkr-ls',

    # Author details
    author='Daria Grudzien',

    # Choose your license
    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],

    keywords='Docker, docker images',
    packages=find_packages(),
    install_requires=dependencies,
    entry_points={'console_scripts': [
        'dkrls=dkrls:main',
        ],
    },
)
