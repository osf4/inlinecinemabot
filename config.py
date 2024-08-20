from dataclasses import dataclass
from datetime import timedelta
from dacite import from_dict, Config as DaciteConfig
from pytimeparse import parse

from yaml import load, CLoader as Loader

def _parse_expire_time(expire_time: str) -> timedelta:
    """
    Parse expiration time of the cache from config file into timedelta
    """
    
    return timedelta(seconds = parse(expire_time))


@dataclass
class Config:
    """
    Application config from 'config.yaml' file

    Example of the config file:

    token: 'abcde1234567890'
    cache_expire_time: '1 hour'
    """

    __dacite_config = DaciteConfig(
        type_hooks = {
            timedelta: _parse_expire_time,
        }
    )

    token: str
    cache_expire_time: timedelta


    @classmethod
    def load(cls, config_file: str = 'config.yaml') -> 'Config':
        with open(config_file) as config_file:
            config = load(config_file, Loader)

        return from_dict(cls, config, cls.__dacite_config)
