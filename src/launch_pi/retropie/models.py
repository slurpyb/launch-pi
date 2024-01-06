from pathlib import Path
from typing import List

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict, field_serializer


class RetroPieGameBase(BaseModel):
    model_config = ConfigDict(extra='ignore')
    id: Optional[str] = None
    name: Optional[str] = None
    desc: Optional[str] = None
    image: Optional[Path] = None
    thumbnail: Optional[Path] = None
    video: Optional[Path] = None
    rating: Optional[float] = None
    releasedate: Optional[str] = None
    developer: Optional[str] = None
    publisher: Optional[str] = None
    genre: Optional[str] = None
    players: Optional[int | str] = None
    playcount: Optional[int] = None
    lastplayed: Optional[datetime] = None
    path: Optional[Path] = None


    @field_serializer('path')
    def serialize_rom_path(self, path: Path, _info):
        if path:
            return path.absolute().as_posix()

    @field_serializer('image')
    def serialize_image_path(self, image: Path, _info):
        if image:
            return image.absolute().as_posix()

class RetroPiePlatformBase(BaseModel):
    name: Optional[str] = None
    games: Optional[List[RetroPieGameBase]] = None