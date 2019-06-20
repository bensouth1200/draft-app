from setuptools import setup

setup(
	name='draft',
	version='1.0',
	py_modules=[
		'engine/draft',
		'engine/board',
		'engine/picker',
		'engine/adp_list',
		'engine/pickers/fanboy_picker',
		'engine/pickers/roster_picker',
		'engine/pickers/TE_QB_picker',
		'engine/pickers/user_picker',
		'engine/pickers/vb_picker',
		'engine/pickers/zeroRB_picker',
		'engine/pickers/zeroWR_picker',
	],
	install_requires=[
		'Click',
	],
	entry_points='''
		[console_scripts]
		draft=draft:cli
	''',
)
