import logging
from pathlib import Path
from typing import List, Dict, Any, Optional

import xml.etree.ElementTree as ET
# from xml.etree
from xml.dom import minidom
from src.launch_pi.retropie.models import RetroPiePlatformBase
from src.launch_pi.retropie.schemas import ReadRetroPieGame
from src.launch_pi.retropie.game import RetroPieGame
from pydantic import TypeAdapter
from src.launch_pi.config import settings
class RetroPiePlatform(RetroPiePlatformBase):
    # _games: List[RetroPieGame] = []
    games_list_xml: Optional[str] = None
    games_list_dir: Path = None

    def __init__(self, name: str, games: List[Dict[str, Any]], logger: logging.Logger = None):
        super().__init__(name=name, games=TypeAdapter(List[RetroPieGame]).validate_python(games))
        Path(settings.retropi_dir, 'roms', self.name).mkdir(exist_ok=True)
        Path(settings.retropi_dir, 'roms', self.name, 'images').mkdir(exist_ok=True)
        games_list: ET.Element = ET.Element('gameList')
        for game in self.games:
            if game.path:
                game.path = Path(settings.retropi_dir, 'roms', self.name, game.rom_name)
            if game.image:
                game.image = Path(settings.retropi_dir, 'roms', self.name, 'images', game.image.name)
            game.dump_xml(games_list_parent=games_list)

        self.games_list_xml = minidom.parseString(ET.tostring(games_list)).toprettyxml(indent="    ")
        self.games_list_dir = Path(settings.retropi_dir, 'emulationstation', 'gamelists', self.name)
        self.games_list_dir.mkdir(parents=True, exist_ok=True)

        # logger.info(self.games_list_xml)

    def write_game_list(self):
        output_file = Path(self.games_list_dir, 'gamelist.xml')
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(self.games_list_xml.replace('/media/jordan/PD1000/retropi/', '/home/jai/RetroPie/'))

    def get_game(self, id: str) -> RetroPieGame | None:
        for game in self.games:
            if game.id == id:
                return game
        return None

        # self.games =
