from setuptools import setup

setup(
	name='draft',
	version='1.0',
	packages = [ 'draft' ],
	include_package_data=True,
	install_requires=[
		'Click',
		'requests',
		'numpy',
	],
	entry_points='''
		[console_scripts]
		draft=draft:cli
	''',
)
