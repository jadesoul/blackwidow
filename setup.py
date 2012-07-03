#!/usr/bin/env python
#coding:utf8

from distutils.core import setup
from os import listdir
from os.path import isfile

fs=filter(isfile, ['scripts/'+i for i in listdir('scripts')])
print fs
print fs

setup(
	name='blackwidow',
	version='1.0',
	description='Jadesoul\'s Python Spider Library',
	author='Jaden Wu',
	author_email='wslgb2006@gmail.com',
	url='http://jadesoul.sinaapp.com/',
	license='Python Software Foundation License',
	packages=['blackwidow'],
	scripts=fs,
)

