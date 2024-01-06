from pathlib import Path
from typing import Dict
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', case_sensitive=False, extra='allow')

    launchbox_path: Path = Path('/media/jordan/PD1000/LaunchBox/')
    retropi_dir: Path = Path('/media/jordan/PD1000/retropi/')

    favorites_only: bool = False
    game_broken: bool = True
    game_hide: bool = True

    platforms: Dict[str, str] = {
        'Atari 2600': 'atari2600',
        'Atari 7800': 'atari7800',
        'Nintendo 64': 'n64',
        'Nintendo Entertainment System': 'nes',
        'Super Nintendo Entertainment System': 'snes',
        'Nintendo Game Boy Advance': 'gba',
        'Nintendo Game Boy Color': 'gbc',
        'Sega 32X': 'sega32x',
        'Sega Genesis': 'genesis',
        'Sega Master System': 'mastersystem',
        'NEC TurboGrafx-16': 'pcengine'
    }

    ratings: Dict[str, bool] = {
        'E - Everyone': True,
        'EC - Early Childhood': True,
        'E10+ - Everyone 10+': True,
        'T - Teen': True,
        'M - Mature': True,
        'Not Rated': True,
        'RP - Rating Pending': True
    }

    hide_regions: Dict[str, bool] = {
    }

    player_count: Dict[str, str] = {
        "2-Player Alternating": "2",
        "2-Player Simultaneous": "2",
        "3-Player Simultaneous": "3",
        "4-Player Alternating / 2-Player Simultaneous": "4",
        "4-Player Alternating": "4",
        "4-Player Simultaneous": "4",
        "6-Player Simultaneous": "6",
        "8-Player Alternating / 2-Player Simultaneous": "8",
        "8-Player Simultaneous": "8",
        "Cooperative; Multiplayer": "1+",
        "Kooperativ; Multiplayer": "1+",
        "Multiplayer": "1+",
        "Single Player": "1",
    }

    player_count_int: Dict[str, int] = {
        "2-Player Alternating": 2,
        "2-Player Simultaneous": 2,
        "3-Player Simultaneous": 3,
        "4-Player Alternating / 2-Player Simultaneous": 4,
        "4-Player Alternating": 4,
        "4-Player Simultaneous": 4,
        "6-Player Simultaneous": 6,
        "8-Player Alternating / 2-Player Simultaneous": 8,
        "8-Player Simultaneous": 8,
        "Cooperative; Multiplayer": 2,
        "Kooperativ; Multiplayer": 2,
        "Multiplayer": 2,
        "Single Player": 1,
    }

    retropie_user: str = 'jai'
    final_retropie_dir: str = '/home/' + retropie_user + '/RetroPie/'
    scrape: bool = False
    moby_games_api_key: str


@lru_cache
def _get_settings() -> Settings:
    _settings: Settings = Settings()
    return _settings


settings = _get_settings()
