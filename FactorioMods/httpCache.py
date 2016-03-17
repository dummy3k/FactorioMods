import hashlib, os, urllib2

def get_md5_str(s):
	m = hashlib.md5()
	m.update(s)
	return m.hexdigest()

def getContent(url):
	cache_filename = "var/cache/%s.html" % get_md5_str(url)
	if os.path.exists(cache_filename):
		with open(cache_filename, 'r') as f:
			return f.read()
	else:
		response = urllib2.urlopen(url)
		html = response.read()
		with open(cache_filename, 'w') as f:
			f.write(html)
		
		return html
		