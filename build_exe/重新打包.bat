@echo off
chcp 936 >nul
cd /d "%~dp0"
taskkill /F /IM "圣经提词器_v1.0.exe" >nul 2>&1
taskkill /F /IM "圣经提词器.exe" >nul 2>&1
C:/Users/HB/.workbuddy/binaries/python/envs/default/Scripts/pyinstaller.exe 圣经提词器.spec --noconfirm
if exist "dist\圣经提词器_v1.0.exe" (explorer /select,"%~dp0dist\圣经提词器_v1.0.exe") else (echo BUILD FAILED - see errors above)
pause
