#coding:utf8

from common import *

class Parser(Thread, object):
	def __init__(this, conf, name='parser'):
		options=ParserOptions(conf)
		
		this.parser_name=name
		print 'init:', this.parser_name
		Thread.__init__(this, name=this.parser_name)
		
		this.history_urls={}	# history urls hash map
		this.new_urls=[]
		this.now_url_id=0
		
		this.seed_urls=lines2list(options.seed_urls)
		for url in this.seed_urls:
			this.history_urls[url]=1
		this.seed_hosts=list2dict([get_host_by_url(url) for url in this.seed_urls])
		
		this.r_enabled_urls=[compile(i) for i in lines2list(options.enabled_urls)]
		this.r_disabled_urls=[compile(i) for i in lines2list(options.disabled_urls)]
		
		this.enabled_exts=tabs2list(options.enabled_exts)
		this.disabled_exts=tabs2list(options.disabled_exts)
		
		this.to_deal_css= ('css' in this.enabled_exts)
		this.to_deal_js= ('js' in this.enabled_exts)
		
		this.sleep_delay=options.sleep_delay
		
		this.max_seconds_gen_urls=options.max_seconds_gen_urls
		this.min_records_gen_urls=options.min_records_gen_urls
		this.reset_depth_on_outsite_link=options.reset_depth_on_outsite_link
		this.in_site_crawl=options.in_site_crawl
		this.archive_by_ext=options.archive_by_ext
		this.gather_infotxt=options.gather_infotxt
		
		# generate initial urls
		this.PASS_TIME_CLOCK=this.parser_name+'-pass-time'
		this.GEN_URLS_CLOCK=this.parser_name+'-gen-urls'	# to record time duration between 2 url generations
		time_init(this.PASS_TIME_CLOCK)
		
		this.gen_urls_file([(i, 0) for i in this.seed_urls])
		time_init(this.GEN_URLS_CLOCK)
		
	def gen_urls_file(this, urls):
		ss=[]
		ids=[]
		for u, depth in urls:
			# try: s='%d\t%s\t%s\t%d' % (this.now_url_id, u, md5(u), depth)
			# except: continue
			s='%d\t%s\t%s\t%d' % (this.now_url_id, u, md5(u), depth)
			
			ids.append(this.now_url_id)
			this.now_url_id+=1
			ss.append(s)
		name='%d-%d.txt' % (ids[0], ids[-1])
		fp=join(dir_urls, name)
		print this.parser_name, 'gen_urls_file', name, 'size=', len(ss)
		s='\n'.join(ss)+'\n'
		print s
		fwrite(s, fp)

	def urls_filter(this, links):
		if this.r_enabled_urls: links=[link for link in links if match_any_pattern(link, this.r_enabled_urls)]
		if this.r_disabled_urls: links=[link for link in links if not match_any_pattern(link, this.r_disabled_urls)]
		return links
		
	def get_next_page(this):
		while 1:
			for fp_info in listfiles(dir_pages):
				if not fp_info.endswith(infotxt): continue
				fp_data=fp_info[:-len(infotxt)]
				if not isfile(fp_data): continue
				if fsize(fp_data)==0 or fsize(fp_info)==0: continue
				ls=fread(fp_info).strip().split('\n')
				ls=[i[i.find('=')+1:] for i in ls]
				id, url, real_url, content_type, ext, md5, depth, finish_time, duration=ls
				if not ext in ['html', 'htm', 'xml', 'shtml', 'xhtml']:
					this.archive_a_page(finish_time, fp_data, fp_info, ext)
					continue
				id=int(id)
				depth=int(depth)
				#page=smart_fread(fp_data)
				page=fread(fp_data)
				return page, id, url, real_url, content_type, ext, md5, depth, finish_time, duration, fp_data, fp_info
			if time_elapse(this.GEN_URLS_CLOCK)>this.max_seconds_gen_urls and this.new_urls:
				this.gen_urls_file(this.new_urls)
				time_update(this.GEN_URLS_CLOCK)
				this.new_urls=[]
			print this.parser_name, str(now()), 'not next page~~ ', time_gap(this.PASS_TIME_CLOCK, reset=0), 'history_urls:%d' % len(this.history_urls)
			sleep(this.sleep_delay)
			
	def archive_a_page(this, time, fp_data, fp_info, ext):
		time_str=time[:16].replace(':', '_').replace(' ', '_')
		dp=dir_archive
		if this.archive_by_ext:
			dp=join(dp, ext) 
			if not isdir(dp): md(dp)
		dp=join(dp, time_str)
		if not isdir(dp): md(dp)
		mv(fp_data, dp)
		
		if not this.gather_infotxt:
			mv(fp_info, dp)
		else:
			dp=join(dir_archive, 'infotxt')
			if not isdir(dp): md(dp)
			if this.archive_by_ext:
				dp=join(dp, ext)
				if not isdir(dp): md(dp)
			dp=join(dp, time_str)
			if not isdir(dp): md(dp)
			mv(fp_info, dp)

	def run(this):
		print 'start:', this.parser_name
		while 1:
			try:
				page, id, url, real_url, content_type, ext, md5, depth, finish_time, duration, fp_data, fp_info=this.get_next_page()
				if url!=real_url:
					this.history_urls[real_url]=1
					url=real_url	#use the real one
				
				# no need to parse all other files except these
				if ext not in ['htm', 'html', 'xml', 'shtml', 'xhtml', 'txt']:
					this.archive_a_page(finish_time, fp_data, fp_info, ext)
					continue
					
				page_host=get_host_by_url(url)
				
				try:
					dom=parse_html(page)
				except Exception, e:
					print 'error parsing html', e, type(e)
					print '\tlen(page)=', len(page)
					print '\tpage[:100]=', repr(page[:100])
					print '\tpage[-100:]=', repr(page[-100:])
					
					
				links=[link['href'] for link in dom('a', href=r_goodlink)]
				links+=[link['src'] for link in dom('img', src=r_goodlink)]
				if this.to_deal_js: links+=[link['src'] for link in dom('script', src=r_goodlink)]
				if this.to_deal_css: links+=[link['href'] for link in dom('link', href=r_goodlink)]
				
				print this.parser_name, 'links all:', len(links)
				
				# remove duplicated ones
				links=[i.strip() for i in links]
				links=unique(links)
				print this.parser_name, 'links unique:', len(links)
				
				# remove bad links
				links=good_link(links)
				print this.parser_name, 'links good:', len(links)
				
				# expand links by page url, merge dots
				# print 'url=', url
				# print 'links[:5]=', links[:5]
				links=expand_urls(url, links)
				print this.parser_name, 'links expand:', len(links)
				
				# some scheduler strategy here
				links=this.urls_filter(links)
				print this.parser_name, 'links urls_filter:', len(links)
				
				# archive the page
				this.archive_a_page(finish_time, fp_data, fp_info, ext)
				
				print this.parser_name, 'links:', len(links)
				if not links: continue
				
				# make some quote
				links=[fix_url(url) for url in links]
				
				new_depth=depth+1
				for link in links:
					if not link in this.history_urls:
						this.history_urls[link]=1
						link_host=get_host_by_url(link)
						 
						if this.in_site_crawl and not link_host in this.seed_hosts: continue
						link_depth=new_depth
						if this.reset_depth_on_outsite_link and link_host!=page_host: link_depth=0
						this.new_urls.append((link, link_depth))
						
				if not this.new_urls: continue
				print this.parser_name, 'new_urls:', len(this.new_urls), time_gap(this.PASS_TIME_CLOCK, reset=0)
				
				for new_url, new_url_depth in this.new_urls:
					print 'new url:', new_url, 'depth:', new_url_depth
				
				if this.seed_urls or time_elapse(this.GEN_URLS_CLOCK)>this.max_seconds_gen_urls or len(this.new_urls)>this.min_records_gen_urls:
					this.gen_urls_file(this.new_urls)
					this.seed_urls=None
					time_update(this.GEN_URLS_CLOCK)
					this.new_urls=[]
					
			except Exception, e:
				print this.parser_name, 'fail', e, type(e)
				raise e
