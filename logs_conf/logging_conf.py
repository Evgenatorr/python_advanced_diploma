from config import settings

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        },
        'verbose': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s (%(filename)s:%(lineno)d)',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': settings.LOG_FILE,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        # 'myapp': {  # логгер для конкретного модуля
        #     'handlers': ['console'],
        #     'level': 'DEBUG',
        #     'propagate': False,
        # },
        'sqlalchemy.engine': {  # логирование запросов SQLAlchemy
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}
