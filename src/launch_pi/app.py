import io
import requests
import logging
import os
from pathlib import Path
from shutil import copy
from typing import Optional, List, Any, Dict, Tuple
from PIL import Image, PngImagePlugin, TiffImagePlugin
from pydantic import BaseModel, Field, ConfigDict, field_validator

from .config import settings

import xml.etree.ElementTree as ET
# from xml.etree
from xml.dom import minidom
from src.launch_pi.launchbox import LaunchBoxPlatform
from src.launch_pi.retropie import RetroPiePlatform, ReadRetroPieGame
TiffImagePlugin.logger.disabled = True
PngImagePlugin.logger.disabled = True



class GameBase(BaseModel):
    model_config = ConfigDict(extra='ignore')
    platform_name: str = Field(..., exclude=True)
    id: Optional[str] = Field(default=None, alias='ID', exclude=True)
    name: Optional[str] = Field(default=None, alias='Title', serialization_alias='name')
    developer: Optional[str] = Field(default=None, alias='Developer', serialization_alias='developer')
    description: Optional[str] = Field(default=None, alias='Notes', serialization_alias='desc')
    # image_path: Optional[Path] = Field(default=None)
    image: Optional[str | Path] = Field(default=None, serialization_alias='image')
    star_rating: Optional[float] = Field(default=None, alias='StarRating', serialization_alias='rating')
    release_date: Optional[str] = Field(default=None, alias='ReleaseDate', serialization_alias='releasedate')
    publisher: Optional[str] = Field(default=None, alias='Publisher', serialization_alias='publisher')
    genre: Optional[str] = Field(default=None, alias='Genre', serialization_alias='genre')
    players: Optional[str] = Field(default=None, alias='PlayMode', serialization_alias='players')
    rating: Optional[str] = Field(default=None, alias='Rating', exclude=True)
    region: Optional[str] = Field(default=None, alias='Region', exclude=True)
    rom_path: Optional[str] = Field(default=None, serialization_alias='path')
    rom_src_path: Optional[str] = Field(default=None, alias='ApplicationPath', exclude=True)
    is_hidden: Optional[bool] = Field(default=None, alias='Hide', exclude=True)
    is_broken: Optional[bool] = Field(default=None, alias='Broken', exclude=True)
    is_favorite: Optional[bool] = Field(default=None, alias='Favorite', serialization_alias='favorite')

    @field_validator('release_date')
    @classmethod
    def format_release_date(cls, v: str) -> str:
        return v.replace("-", "").split("T")[0] + "T000000"

    @field_validator('players')
    @classmethod
    def format_players(cls, v: str) -> str:
        return settings.player_count.get(v)

    @field_validator('star_rating')
    @classmethod
    def format_star_rating(cls, v: float) -> float:
        return int(v) * 2 / 10

class Game(GameBase):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.image = self._get_image(name=self.name)


    def _get_image(self, name: str) -> Path:
        image_name = name.replace(':', '_').replace("'", '_').replace('/', '_')
        image_name = image_name + '-01'
        launchbox_image_path = Path(settings.launchbox_path, 'Images', self.platform_name, 'Box - Front')
        for filename in launchbox_image_path.glob('**/*'):
            if filename.name.startswith(image_name):
                return filename

    def copy_rom(self):
        src = self.rom_path.replace('\\', '/')
        copy(Path(settings.launchbox_path, src), Path(settings.retropi_dir, 'roms', settings.platforms.get(self.platform_name)))


    def save_image(self):
        destination_filename = Path(settings.retropi_dir, 'roms', settings.platforms.get(self.platform_name), 'images', self.image_path.name)
        try:
            image = Image.open(self.image_path)
            image.load()
            width = int(image.size[0])
            height = int(image.size[1])
            ratio = 0
            if (width > 500) and (width > height):
                ratio = width / 500
            elif (height > 500) and (height > width):
                ratio = height / 500
            if ratio > 0:
                width = width / ratio
                height = height / ratio
                size = (width, height)
                image.thumbnail(size)
                image.save(destination_filename)
            self.image_path = destination_filename
        except Exception as e:
            print(e)


class Platform:
    def __init__(self, name: str, logger: logging.Logger = None):
        self.name = settings.platforms.get(name)
        self.launchbox_name = name
        self.logger = logger
        self.roms_path = Path(settings.retropi_dir, 'roms', self.name)
        self.images_path = Path(self.roms_path, 'images')
        self.gamelists_path = Path(settings.retropi_dir, 'gamelists', self.launchbox_name)
        self.gamelists_file = Path(self.gamelists_path, 'gamelist.xml')

        self.launchbox_xml_tree = ET.parse(Path(settings.launchbox_path,  f'Data/Platforms/{name}.xml'))

        self.launchbox_img_path = Path(settings.launchbox_path, 'Images', name, 'Box - Front')

        self.images = []
        self.games = []

    def _initialize_paths(self):
        self.roms_path.mkdir(parents=False, exist_ok=True)
        self.gamelists_path.mkdir(parents=True, exist_ok=True)
        self.images_path.mkdir(parents=False, exist_ok=True)


    def _build_gamelist(self):
        top = ET.Element('gameList')
        for game in self.games:
            game.image = str(game.image)
            _game: dict = game.model_dump(by_alias=True)
            # print(_game)
            child = ET.SubElement(top, 'game')
            for key, value in _game.items():
                child_content = ET.SubElement(child, key)
                child_content.text = value

        try:
            xmlstr = minidom.parseString(ET.tostring(top)).toprettyxml(indent="    ")
            with open(self.gamelists_file, "w", encoding="utf-8") as f:
                f.write(xmlstr)
        except Exception as e:
            self.logger.error(e)

    def begin(self):
        self._initialize_paths()

        for item in self.launchbox_xml_tree.getroot():
            this_game = dict()
            if item.tag == 'Game':

                for el in item:
                    this_game.update({el.tag: el.text})
            if this_game.get('ID'):
                self.games.append(Game(platform_name=self.launchbox_name, **this_game))

        self._build_gamelist()


