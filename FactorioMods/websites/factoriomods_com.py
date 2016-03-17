import logging
logger = logging.getLogger(__name__)

from FactorioMods.httpCache import getContent
from bs4 import BeautifulSoup

def parse_html(mod_name):
	html_doc = getContent("http://www.factoriomods.com/mods/%s" % mod_name)
	soup = BeautifulSoup(html_doc, 'html.parser')
	mod_downloads_table = soup.find("table", { "class" : "mod-downloads-table" })
	headers = mod_downloads_table.thead.tr.find_all("th")
	headers = map(lambda x: x.text.strip(), headers)
	logger.debug(headers)

	retVal = []
	for row in mod_downloads_table.tbody.find_all("tr"):
		row_dict = {}
		for col_index, col in enumerate(row.find_all("td")):
			col_name = headers[col_index]
			# logger.debug(col_name, col.text.strip())
			if col.a:
				row_dict[col_name] = col.a["href"]
			else:
				row_dict[col_name] = col.text.strip()
		
		# logger.debug(str(row_dict))
		retVal.append(row_dict)
	
	retVal = map(lambda x: {"factorio_version":x[u'Factorio version'],
							"mod_version":x[u'Mod version'],
							"download_link":x[u'File version'],
							},
				 retVal)
	return retVal
	
