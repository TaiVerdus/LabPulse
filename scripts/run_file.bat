@echo off
chcp 65001 >nul
set PYTHONIOENCODING=utf-8

rem ============================================================
rem  验收工具·文件模式（本文件是副本，位于课程空间 LabPulse）
rem  用法（二选一）：
rem   1) 把录好的数据文件【拖到这个 bat 图标上】松手
rem   2) 双击运行，然后按提示把文件路径粘贴进来，回车
rem ============================================================

set "DATAFILE=%~1"
if not "%DATAFILE%"=="" goto gotfile

echo 请把录好的数据文件（CSV / EDF / BDF / FIF）拖进这个窗口，然后按回车：
set /p "DATAFILE="
if "%DATAFILE%"=="" (
  echo 没有输入文件路径，退出。
  pause
  exit /b 1
)

:gotfile
set DATAFILE=%DATAFILE:"=%

set "HERE=%~dp0"
set "CANON=%HERE%..\..\EEG\scripts"

if not exist "%CANON%\acceptance_check.py" (
  echo.
  echo [错误] 找不到验收脚本主本：
  echo        %CANON%\acceptance_check.py
  echo        请确认科研空间仍在 C:\Users\wshix\WorkBuddy\EEG
  pause
  exit /b 1
)

echo.
echo 正在分析文件：%DATAFILE%
echo.

cd /d "%CANON%"
"C:\Users\wshix\.workbuddy\binaries\python\envs\default\Scripts\python.exe" acceptance_check.py file "%DATAFILE%"

echo.
pause
