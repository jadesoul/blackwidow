#coding:utf8

from common import *

class Fetcher(Thread, object):
	def __init__(this, conf, fecher_id, fecher_name='fetcher-%d'):
		options=FetcherOptions(conf)
		
		this.num_fechers=options.num_fechers
		this.fecher_id=fecher_id
		this.fecher_name=fecher_name % fecher_id
		print 'init:', this.fecher_name
		Thread.__init__(this, name=this.fecher_name)
		
		
		this.max_depth=options.max_depth
		this.page_files_max_num=options.page_files_max_num
		this.sleep_delay=options.sleep_delay
		this.crawl_delay=options.crawl_delay
		
		this.enabled_exts=tabs2list(options.enabled_exts)
		this.disabled_exts=tabs2list(options.disabled_exts)
		
		this.priority_order=tabs2list(options.priority_order, 0)
		this.priority_order_dict={}
		for i, ext in enumerate(this.priority_order):
			this.priority_order_dict[ext]=i
		
		this.request_headers=options.request_headers
		this.cookie_string=options.cookie_string
		
		this.history_url_files={}
		this.fp_state=join(dir_state, this.fecher_name+'.txt')
		this.fp_log=join(dir_state, this.fecher_name+'.log')
		this.next_url_id=this.fecher_id
		
		this.PASS_TIME_CLOCK=this.fecher_name+'-parser_pass_time'
		time_init(this.PASS_TIME_CLOCK)
		
	def get_next_urls(this, urls):
		while 1:
			for fp in listfiles(dir_urls):
				fp, dp, fn, name, ext=split(fp)
				if not name in this.history_url_files:
					this.history_url_files[name]=1
					start, end=[int(i) for i in name.split('-')]
					for l in fread(fp).strip().split('\n'):
						id, url, md5, depth=l.split('\t')
						id=int(id)
						depth=int(depth)
						if this.max_depth>=0 and depth>this.max_depth: continue
						if id%this.num_fechers==this.fecher_id:
							ext=get_file_type_by_url(url)
							rank=this.priority_order_dict.get(ext, 1000000)
							urls.append((id, url, md5, depth, rank))
			if urls: return urls
			print this.fecher_name, str(now()), 'no next urls !!!', time_gap(this.PASS_TIME_CLOCK, reset=0)
			sleep(this.sleep_delay)
			
	def is_ext_ok(this, ext):
		# only one takes effects
		if this.enabled_exts:
			if ext in this.enabled_exts:
				return True
		elif this.disabled_exts:
			if ext not in this.disabled_exts:
				return True
		return False
		
	def run(this):
		print 'start:', this.fecher_name
		urls=[]
		while 1:
			if len(listfiles(dir_pages))>this.page_files_max_num:
				sleep(this.sleep_delay)
				continue
			urls=this.get_next_urls(urls)
			
			# sort the urls by rank
			urls=sorted(urls, key=lambda x: x[-1])
			
			cnt=0
			total=len(urls)
			while urls:
				sleep(this.crawl_delay*(0.5+random.random()))
				cnt+=1
				id, url, md5, depth, rank=urls.pop(0)
				
				# some schedule let newly add urls with higher rank be processed first
				if total<1000 and cnt>(total/2): break
				if cnt>800: break
				
				try:
					begin_time=time.time()
					real_url, content_type, fsock=webopen(url, this.request_headers)
					
					# TODO: add debug logging here
					print 'url=', url
					print 'real_url=', real_url
					print 'content_type=', content_type
					
					ext=get_ext_by_mimetype(content_type)
					if not ext: ext=get_file_type_by_url(real_url)
					if not this.is_ext_ok(ext):
						sockclose(fsock)
						print this.fecher_name, 'bad_ext', rank, real_url
						continue
					
					base=md5+'.'+ext
					fp=join(dir_pages, base)
					
					if isfile(fp) and isfile(fp+infotxt):
						# if the content has been downloaded before, skip
						sockclose(fsock)
						print this.fecher_name, 'exists', rank, real_url
						continue
					
					data=sockreadonce(fsock)
					# debug
					# print 'data=', data
					datasave(data, fp)
					
					finish_time=now()
					duration=time.time()-begin_time
					s='''id=%d
url=%s
real-url=%s
content-type=%s
extension=%s
md5=%s
depth=%d
download-time=%s
download-duration=%f''' % (id, url, real_url, content_type, ext, md5, depth, finish_time, duration)
					fwrite(s, join(dir_pages, base+infotxt))
					print this.fecher_name, 'good', rank, url
					if url!=real_url: print '\t->', real_url
					print '\t', id, content_type, ext, md5, depth
					print '\t', finish_time, duration
				except Exception, e:
					try: 
						sockclose(fsock)
					except: 
						# print log
						pass
					print this.fecher_name, 'failed', rank, url
					print '\t', e
					continue
				
