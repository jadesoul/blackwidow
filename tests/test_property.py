#coding:utf8

from libjade import *
		
class test(object):
	def __init__(this, conf):
		this.conf=conf
		
	def __getattr__(this, name):
		if name[0]=='_': return name
		return this.conf.get(name, 'no value')

if __name__=='__main__':
	a=test({'a':1, 'v':2})
	print a.__init__
	print a.abc
	print a.a
	print a.v
	print a.x
	a.x=1
	print a.x

