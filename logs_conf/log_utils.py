import logging.config
from typing import Dict, Any


def setup_logging(dict_conf: Dict[str, Any]) -> None:
    logging.config.dictConfig(dict_conf)


logger = logging.getLogger()
