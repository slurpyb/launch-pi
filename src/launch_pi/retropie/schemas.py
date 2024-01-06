from pathlib import Path
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, HttpUrl, Field, ConfigDict, field_validator
from .models import RetroPieGameBase, RetroPiePlatformBase
from src.launch_pi.config import settings

class ReadRetroPieGame(RetroPieGameBase):
    id: Optional[str] = Field(...)
    name: Optional[str] = Field(default=None, alias='title')
    desc: Optional[str] = Field(default=None, alias='notes')
    image: Optional[Path] = Field(default=None)
    rating: Optional[float] = Field(default=0.0, alias='community_star_rating')
    developer: Optional[str] = Field(default=None)
    publisher: Optional[str] = Field(default=None)
    genre: Optional[str] = Field(default=None)
    players: Optional[int | str] = Field(default=None, alias='play_mode')
    releasedate: Optional[datetime | str] = Field(default=None, alias='release_date')
    path: Optional[str | Path] = Field(default=None, alias='rom_path')


    @field_validator('players')
    @classmethod
    def format_players(cls, v: str | int) -> str:
        if isinstance(v, str):
            count = settings.player_count_int.get(v)
            if count:
                return count
            else:
                return 1

    @field_validator('releasedate')
    @classmethod
    def format_releasedate(cls, v: datetime | str) -> str:
        if isinstance(v, datetime):
            iso_str = v.date().isoformat()
            iso_str = iso_str.replace('-', '')
            return iso_str + 'T000000'

class ReadRetroPiePlatform(RetroPiePlatformBase):
    name: str = Field(default=None)


    @field_validator('name')
    @classmethod
    def format_name(cls, v: str) -> str:
        return settings.platforms.get(v)