#!/usr/bin/env python3

"""Launch Pi
Author(s): Jordan Sweeting (@slurpyb)

Transfer LaunchBox roms and metadata to RetroPi / Handheld Linux (e.g. Anbernic)
"""

import logging
from loguru import logger

from . import app

# logging.basicConfig(handler)
logging.basicConfig(level=logging.DEBUG,
                    format="[%(asctime)s] %(name)s {%(filename)s:%(lineno)d} %(levelname)s - %(message)s")
logging.basicConfig(level=logging.INFO,
                    format="[%(asctime)s] %(name)s {%(filename)s:%(lineno)d} %(levelname)s - %(message)s")

LOG = logger


def main():
    return app.run(logger=LOG)


if __name__ == "__main__":
    main()
