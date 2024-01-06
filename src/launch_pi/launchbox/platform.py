from pathlib import Path
import xml.etree.ElementTree as ET
from typing import List, Dict

from src.launch_pi.launchbox.models import LaunchBoxPlatformBase
from src.launch_pi.launchbox.schemas import ReadGameData
from src.launch_pi.launchbox.game import LaunchBoxGame
from src.launch_pi.config import settings


class LaunchBoxPlatform(LaunchBoxPlatformBase):
    _games: List[LaunchBoxGame] = []
    missing_images: Dict[str, str] = {}

    def __init__(self, name):
        super().__init__(name=name)
        # self.platform_xml = ET.parse(Path(settings.launchbox_path,  f'Data/Platforms/{self.name}.xml'))
        self.games = ET.parse(Path(settings.launchbox_path,  f'Data/Platforms/{self.name}.xml'))

    def get_game(self, id: str) -> LaunchBoxGame | None:
        for game in self.games:
            if game.id == id:
                return game
        return None

    @property
    def games(self) -> List[LaunchBoxGame]:
        return self._games

    @games.setter
    def games(self, games_data: ET.ElementTree) -> None:
        for item in games_data.getroot():
            if item.tag == 'Game':
                if item.tag.find('ID'):
                    game_data = ReadGameData(**{el.tag: el.text for el in item})
                    self._games.append(LaunchBoxGame(game_data.model_dump(exclude_none=True)))

