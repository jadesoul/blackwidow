#coding:utf8

from libjade import *
from threading import Thread
import gzip

dir_root=cwd()
dir_pages=join(dir_root, 'pages')
dir_urls=join(dir_root, 'urls')
dir_archive=join(dir_root, 'archive')
dir_state=join(dir_root, 'state')

dirs=smap_dict('dir_root dir_pages dir_urls dir_archive dir_state', locals())

infotxt='.info.txt'
	

def smart_fread(fp):
	'''
	smart read from a text file or a gzip text file
	'''
	try:
		f=gzip.GzipFile(fp)
		data=f.read()
		f.close()
	except:
		data=fread(fp)

	return data

def dump_state():
	jsonwrite(conf, fp_state)

def reload_state():
	global conf
	conf=jsonread(fp_state)
	
def lines2list(s, make_it_unique=True):
	'''
	this function can turn a string consist of serveral lines into a list, empty lines 
	and and comment starting with # in the lines will be ignored, each line will 
	be striped to ensure there is no empty chars on the head or tail of the line
	
	for example:
		abc
		#def
		hij	#klm
	will return ['abc', 'hij']
	'''
	lines=s.strip().split('\n')
	lines=[(l, l.find('#')) for l in lines]
	lines=[l.strip() if i==-1 else l[:i].strip() for l, i in lines]
	items=[l for l in lines if l]
	iset=set(items)
	if not make_it_unique or len(iset)==len(items):
		return items	# to keep the original sequence
	else:
		return list(iset)	# will lost the original sequence
	

def tabs2list(s, make_it_unique=True):
	'''
	this function can turn a string consist of serveral lines into a item list, 
	each line contains some items seperated with tabs or empty chars,
	empty lines and and comment starting with # in the lines will be ignored, 
	each line will be striped to ensure there is no empty chars on the head or 
	tail of the line
	
	for example:
		abc yui
		#def
		hij	poi	#klm
	will return ['abc', 'yui', 'hij', 'poi']
	'''
	lines=s.strip().split('\n')
	lines=[(l, l.find('#')) for l in lines]
	lines=[l.strip() if i==-1 else l[:i].strip() for l, i in lines]
	lines=[l for l in lines if l]
	items=[]
	for line in lines:
		items.extend(line.split())
	iset=set(items)
	if not make_it_unique or len(iset)==len(items):
		return items	# to keep the original sequence
	else:
		return list(iset)	# will lost the original sequence
		
def attrstr2dict(s):
	'''
	this function can turn a string consist of serveral lines of attributive records 
	into a key-value dict, the record line if the in the form of key=value,
	empty chars around the key or value will be stripped, and the content
	before the first = in each line will be considered as key, after the =
	is the value.
	Note that only the lines begin with # will be considered as comment, because some time we need # as value.
	
	for example:
		key=value
		#def
		a=b	= #klm
	will return {'key'='value', 'a'='b	= #klm'}
	'''
	lines=s.strip().split('\n')
	lines=[l.strip() for l in lines]
	lines=[l for l in lines if len(l)>0 and l[0]!='#' and '=' in l]
	obj={}
	for l in lines:
		p=l.find('=')
		k=l[:p].strip()
		v=l[p+1:].strip()
		obj[k]=v
	return obj
	
def match_any_pattern(target_string, regexp_list):
	for regexp in regexp_list:
		if regexp.search(target_string): return True
	return False
		
def good_link(links):
	links=[i.strip() for i in links]
	links=[i for i in links if i and len(i)<=512 and i.find('\n')==-1 and i.find('\t')==-1 and i.find('\r')==-1]
	links=[i.replace(' ', '%20') for i in links]
	return links
		

class Options(object):
	def __init__(this, conf):
		this.conf={}
		for k in conf:
			if k[0]=='_': continue
			this.conf[k]=conf[k]
		this.num_fechers=this.get('num_fechers', 10)
		
		this.sleep_delay=this.get('sleep_delay', 1)
		assert this.sleep_delay>=0
		
		this.enabled_exts=this.get('enabled_exts', '')
		this.disabled_exts=this.get('disabled_exts', '')
		
	def __getattr__(this, name):
		if name in this.conf:
			return this.conf[name]
		# print 'can not get attr:', name
		# raw_input()
		raise AttributeError
		
	def get(this, name, default=None, func=None):
		assert is_dict(this.conf)
		assert is_str(name)
		if func==None and default!=None:
			func=type(default)
		if default==None:
			ret=this.conf.get(name)
		else:
			ret=this.conf.get(name, default)
			
		if default!=None and func!=None and type(ret)!=type(default):
			ret=func(ret)
		return ret
		
class ParserOptions(Options):
	def __init__(this, conf):
		Options.__init__(this, conf)
		this.seed_urls=this.get('seed_urls')
		
		this.max_seconds_gen_urls=this.get('max_seconds_gen_urls', 30)
		this.min_records_gen_urls=this.get('min_records_gen_urls', 2000)
		
		this.reset_depth_on_outsite_link=this.get('reset_depth_on_outsite_link', True)

		this.in_site_crawl=this.get('in_site_crawl', True)
		this.archive_by_ext=this.get('archive_by_ext', False)
		this.gather_infotxt=this.get('gather_infotxt', False)
		
		this.enabled_urls=this.get('enabled_urls', 'jadesoul\.org')
		this.disabled_urls=this.get('disabled_urls', 'jadesoul\.org')
				
class FetcherOptions(Options):
	def __init__(this, conf):
		Options.__init__(this, conf)
		
		this.max_depth=this.get('max_depth', 5)
		this.page_files_max_num=this.get('page_files_max_num', 20000)
		
		this.crawl_delay=this.get('crawl_delay', 1)
		assert this.crawl_delay>=0
		
		this.priority_order=this.get('priority_order', '')
		
		this.request_headers=this.get('request_headers', {})
		this.cookie_string=this.get('cookie_string', '')
		
if __name__=='__main__':
	pass
