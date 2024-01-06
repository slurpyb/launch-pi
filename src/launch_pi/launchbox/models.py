from pathlib import Path
from typing import Optional, List

import xml.etree.ElementTree as ET
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, HttpUrl, Field, ConfigDict

from src.launch_pi.config import settings


class LaunchBoxGameBase(BaseModel):
    model_config = ConfigDict(extra='ignore')
    application_path: Optional[str] = Field(None)
    developer: Optional[str] = Field(None)
    favorite: Optional[bool] = Field(None)
    id: Optional[str] = Field(None)
    notes: Optional[str] = Field(None)
    platform: Optional[str] = Field(None)
    publisher: Optional[str] = Field(None)
    rating: Optional[str] = Field(None)
    release_date: Optional[datetime] = Field(None)
    root_folder: Optional[str] = Field(None)
    source: Optional[str] = Field(None)
    star_rating_float: Optional[float] = Field(None)
    star_rating: Optional[int] = Field(None)
    community_star_rating: Optional[float] = Field(None)
    community_star_rating_total_votes: Optional[int] = Field(None)
    status: Optional[str] = Field(None)
    database_id: Optional[int] = Field(None)
    title: Optional[str] = Field(None)
    version: Optional[str] = Field(None)
    play_mode: Optional[str] = Field(None)
    region: Optional[str] = Field(None)
    hide: Optional[bool] = Field(None)
    broken: Optional[bool] = Field(None)
    clone_of: Optional[str] = Field(None)
    genre: Optional[str] = Field(None)
    missing_box_front_image: Optional[bool] = Field(None)
    release_type: Optional[str] = Field(None)
    max_players: Optional[int] = Field(None)
    rom_path: Optional[Path] = Field(None)
    rom_file_name: Optional[str] = Field(None)



class LaunchBoxPlatformBase(BaseModel):
    name: Optional[str] = None
    # platform_xml: Optional[ET.ElementTree] = None
    # games: Optional[List[LaunchBoxGame]] = []
