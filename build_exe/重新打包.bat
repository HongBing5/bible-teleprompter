@echo off
chcp 936 >nul
cd /d "%~dp0"
taskkill /F /IM "bible-teleprompter_v1.2.0.exe" >nul 2>&1
taskkill /F /IM "bible-teleprompter.exe" >nul 2>&1
C:/Users/HB/.workbuddy/binaries/python/envs/default/Scripts/pyinstaller.exe bible-teleprompter.spec --noconfirm
if exist "dist\bible-teleprompter_v1.2.0.exe" (explorer /select,"%~dp0dist\bible-teleprompter_v1.2.0.exe") else (echo BUILD FAILED - see errors above)
pause
