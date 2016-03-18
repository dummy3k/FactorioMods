import logging
logger = logging.getLogger(__name__)

import re
from FactorioMods.httpCache import getContent
from bs4 import BeautifulSoup

def parse_html():
    html_doc = getContent("https://forums.factorio.com/viewtopic.php?f=46&t=2842")
    soup = BeautifulSoup(html_doc, 'html.parser')
    retVal = []
    for link in soup.find_all("a", { "class" : "postlink" }):
        link_text = link.text.strip()
        m = re.match(r"test-mode_(\d+).(\d+).(\d+)", link_text)
        if m:
            # logger.debug(link)
            # logger.debug(link["href"])
            retVal.append({'factorio_version':u"%s.%s" % (m.group(1),
                                                          m.group(2)),
                           'mod_version':u"%s.%s.%s" % (m.group(1),
                                                     m.group(2),
                                                     m.group(3)),
                           'download_link':link["href"]})
    # logger.debug()
    return(retVal)
    # mod_downloads_table = soup.find("table", { "class" : "mod-downloads-table" })
