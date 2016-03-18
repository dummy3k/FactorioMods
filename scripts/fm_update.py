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
            'level': 'DEBUG',
            'propagate': True
        },
        'FactorioMods.httpCache': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
})


logger = logging.getLogger('fm_update')
# logger.debug('Protocol problem: %s', 'connection reset')
# logger.info('Protocol problem: %s', 'connection reset')
# logger.warning('Protocol problem: %s', 'connection reset')
# logger.error('Protocol problem: %s', 'connection reset')
# print("hello world")

from FactorioMods.httpCache import getContent
# getContent("http://www.factoriomods.com/recently-updated")



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
getContent("https://raw.githubusercontent.com/dummy3k/FactorioMods/master/.gitignore")