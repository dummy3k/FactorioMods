from FactorioMods.httpCache import getContent
import logging
import logging.config

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
			'format': "%(log_color)s%(levelname)-8s%(message)s"
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
        'django.request': { 
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': False
        },
    } 
})

	
logger = logging.getLogger('fm_update')
logger.debug('Protocol problem: %s', 'connection reset')
logger.info('Protocol problem: %s', 'connection reset')
logger.warning('Protocol problem: %s', 'connection reset')
logger.error('Protocol problem: %s', 'connection reset')

#getContent("http://www.factoriomods.com/recently-updated")
print("hello world")