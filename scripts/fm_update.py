import argparse
import logging
import logging.config
from pprint import pprint

# from colorlog import ColoredFormatter
# # FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
# # logging.basicConfig(format=FORMAT)

# #http://stackoverflow.com/questions/7507825/python-complete-example-of-dict-for-logging-config-dictconfig
# #https://pypi.python.org/pypi/colorlog/2.0.0


logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        'colored': {
            '()': 'colorlog.ColoredFormatter',
            'format': "%(log_color)s%(levelname)-5s [%(name)s] %(message)s"
        }
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'formatter': 'colored',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': True
        },
        'FactorioMods.httpCache': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': False
        },
        'FactorioMods.websites.com.factoriomods.ModPage': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': False
        },
    }
})


logger = logging.getLogger('fm_update')

def dump_mods():
    all_mods = {}
    import FactorioMods.websites.factoriomods_com
    # all_mods["logistics-railway"] = FactorioMods.websites.factoriomods_com.parse_html("logistics-railway")
    # pprint(FactorioMods.websites.factoriomods_com.parse_html("logistics-railway"))

    import FactorioMods.websites.test_mode
    all_mods["test-mode"] = FactorioMods.websites.test_mode.parse_html()

    import json
    all_mods_json = json.dumps(all_mods,
                               sort_keys=True,
                               indent=4,
                               separators=(',', ': '))
    # print(all_mods_json)
    # import readline # optional, will allow Up/Down/History in the console
    # import IPython;IPython.embed()

# dump_mods()
# getContent("https://docs.python.org/2/library/httplib.html")
# getContent("https://raw.githubusercontent.com/dummy3k/FactorioMods/master/.gitignore")

from FactorioMods.websites.com.factoriomods.AllModsPage import AllModsPage
from FactorioMods.websites.com.factoriomods.ModPage import ModPage

import os

def update_all(outdir):
    amp = AllModsPage()
    logger.debug(amp.max_pages)
    logger.debug(amp.mods)

    factorio_versions = {}
    while amp:
        for mod_name in amp.mods:
            try:
                mp = ModPage(mod_name)
                logger.debug(mp.dict)
                versions = map(lambda x: x['mod_version'], mp.dict)
                # print(versions)
                # factorio_versions[factorio_version][mod_name] = {'max_mod_version':versions[0]}

                for item in mp.dict:
                    factorio_version = item['factorio_version']
                    if not factorio_version in factorio_versions:
                        factorio_versions[factorio_version] = {}
                    if not mod_name in factorio_versions[factorio_version]:
                        factorio_versions[factorio_version][mod_name] = {}

                    mod_version = item['mod_version']
                    factorio_versions[factorio_version][mod_name][mod_version] = item['download_link']
            except:
                logger.warn("failed: %s" % mod_name)
                raise

        if not amp.max_pages or amp.page_number >= amp.max_pages:
            amp = None
        else:
            amp = AllModsPage(amp.page_number + 1)

    # pprint(factorio_versions)

    import json
    for factorio_version in factorio_versions:
        out_filename = os.path.join(outdir, "%s.json" % factorio_version)
        with open(out_filename, 'w') as f:
            json.dump(factorio_versions[factorio_version], f,
                                   sort_keys=True,
                                   indent=4)

def main():
    parser = argparse.ArgumentParser(description='Update FactorioMods')
    parser.add_argument('--update_all', action='store_true')
    parser.add_argument('-o', action='store')
    args = parser.parse_args()
    if args.update_all:
        if not args.o:
            logger.error("missing argument o")

        update_all(args.o)


if __name__ == '__main__':
    main()