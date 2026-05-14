# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

## [1.0.1] - 2026-05-14

### Fixed
- Thread-safe Tkinter updates: tray callbacks now marshalled via `after(0, ...)` to prevent UI corruption
- Double `stop()` bug on quit eliminated by removing redundant `_quit` method in `TrayIcon`
- `JigglerThread.join(timeout=2)` added in `_stop()` and `_quit()` to prevent overlapping threads
- Interval timing drift fixed: replaced float accumulation with `time.monotonic()` deadline
- Silent thread death fixed: `pyautogui.moveRel` exceptions now caught and logged
- Slider values now use `round()` instead of `int()` for correct rounding
- Status label text inconsistency fixed (`"Durum: PASiF"` unified)
- `ctypes` AppUserModelID call guarded with `sys.platform == "win32"`
- `self.destroy()` added after `self.quit()` for clean Tk teardown

### Added
- `utils.py` with shared `base_path()` helper — eliminates duplication between `ui.py` and `tray.py`

## [1.0.0] - 2026-05-07

### Added
- Start/Stop control with a single button
- Configurable interval setting (10–120 seconds)
- Configurable movement amount (1–20 pixels)
- System tray support — minimize to tray, double-click to restore
- Custom icon with clean dark-mode UI
- Standalone `.exe` build via PyInstaller

[1.0.1]: https://github.com/kaanhaciomeroglu/Mouse_Jiggler/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/kaanhaciomeroglu/Mouse_Jiggler/releases/tag/v1.0.0
