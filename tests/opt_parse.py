#!/usr/bin/env python

from optparse import OptionParser

# parser=OptionParser(usage="%prog [-f] [-q]", version="%prog 1.0")  
parser=OptionParser(version="%prog 1.0")  
parser.add_option("-g", "--file1", action="store", type="string", dest="filename1")  
parser.add_option("-f", "--file", dest="filename", help="write report to FILE", metavar="FILE")
parser.add_option("-q", "--quiet", action="store_false", dest="verbose", default=True, help="don't print status messages to stdout")
parser.add_option("-n", type="int", dest="num")
parser.add_option("-v", action="store_true", dest="verbose", help="print status messages to stdout")  

(options, args) = parser.parse_args()

if len(args) != 1:  
	parser.error("incorrect number of arguments")  
	
print options
print type(options)
print options.filename
print options.verbose
print
print args
print type(args)




s=('''a'''
'''b''')

print s













