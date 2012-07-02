#!/usr/bin/env python
#coding:utf8

from blackwidow import *

# the first urls list to start crawling, called seeds, seperated line by line
# lines begin with # will be ignored as comment (the same for all string options in this file)
seed_urls='''
http://jadesoul-home
'''

# whether or not crawling only inside the site/sites specified by the seed urls
in_site_crawl=1

# the number of the fechers, the more the better usage of the network bandwidth
# however, too many fechers will have a strong influence on the OS process scheduling
num_fechers=1

# average seconds delay used in each fecher when finished downloading a page
crawl_delay=1

# set the request headers dict
# for example:
''' request_headers={
	'Accept'			:	'*/*',
	'Accept-Charset'	:	'GBK,utf-8;q=0.7,*;q=0.3',
	'Accept-Encoding'	:	'gzip,deflate,sdch',
	'Accept-Language'	:	'en-US,en;q=0.8',
	'Cache-Control'	:	'max-age=0',
	'Proxy-Connection'	:	'keep-alive',
	'Cookie'			:	'GSP=ID=8d0e6002d55d165e; PREF=ID=8d0e6002d55d165e:U=8bc852eae13e12a8:FF=0:TM=1318149638:LM=1318213357:GM=1:S=EH6Oc_BimnX3LGqs; NID=54=fMTRP-py-BI9IKHWhmu0nCiSsOGbLYL28ZA2CRO_OCmk3vE1MAtqR8sHzQ44E_9BL0Ky6flU4WzKZOyKPHAuBbqhb5_HUNxlRW8SliiFHWghA8ROJTiEN9c19BbpKHzu',
	'User-Agent'		:	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.121 Safari/535.2'
}'''
request_headers={}
		
# set the cookie string
# example: 
# cookie_string='GSP=ID=8d0e6002d55d165e; PREF=ID=8d0e6002d55d165e:U=8bc852eae13e12a8:FF=0:TM=1318149638:LM=1318213357:GM=1:S=EH6Oc_BimnX3LGqs; NID=54=fMTRP-py-BI9IKHWhmu0nCiSsOGbLYL28ZA2CRO_OCmk3vE1MAtqR8sHzQ44E_9BL0Ky6flU4WzKZOyKPHAuBbqhb5_HUNxlRW8SliiFHWghA8ROJTiEN9c19BbpKHzu'
cookie_string=''

# seconds when a parser or fecher sleeps for nothing to do
sleep_delay=5

# max depth of following a link to process, 0 means just handle seed urls, -1 means no limit
max_depth=1

# on outsite link, whether reset depth as 0, or increasing the depth like the insite link did
# outsite link is a link from a site pointing to another different site, while insite link is pointing to the site itself
reset_depth_on_outsite_link=1

# max seconds between continuously generating urls file in 2 times
max_seconds_gen_urls=10

# min records to generate a new urls file
min_records_gen_urls=2000

# if files num in the page dir reach this amount, the fetcher will wait for the parser to deal them
page_files_max_num=20000

# while list of url regular expressions, only urls match this and not match disabled_urls will be processed
# this is only used in the parser when new links are extracted from a page, same with disabled_urls
enabled_urls='''
jadesoul\-home
'''

# black list of url regular expressions, any url match this will be ignored, even in enabled_urls 
disabled_urls='''
'''

# enabled extensions of a url to download data, seperated by empty chars or line
# the extension is determined by the mime-type of response document and refer-url
# the enabled_exts and disabled_exts are only used in the fecher, it will open socket first
# to get the mime-type and refer-url, the content is downloaded only when ext is permitted
enabled_exts='''
htm html shtml
xml txt
pdf ps
jpg jpeg png bmp gif tiff tif
'''

# disabled extensions of a url to download data, seperated by empty chars or line
# if enabled_exts is not empty, this won't take effect
disabled_exts='''
rm rmvb avi mp3
'''

# when archive, whether to gather all files with the same extension or not
archive_by_ext=1

# priority of different extensions of urls to be scheduled, seperated by empty chars or line
# if you are about to crawl pdfs, you can move the "pdf ps ps.gz" to the first line
priority_order='''
htm html shtml mht mhtm xhtml
xml xslt
txt
pdf ps ps.gz
jpg jpeg png bmp gif tiff tif
doc docx xls xlsx csv tsv tab ppt pptx
css
js vbs
zip gz gzip tar rar jar 7z lzma tar.gz
mp4 mp3 wma wmv rm rmvb mpeg mpeg3 3gp avi ts flv f4v
swf fla
php jsp asp aspx py
exe bin com msi deb
'''

start(locals())
