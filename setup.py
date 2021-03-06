"""Build with
   > py setup.py sdist"""

from rstring import __version__

from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name = 'rstring',
    version = __version__,
    packages = find_packages(),
    long_description = open(join(dirname(__file__), 'README.md')).read(),
    install_requires=[
          'take @ https://github.com/phantie/take/archive/1.0.zip',
          'ruption @ https://github.com/phantie/ruption/archive/master.zip#egg=option-1.3',
      ]
)