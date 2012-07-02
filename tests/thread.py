#!/usr/bin/env python
#coding:utf8

from threading import Thread
from time import sleep
from os import system as run

l=[1, 2, 3]

class MyThread(Thread, object):
	def __init__(self, name):
		Thread.__init__(self,name=name)

	def run(self):
		name=self.getName()
		print "start:", name
		print name, l
		l[0]=name
		print name, l
		print
		sleep(3)
	
	def __del__(self):
		print 'stop:', self.getName()

if __name__=='__main__':
	for i in range(10):  
		obj = MyThread('thread %d' % i)
		obj.start()
		


