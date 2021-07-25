# DesktopPong
Game of pong that overlays other windows.

## Usage
After starting DesktopPong, you can move your paddle (red) by clicking and dragging. The AI paddle (green) will move automatically.

## Config
You can change the configuration values in `src/config.py`.

## Anti-Tamper
The anti-tamper system prevents tampering with the windows. However, it can cause lag and flashing (especially if the configuration values not fitting). You can disable it completely by setting `USE_ANTI_TAMPER` to `False` in `src/config.py`.

## Compatibility
Tested on Cinnamon 4.8 and 5.0 (with the panel at the bottom). There is a very good chance DesktopPong will not work on any other desktop environments.

## License
[MIT](https://choosealicense.com/licenses/mit/)
