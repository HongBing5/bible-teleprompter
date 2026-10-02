@echo off
chcp 936 >nul
cd /d "%~dp0"

rem 注意：本文件所有提示用英文，避免 GBK 控制台下中文乱码。
rem 版本号不再写死在这里：spec 和 version_info.txt 都从项目根 version.json 派生。

set PY=C:/Users/HB/.workbuddy/binaries/python/envs/default/Scripts/python.exe

echo [1/3] Sync version_info.txt from version.json ...
"%PY%" make_version_info.py

echo [2/3] Kill running app and clean old build ...
taskkill /F /IM "bible-teleprompter_v*.exe" >nul 2>&1
del /Q "dist\bible-teleprompter_v*.exe" >nul 2>&1

echo [3/3] Building exe with PyInstaller ...
"%PY%" -m PyInstaller bible-teleprompter.spec --noconfirm

set BUILT=
for %%f in ("dist\bible-teleprompter_v*.exe") do set BUILT=%%~nxf
if defined BUILT (
  echo.
  echo BUILD OK: dist\%BUILT%
  explorer /select,"%~dp0dist\%BUILT%"
) else (
  echo.
  echo BUILD FAILED - see errors above
)
pause
