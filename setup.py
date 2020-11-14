# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path
import sys

here = path.abspath(path.dirname(__file__))

dependencies = [
    'certifi==2020.6.20',
    'chardet==3.0.4',
    'docker==4.3.1',
    'idna==2.10',
    'python-dateutil==2.8.1',
    'requests==2.24.0',
    'six==1.15.0',
    'urllib3==1.25.10',
    'websocket-client==0.57.0'
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

    keywords='Docker, docker images, CLI',
    packages=find_packages(),
    install_requires=dependencies,
    entry_points={'console_scripts': [
        'dkrls=dkrls:main',
        ],
    },
)
