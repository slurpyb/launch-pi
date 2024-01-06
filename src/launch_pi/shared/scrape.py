import json
import logging
from collections import namedtuple

from loguru import logger

import requests
from src.launch_pi.config import settings

Platform = namedtuple('Platform', 'id name')

def get_platform(platform_name: str) -> Platform | None:
    r = requests.get(f'https://api.mobygames.com/v1/platforms?api_key={settings.moby_games_api_key}').json()
    logger.info(r)
    for item in r.get('platforms'):
        if item.get('platform_name') == platform_name:
            return Platform(id=item.get('platform_id'), name=item.get('platform_name'))
    return None
    # return r.get('platforms')

def get_game_rating(platform: str, name: str):
    name_encoded = requests.utils.quote(name)
    # platform_id = get_platform(platform_name=platform).id
    platform_id = 9
    r = requests.get(f'https://api.mobygames.com/v1/games?api_key={settings.moby_games_api_key}&title={name_encoded}&platform={platform_id}')
    return r.json()

name = 'Perfect Dark'

platform = 'Nintendo 64'
logger.info(get_game_rating(platform=platform, name=name))

# get_platform('Nintendo 64')