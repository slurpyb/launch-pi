# Launch Pi
Transfer your LaunchBox ROM library to RetroPie/EmulationStation

Thanks to Wts42 (https://github.com/wts42/) for insipiration and original python script.

## TODO
- Write better documentation
- Finish support for scraping missing Box Art
- Refactor config/settings management

## Running
- Copy LaunchBox directory on Windows machines to external drive (commonly installed to C:/Users/%USER%/LaunchBox on Windows)
- Add variables via .env
  - launchbox_path: LaunchBox directory (folder on your external drive i.e. /media/$USER/externaldrive/LaunchBox)
  - retropi_dir: destination for app to copy roms and images (i.e. /media/$USER/externaldrive/retropi)
- Edit config.py platforms for desired platforms (dict with LaunchBox platform names as keys, EmulationStation platform names as values)
- 
```bash
poetry install
chmod a+x ./scripts/run.sh
./scripts/run.sh
```