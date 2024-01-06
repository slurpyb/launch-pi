from pathlib import Path

from src.launch_pi.shared.models import ImageFileBase


class ImageFile(ImageFileBase):
    image_path: Path
