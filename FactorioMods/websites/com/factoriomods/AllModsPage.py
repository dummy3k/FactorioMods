import logging
logger = logging.getLogger(__name__)

import re
from bs4 import BeautifulSoup
from FactorioMods.httpCache import getContent


class AllModsPage:
    def __init__(self, page_number=1):
        self.page_number = page_number
        self.url = "http://www.factoriomods.com/mods?page=%s" % page_number
        self.html = getContent(self.url)
        self.soup = BeautifulSoup(self.html, 'html.parser')

    @property
    def max_pages(self):
        link = self.soup.find("span", { "class" : "last" })
        if not link:
            return None
        href = link.a['href']
        logger.debug("href: %s" % href)

        #/mods?page=13
        matches = re.findall(r'page=(\d+)', href)
        return int(matches[0])

    @property
    def mods(self):
        retVal = []
        mod_divs = self.soup.find_all("div", { "class" : "mod" })
        for mod_div in mod_divs:
            name = mod_div.find_all("span", { "class" : "highlight-query" })
            logger.debug(name)
            pretty_name = name[0].a.text
            href = name[0].a["href"]
            logger.debug(href)

            #/mods/barrel-mod
            name = re.findall(r"/mods/([^/]+)", href)[0]
            logger.debug(name)
            retVal.append(name)

        return retVal

