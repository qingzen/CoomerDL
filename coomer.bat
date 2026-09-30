@echo off
setlocal
title Coomer Downloader

set SCRIPT=%~dp0coomer.py

:MENU
cls
echo.
echo  ============================================
echo    COOMER DOWNLOADER
echo  ============================================
echo.
echo    Select a service:
echo.
echo    [1] OnlyFans
echo    [2] Fansly
echo    [3] Fansdb
echo    [4] Candifans
echo    [0] Exit
echo.
set /p PILIHAN="   Your choice: "

if "%PILIHAN%"=="1" set SERVICE=onlyfans  & goto INPUT
if "%PILIHAN%"=="2" set SERVICE=fansly    & goto INPUT
if "%PILIHAN%"=="3" set SERVICE=fansdb    & goto INPUT
if "%PILIHAN%"=="4" set SERVICE=candifans & goto INPUT
if "%PILIHAN%"=="0" exit /b
echo    [!] Invalid choice, try again.
timeout /t 1 >nul
goto MENU

:INPUT
cls
echo.
echo  ============================================
echo    COOMER DOWNLOADER  ^>  %SERVICE%
echo  ============================================
echo.
set /p USER="   Creator username  : "
echo.
set /p LIMIT="   Photo limit (0 = all, e.g. 100) : "
if "%LIMIT%"=="" set LIMIT=0
echo.
set /p SKIP="   Skip already downloaded files? (y/n) : "
echo.

set EXTRA=
if /i "%SKIP%"=="y" set EXTRA=--skip-existing

echo  ============================================
echo   Starting download: %SERVICE% / %USER%
if not "%LIMIT%"=="0" echo   Limit: %LIMIT% photos
if /i "%SKIP%"=="y" echo   Mode: skip existing files
echo  ============================================
echo.

python "%SCRIPT%" %SERVICE% %USER% --limit %LIMIT% %EXTRA%

echo.
if %ERRORLEVEL%==0 (
    echo  [OK] Done! Photos saved to: %~dp0%USER%\
) else (
    echo  [!] Exited with error code %ERRORLEVEL%
)
echo.
set /p AGAIN="   Download another? (y/n) : "
if /i "%AGAIN%"=="y" goto MENU
exit /b
