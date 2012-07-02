#coding:utf8

from common import *
from parser import *
from fetcher import *

def start(conf):
	for name, dp in dirs.items():
		if not exists(dp): md(dp)
	
	parser=Parser(conf)
	parser.start()
	
	options=Options(conf)
	num_fechers=options.num_fechers
	
	for fetcher_id in xrange(num_fechers):
		fetcher=Fetcher(conf, fetcher_id)
		fetcher.start()
		
if __name__=='__main__':
	pass
	

