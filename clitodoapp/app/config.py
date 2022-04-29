import copy
import os
import logging

from typing import Dict
from typing import Optional

import yaml


from clitodoapp.app.exceptions import ClitodoappException
from clitodoapp.app.utils import update_nested_dict

LOG = logging.getLogger(__name__)


class ConfigLoadingException(ClitodoappException):
    pass


class InvalidConfigFilePathError(ConfigLoadingException, ValueError):
    pass


_CONFIG_SCHEMA = {
    'type': 'object',
    'required': [
        'logging',
    ],
    'properties': {
        'logging': {
            'type': 'object',
        },
    },
}


_CONFIG_DEFAULTS = {
    'logging': {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'generic': {
                '()': "clitodoapp.app.logger.LogRecordFormatter",
                'format': "%(asctime)s [%(levelname).1s] [%(process)s %(threadName)s] %(message)s",
                'datefmt': "%Y-%m-%d %H:%M:%S.%f %z",
            },
            
        },
        'handlers': {
            #'console': {
            #    'level': 'INFO',
            #   'formatter': 'generic',
            #    'class': 'logging.StreamHandler',
            #    'stream': 'ext://sys.stdout',
            #},
            'file': {
                'level': 'DEBUG',
                'formatter': 'generic',
                'class': 'logging.FileHandler',
                'filename': 'new-todo.log',
                'mode': 'w',
            },
        },
        'loggers': {
            '': {
                'handlers': ['file'],
                'level': 'DEBUG',
            },
        },
    },
}


_CONFIG_ENV_VARS_MAP = {
    'logging': {
        'formatters': {
            'generic': {
                'format': "CLITODOAPP_GENERIC_LOG_RECORD_FMT",
                'datefmt': "CLITODOAPP_GENERIC_LOG_DATE_FMT",
            },
            
        },
    },
}

def _maybe_override_from_file(
    config: Dict,
    file_path: Optional[str]=None,
    section_name: Optional[str]=None,
) -> None:

    if not file_path:
        return

    if not os.path.isfile(file_path):
        raise InvalidConfigFilePathError("config path must point to a file")

    with open(file_path, 'rt') as f:
        overrides = yaml.safe_load(f)

    if overrides and section_name:
        overrides = overrides[section_name]

    if overrides:
        update_nested_dict(config, overrides)


def _maybe_override_log_record_format_from_env(config: Dict, formatter_name: str) -> None:
    value = os.environ.get(_CONFIG_ENV_VARS_MAP['logging']['formatters'][formatter_name]['format'])
    if value:
        config['logging']['formatters'][formatter_name]['format'] = value


def _maybe_override_log_date_format_from_env(config: Dict, formatter_name: str) -> None:
    value = os.environ.get(_CONFIG_ENV_VARS_MAP['logging']['formatters'][formatter_name]['datefmt'])
    if value:
        config['logging']['formatters'][formatter_name]['datefmt'] = value


def _maybe_override_logging(config: Dict) -> None:
    _maybe_override_log_record_format_from_env(config, 'generic')
    _maybe_override_log_date_format_from_env(config, 'generic')
    


def _maybe_override_from_env(config: Dict) -> None:
    _maybe_override_logging(config)


def try_to_load_config(
    file_path: Optional[str]=None,
    section_name: Optional[str]=None,
    # extra params passed from CLI args
) -> Dict:
    config = copy.deepcopy(_CONFIG_DEFAULTS)
    _maybe_override_from_file(config, file_path, section_name)
    _maybe_override_from_env(config)
    # override from CLI args if passed as extra params
    try:
        validate(config, _CONFIG_SCHEMA)
    except NameError as err:
        LOG.debug(err)

    return config
