import logging.config


def setup_logging(dict_conf: dict) -> None:
    logging.config.dictConfig(dict_conf)


logger = logging.getLogger()
