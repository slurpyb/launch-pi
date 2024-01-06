from pathlib import Path
import xml.etree.ElementTree as ET
from typing import List, Any, Dict
from PIL import Image
from src.launch_pi.launchbox.models import LaunchBoxGameBase
from src.launch_pi.config import settings
from src.launch_pi.shared.image import ImageFile


class LaunchBoxGame(LaunchBoxGameBase):
    image: Path | None = None

    def __init__(self, game_data: Dict[str, Any]):
        super().__init__(**game_data)
        self.rom_path = Path(settings.launchbox_path, self.application_path.replace('\\', '/'))
        self.rom_file_name = self.rom_path.name
        self.image = self._find_image()



    def _find_image(self) -> Path | None:
        _images_dir = Path(settings.launchbox_path, 'Images', self.platform, 'Box - Front')
        _title = self.title.replace(":", "_").replace("'", "_").replace("/", "_")
        for file in _images_dir.glob('**/*'):
            if file.name.startswith(_title + '-01'):
                return file
        return None
