import uuid
from pathlib import Path
from typing import Dict, Any
import xml.etree.ElementTree as ET
from .models import RetroPieGameBase
from src.launch_pi.config import settings
class RetroPieGame(RetroPieGameBase):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def rom_name(self) -> str:
        return self.path.name

    def dump_xml(self, games_list_parent: ET.Element):

        parent = ET.SubElement(games_list_parent, 'game')
        try:
            for key, value in self.model_dump(exclude_none=True, exclude='id').items():
                child = ET.SubElement(parent, key)
                child.text = str(value)
        except Exception as e:
            print(e)

        # self.image =