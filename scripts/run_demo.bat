@echo off
chcp 65001 >nul
set PYTHONIOENCODING=utf-8

rem ============================================================
rem  验收工具·练习模式（本文件是副本，位于课程空间 LabPulse）
rem  脚本主本(canonical)在科研空间，本文件只负责定位并执行它。
rem  用法：双击即可，不需要任何命令行操作。
rem ============================================================

set "HERE=%~dp0"
set "CANON=%HERE%..\..\EEG\scripts"

if not exist "%CANON%\acceptance_check.py" (
  echo.
  echo [错误] 找不到验收脚本主本：
  echo        %CANON%\acceptance_check.py
  echo.
  echo        请确认科研空间仍在 D:\Notes\EEG\EEG
  echo        如果它已经被移动，请用记事本打开本文件，
  echo        把第 12 行 set "CANON=..." 改成新的 scripts 目录，再双击重试。
  echo.
  pause
  exit /b 1
)

cd /d "%CANON%"
"C:\Users\wshix\.workbuddy\binaries\python\envs\default\Scripts\python.exe" acceptance_check.py demo

echo.
pause
