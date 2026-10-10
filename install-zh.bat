@echo off
rem Strata Chinese Edition - installer. Messages come from Python (UTF-8).
chcp 65001 >nul
setlocal
title Strata Chinese Edition - install
cd /d "%~dp0"

set PY=
if exist ".venv\Scripts\python.exe" set PY=.venv\Scripts\python.exe
if not defined PY (
  where py >nul 2>nul && set PY=py -3
)
if not defined PY set PY=python

%PY% apply_zh_ui.py %*
echo.
pause
