"""Build with
   > py setup.py sdist"""

from setuptools import setup, find_packages
from os.path import join, dirname
from rstring import __version__

setup(
    name = 'rstring',
    version = __version__,
    packages = find_packages(),
    long_description = open(join(dirname(__file__), 'README.md')).read(),
    install_requires=[
          'pytest',
          'ruption @ https://github.com/phantie/ruption/archive/master.zip#egg=option-1.3'
      ]
)