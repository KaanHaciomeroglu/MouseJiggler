import time
import threading
import logging
import pyautogui

pyautogui.FAILSAFE = False  # tray "Çıkış" ile durdurmak için köşe-kaçış devre dışı

logger = logging.getLogger(__name__)


class JigglerThread(threading.Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self._stop_event = threading.Event()
        self.interval = 30
        self.pixels = 5
        self._direction = 0

    def run(self):
        while not self._stop_event.is_set():
            deadline = time.monotonic() + self.interval
            while time.monotonic() < deadline and not self._stop_event.is_set():
                self._stop_event.wait(0.2)
            if not self._stop_event.is_set():
                self._move()

    def _move(self):
        moves = [(self.pixels, 0), (-self.pixels, 0), (0, self.pixels), (0, -self.pixels)]
        dx, dy = moves[self._direction % 4]
        self._direction += 1
        try:
            pyautogui.moveRel(dx, dy, duration=0.1)
        except Exception:
            logger.exception("Mouse hareketi başarısız")

    def stop(self):
        self._stop_event.set()
