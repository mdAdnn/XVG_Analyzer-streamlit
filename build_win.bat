@echo off
echo === Building XVG Analyzer for Windows ===
rmdir /s /q dist build 2>nul

REM Ensure pyinstaller is available
where pyinstaller >nul 2>&1 || (
    echo Installing pyinstaller...
    pip install pyinstaller
)

echo.
echo 🔧 Compiling XVG Analyzer with icon...
pyinstaller --noconfirm --clean --onefile --windowed ^
  --name "XVG_Analyzer" ^
  --add-data "app.py;." ^
  --icon "icon.ico" ^
  launch.py

echo.
echo ✅ Build complete!
echo 📦 Output file: dist\XVG_Analyzer.exe
pause
