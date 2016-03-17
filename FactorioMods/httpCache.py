import hashlib, os, urllib2

import logging
logger = logging.getLogger(__name__)

def get_home_dir():
	from os.path import expanduser
	return expanduser("~")
	
def create_data_dir():
	data_dir = os.path.join(get_home_dir(), ".FactorioMods")
	if not os.path.exists(data_dir):
		logger.info("creating: %s" % data_dir)
		os.mkdir(data_dir)
		
	return data_dir
	
def get_md5_str(s):
	m = hashlib.md5()
	m.update(s)
	return m.hexdigest()

def getContent(url):
	logger.debug("GET? %s", url)
	# cache_filename = "%s/%s.html" % (get_home_dir(), get_md5_str(url))
	cache_dir = os.path.join(create_data_dir(), "cache")
	if not os.path.exists(cache_dir):
		logger.info("creating: %s" % cache_dir)
		os.mkdir(cache_dir)

	cache_filename = os.path.join(cache_dir, get_md5_str(url))
	logger.debug("cache_filename: %s", cache_filename)
	if os.path.exists(cache_filename):
		with open(cache_filename, 'r') as f:
			return f.read()
	else:
		logger.info("GET %s", url)
		response = urllib2.urlopen(url)
		html = response.read()
		with open(cache_filename, 'w') as f:
			f.write(html)
		
		return html
		