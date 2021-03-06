import logging
import re

logger = logging.getLogger(__name__)

from FactorioMods.httpCache import getContent
from bs4 import BeautifulSoup

class ModPage():
    def __init__(self, mod_name):
        self.mod_name = mod_name

        self.html = getContent("http://www.factoriomods.com/mods/%s" % self.mod_name)
        self.soup = BeautifulSoup(self.html, 'html.parser')

    @property
    def dict(self):
        retVal = []
        mod_downloads_table = self.soup.find("table", { "class" : "mod-downloads-table" })
        if not mod_downloads_table and "This mod doesn't have anything to download :(" in self.html:
            return retVal

        headers = mod_downloads_table.thead.tr.find_all("th")
        headers = map(lambda x: x.text.strip(), headers)
        logger.debug(headers)

        for row in mod_downloads_table.tbody.find_all("tr"):
            row_dict = {}
            for col_index, col in enumerate(row.find_all("td")):
                col_name = headers[col_index]
                # logger.debug(col_name, col.text.strip())
                if col.a:
                    row_dict[col_name] = col.a["href"]
                else:
                    row_dict[col_name] = col.text.strip()

            logger.debug(str(row_dict))
            if row_dict[u'Factorio version']:
                m = re.match(r"[\.\d]+\d+", row_dict[u'Factorio version'])
                if not m:
                    logger.warn("[%s] cant read 'Factorio version': '%s'" % (self.mod_name, row_dict[u'Factorio version']))
                else:
                    row_dict[u'Factorio version'] = m.group(0)
                    retVal.append(row_dict)

        retVal = map(lambda x: {"factorio_version":row_dict[u'Factorio version'],
                                "mod_version":x[u'Mod version'],
                                "download_link":x[u'File version'],
                                },
                     retVal)
        return retVal

