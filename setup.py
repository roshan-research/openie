
from distutils.core import setup

setup(name='baaz',
	version='0.1',
	description='Open information extraction from Persian web.',
	author='Alireza Nourian',
	author_email='az.nourian@gmail.com',
	url='http://www.sobhe.ir/baaz/',
	packages=['baaz'],
	classifiers=[
		'Topic :: Text Processing',
		'Natural Language :: Persian',
		'Programming Language :: Python :: 3.2',
		'Programming Language :: Python :: 3.3',
		'Programming Language :: Python :: 3.4',
		'License :: OSI Approved :: MIT License',
	],
	install_requires=['hazm']
)