class Scraper:
    def __init__(self):
        self.api_key = settings.moby_games_api_key
        self.endpoint_base = 'https://api.mobygames.com/v1/'
        self.platform_ids = self._get_platforms()

    def _get_platforms(self) -> dict:
        d = dict()
        r = requests.get(f'https://api.mobygames.com/v1/platforms?api_key={settings.moby_games_api_key}').json()
        for platform in r.get('platforms'):
            d.update({platform.get('platform_name'): platform.get('platform_id')})
        return d

    def get_game_rating(self, platform_name: str, game_name: str):
        r = requests.get(
            f'https://api.mobygames.com/v1/games?api_key={settings.moby_games_api_key}&title={game_name}&platform={platform_id}')
        return r.json()



class Application:
    retropi_roms_path: Path = Path(settings.retropi_dir, 'roms')
    retropi_gamelists_path: Path = Path(settings.retropi_dir, 'gamelists')


    def __init__(self, logger: logging.Logger = None, scrape: bool = False):
        self.logger = logger
        self.scraper = Scraper() if scrape else None

    def begin(self):
        self._initialize_paths()

        for launchbox_platform_name, retropi_platform_name in settings.platforms.items():
            self.logger.info(f'Handling {launchbox_platform_name} ({retropi_platform_name})')
            launchbox_platform = LaunchBoxPlatform(name=launchbox_platform_name)
            retropie_platform = RetroPiePlatform(name=retropi_platform_name, games=[ReadRetroPieGame(**x.model_dump()).model_dump() for x in launchbox_platform.games], logger=self.logger)
            for count, game in enumerate(retropie_platform.games):
                launchbox_game = launchbox_platform.get_game(id=game.id)
                if launchbox_game:
                    if launchbox_game.missing_box_front_image:
                        launchbox_platform.missing_images.update({launchbox_game.id: launchbox_game.title})
                        self.logger.warning(f'Box Image missing for {launchbox_game.title}, skipping.')
                    else:
                        self.copy_image(launchbox_game.image, game.image)
                self.copy_rom(launchbox_game.rom_path, game.path.absolute())
                self.logger.info(f'Dumped {launchbox_game.title}. Progress: {count} / {len(retropie_platform.games)}')

            retropie_platform.write_game_list()

            self.logger.info(f'Dump complete for platform {launchbox_platform.name}')
            self.logger.info(f'Missing images: {launchbox_platform.missing_images}')


    def copy_image(self, launchbox_image_path: Path, retropie_image_path: Path):
        try:
            # self.logger.info(f'{launchbox_image_path}: {launchbox_image_path.is_file()}')
            # self.logger.info(f'{retropie_image_path}: {retropie_image_path.is_file()}')
            with Image.open(launchbox_image_path) as _img:
                _img_width = int(_img.size[0])
                _img_height = int(_img.size[1])
                _img_ratio = 0
                if (_img_width > 500) and (_img_width > _img_height):
                    _img_ratio = _img_width / 500
                elif (_img_height > 500) and (_img_height > _img_width):
                    _img_ratio = _img_height / 500
                if _img_ratio > 0:
                    _img_width = _img_width / _img_ratio
                    _img_height = _img_height / _img_ratio
                    _img_size = (_img_width, _img_height)
                    _img.thumbnail(_img_size)
                    _image = _img
                    _image.save(retropie_image_path)
                else:
                    copy(launchbox_image_path, retropie_image_path)
                # self.logger.info(f'Copied {launchbox_image_path.absolute()} to {retropie_image_path.absolute()}')
        except Exception as e:
             self.logger.error(e)


    def copy_rom(self, launchbox_rom_path: Path, retropie_rom_path: Path):
        try:
            copy(launchbox_rom_path, retropie_rom_path)
        except Exception as e:
            self.logger.error(e)


    def _initialize_paths(self) -> None:
        try:
            self.retropi_roms_path.mkdir(parents=True, exist_ok=False)
            self.logger.info(f'Created Retropi ROMS directory.')
        except FileExistsError as folder_exists_err:
            self.logger.error(f'Retropi ROMS directory already exists, skipping.')

        try:
            self.retropi_gamelists_path.mkdir(parents=True, exist_ok=False)
            self.logger.info(f'Created RetroPi/EmulationStation Gameslists directory.')
        except FileExistsError as folder_exists_err:
            self.logger.error(f'RetroPi/EmulationStation Gameslists directory already exists, skipping.')



def run(logger: logging.Logger = None):
    app = Application(logger)
    app.begin()
