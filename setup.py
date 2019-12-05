#from distutils.core import setup
from setuptools import setup, find_packages

setup(
	name='draft',
	version='1.0',
	packages = find_packages(),
	include_package_data=True,
	install_requires=[
		'Click',
		'requests',
		'numpy',
		'plotly',
		'colorlover',
                'keras',
                'tensorflow',
                'pydot',
                'GraphViz'
	],
	entry_points='''
		[console_scripts]
                draft=draft.draft:draft
	''',
)
