import threading
import pyautogui

pyautogui.FAILSAFE = False


class JigglerThread(threading.Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self._stop_event = threading.Event()
        self.interval = 30
        self.pixels = 5
        self._direction = 0

    def run(self):
        while not self._stop_event.is_set():
            elapsed = 0.0
            while elapsed < self.interval and not self._stop_event.is_set():
                self._stop_event.wait(0.2)
                elapsed += 0.2
            if not self._stop_event.is_set():
                self._move()

    def _move(self):
        moves = [(self.pixels, 0), (-self.pixels, 0), (0, self.pixels), (0, -self.pixels)]
        dx, dy = moves[self._direction % 4]
        self._direction += 1
        pyautogui.moveRel(dx, dy, duration=0.1)

    def stop(self):
        self._stop_event.set()
