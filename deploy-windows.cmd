@echo off
setlocal
cd /d "%~dp0"
if "%~1"=="" (
  echo Usage: deploy-windows.cmd YOUR-FIREBASE-PROJECT-ID
  exit /b 2
)
if not exist "firebase.json" (
  echo ERROR: firebase.json missing
  exit /b 3
)
call firebase.cmd deploy --only hosting --project "%~1"
if errorlevel 1 exit /b 1
echo VERIFY: Inspect visible footer version: SESSION / V4.0
echo VERIFY: Test mobile consent, audio, portrait and burning; run smoke test against actual URL.
endlocal
