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
	],
	entry_points='''
		[console_scripts]
		draft=draft:draft
	''',
)
