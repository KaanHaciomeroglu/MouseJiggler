import os
import sys
import pystray
from PIL import Image


def _base_path():
    if hasattr(sys, "_MEIPASS"):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))


_ICON_PATH = os.path.join(_base_path(), "icon.ico")


def _create_icon_image():
    return Image.open(_ICON_PATH).convert("RGBA").resize((64, 64))


class TrayIcon:
    def __init__(self, on_show, on_toggle, on_quit):
        self._on_show = on_show
        self._on_toggle = on_toggle
        self._on_quit = on_quit
        self._icon = None

    def start(self):
        menu = pystray.Menu(
            pystray.MenuItem("Aç", lambda: self._on_show(), default=True),
            pystray.MenuItem("Başlat / Durdur", lambda: self._on_toggle()),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Çıkış", lambda: self._quit()),
        )
        self._icon = pystray.Icon("MouseJiggler", _create_icon_image(), "Mouse Jiggler", menu)
        self._icon.run_detached()

    def _quit(self):
        self._on_quit()
        if self._icon:
            self._icon.stop()

    def stop(self):
        if self._icon:
            self._icon.stop()
