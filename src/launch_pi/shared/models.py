from pathlib import Path
from typing import Optional, List

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, HttpUrl, Field, ConfigDict

from src.launch_pi.config import settings

class ImageFileBase(BaseModel):
    image_path: Optional[Path] = None
