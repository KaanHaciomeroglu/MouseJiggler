@echo off
pyinstaller --onefile --windowed ^
  --icon=icon.ico ^
  --add-data "icon.ico;." ^
  --name=MouseJiggler ^
  main.py
echo.
echo Build tamamlandi! dist\MouseJiggler.exe hazir.
pause
