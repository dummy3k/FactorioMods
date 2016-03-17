#!/usr/bin/env python

#from distutils.core import setup
from setuptools import setup	#https://github.com/django-extensions/django-extensions/issues/92

setup(name='FactorioMods',
      version='0.1',
      description='Read factoriomods.com/recently-updated and update git repo',
      author='Dummy3k',
      author_email='l4711@gmx.net',
      # url='https://github.com/dummy3k/to_be_done',
      packages=['FactorioMods'],
      scripts=['scripts/fm_update.py'],
	  install_requires=[
          'colorlog', 
		  'coloredlogs', 
      ],
     )