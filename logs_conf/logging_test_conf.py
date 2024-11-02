from config import settings

TEST_LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s (%(filename)s:%(lineno)d)',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': settings.TEST_LOG_FILE,
            'formatter': 'standard',
            'mode': 'w',
        },
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}