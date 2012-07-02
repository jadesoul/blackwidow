#!/usr/bin/env python
#coding:utf8

from blackwidow import start, argv

# whether or not crawling only inside the site specified by the seed url
in_site_crawl=0

# the number of the fechers, the more the better usage of the network bandwidth
num_fechers=10

# the first urls list to start crawling, called seeds, seperated line by line
seed_urls='''
http://gb.wallpapersking.com/
'''

# seconds when a parser or fecher sleeps for nothing to do
sleep_delay=5

# max depth of following a link to process, 0 means just seed urls, -1 means no limit
max_depth=100

# on outsite link, whether reset depth as 0, or increasing the depth like the insite link did
# outsite link is a link from a site pointing to another different site, while insite link is pointing to the site itself
reset_depth_on_outsite_link=1

# max seconds between continuously generating urls file in 2 times
max_seconds_gen_urls=10

# min records to generate a new urls file
min_records_gen_urls=2000

# while list of url regexps, only urls match this and not match disabled_urls will be processed
# this is only used in the parser when new links are extracted from a page, same with disabled_urls
enabled_urls='''
wallpapersking
'''

# black list of url regexps, any url match this will be ignored, even in enabled_urls 
disabled_urls='''
'''

# enabled extensions of a url to download data, seperated by empty chars or line
# the extension is determined by the mime-type of response document and refer-url
# the enabled_exts and disabled_exts are only used in the fecher, it will open socket first
# to get the mime-type and refer-url, the content is downloaded only when ext is permitted
enabled_exts='''
htm html shtml
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
# normally you don't have to change this, just leave as it is
priority_order='''
jpg jpeg png bmp gif tiff tif
htm html shtml mht mhtm xhtml
xml xslt
txt
pdf ps ps.gz
doc docx xls xlsx csv tsv tab ppt pptx
css
js vbs
zip gz gzip tar rar jar 7z lzma tar.gz
mp4 mp3 wma wmv rm rmvb mpeg mpeg3 3gp avi ts flv f4v
swf fla
php jsp asp aspx py
exe bin com msi deb
'''


# start(locals())




