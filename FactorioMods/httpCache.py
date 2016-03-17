import hashlib, os, urllib2

import logging
logger = logging.getLogger(__name__)

def get_home_dir():
	from os.path import expanduser
	return expanduser("~")
	
def get_md5_str(s):
	m = hashlib.md5()
	m.update(s)
	return m.hexdigest()

def getContent(url):
	logger.debug("GET? %s", url)
	# cache_filename = "%s/%s.html" % (get_home_dir(), get_md5_str(url))
	cache_filename = os.path.join(get_home_dir(), get_md5_str(url))
	logger.debug("cache_filename: %s", cache_filename)
	if os.path.exists(cache_filename):
		with open(cache_filename, 'r') as f:
			return f.read()
	else:
		logger.info("GET %s", url)
		return
		response = urllib2.urlopen(url)
		html = response.read()
		with open(cache_filename, 'w') as f:
			f.write(html)
		
		return html
		