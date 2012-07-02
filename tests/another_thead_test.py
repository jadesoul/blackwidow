#!/usr/bin/env python
#coding:utf8

from threading import Thread
from time import sleep
from os import system as run

urls=['http://www.abc.com/%d.html' % i for i in xrange(10)]
id=0
def get_url():
	global id
	id=(id+1)%10
	return urls[id]

class MyThread(Thread, object):
	def __init__(self, name):
		Thread.__init__(self,name=name)

	def run(self):
		name=self.getName()
		print "start:", name
		print name, get_url()
		print
		#sleep(1)
	
	def __del__(self):
		name=self.getName()
		print 'stop:', name
		print name, get_url()
		print


if __name__=='__main__':
	for i in range(4):  
		obj = MyThread('thread %d' % i)
		obj.start()
		
	raw_input()

