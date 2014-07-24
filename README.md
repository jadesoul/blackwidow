blackwidow
==========

Jadesoul's OpenSource Web Spider Program 

Welcome to Black Widow
----------------------

Black Widow is a lightweight, efficient, scalable and practical web spider 
purely implemented in python.

The name "black widow" comes from a kind of spider species, which 
is one of the top 6 most venomous animals on the earth. Here is a picture
of Female black widow spider from wiki.


![More info about black widow in wiki](http://upload.wikimedia.org/wikipedia/commons/f/f9/BlackWidow.jpg "black widow")

The black widow is very handsome, powerful, and pretty dangerous 
if not playing with caution, as well as this spider program.


Features
--------

### Lightweight
  * It is designed to be lightweight and easy to use, with less than 5000 lines of python code, it is tiny small in comparison to so many opensource and production spiders.
  * The structure of the spider is pretty simple, including the code structure, the temporary data structure and so on.

### Efficient
  * It is designed to be efficient. It has a multi-process structure, that is, one parser process and N fetcher process.
  * Their coperations through the file system is designed to be efficient and no deadlock will happen because of the time limitation and space checking are both considerd for controlling.
  * The url's file extention used in runtime is determined by content type in the document response http headers first rather than simply determined by the url extension.

### Scalable
  * It is totally configurable, there are enought simple options to meet different demand. 
  * For example, seed urls, max depth, enalbled and disabled url patterns and extensions, priority of extensions for sheduling to make sure important resources being processed earlier. 
  * The number of fetcher process is changable for better use of network bandwidth. 
  * Downloaded resource will be archived by extension or not, and so on.
  
### Practical
  * It is designed to be pratical and useful, especially for small and middium scale crawling tasks. 
  * At the beginning, in fact, this spider is designed to grap pictures from a picture site or fetch all pdfs from a professor's homepage. So it ignored many details as a  production spider should consider, for example, robots.txt will not be considered.

Requirements
-------------

  * Any OS supported Python
  * Python 2.5 or 2.6 or *2.7(Recommended)*  [http://www.python.org/getit/ Python Download Page]

Installation
-------------

### Install blackwidow as a python package by pth file automatically(Only for Windows)
  * If you have installed python in the root folder of a drive, simply click the "install_pth_file_blackwidow.py" to install a pth file in your ${python installation directory}/Lib/site-packages
  
### Install blackwidow as a python package maually
  * Just copy the "libspider" directory into your python's site-packages directory
  * Or create a pth file in your python's site-packages directory manually
  
### What If I don't have time to install ?
  * No problem, you just need to copy the libspider directory to where every time you run a new crawling application.

User Guide
----------

### To run a new crawler application after installation, you just need to
 # copy the "a_spider_sample.py" to anywhere as you want, or you can also leave it where it is
 # modify the necessary options, you can rename the file if you want
 # just double click to run that python file
 
### What if I can't start the program
  * please do make sure you installed python *2.5/2.6/2.7*, Python 3.x is temporarily *not supported*, but will be considered in the future :)
  * try to make sure "python" command is accessable in system shell
  * try to make sure the libspider directory and your application is in the same folder
  
### Where could I find the result
  * You can find your result in archive folder
  * the urls, pages, states dir are tmp dirs
  
### Configuration Details

		# the first urls list to start crawling, called seeds, seperated line by line
		# lines begin with # will be ignored as comment (the same for all string options in this file)
		seed_urls='''
		http://www.clsp.jhu.edu/ws03/groups/translate/biblio.shtml
		'''

		# whether or not crawling only inside the site/sites specified by the seed urls
		in_site_crawl=1

		# the number of the fechers, the more the better usage of the network bandwidth
		# however, too many fechers will have a strong influence on the OS process scheduling
		num_fechers=10

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

		# while list of url regular expressions, only urls match this and not match disabled_urls will be processed
		# this is only used in the parser when new links are extracted from a page, same with disabled_urls
		enabled_urls='''
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
		doc docx rtf xls xlsx csv tsv tab ppt pptx
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
		xml xslt rss
		txt
		pdf ps ps.gz
		jpg jpeg png bmp gif tiff tif
		doc docx rtf xls xlsx csv tsv tab ppt pptx
		css
		js vbs
		zip gz gzip tar rar jar 7z lzma tar.gz
		mp4 mp3 wma wmv rm rmvb mpeg mpeg3 3gp avi ts flv f4v
		swf fla
		php php1 php2 php3 php4 php5 jsp asp aspx py do cfm cgi
		exe bin com msi deb
		'''

If you have any problem, please feel free to ask me by wslgb2006@gmail.com :)

This software is designed in my spare time, hope you will enjoy it !
---------------------------------------------------------------------------

Designed By Jadesoul @ 2011-11-23 | http://jadesoul.org
Move to Git On 2012-7-3 By Jadesoul
