import logging.config

from logs_conf.logging_conf import LOGGING_CONFIG


def setup_logging(dict_conf: dict) -> None:
    logging.config.dictConfig(dict_conf)


logger = logging.getLogger()
