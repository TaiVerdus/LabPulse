@echo off
chcp 65001 >nul
set PYTHONIOENCODING=utf-8

rem ============================================================
rem  验收工具·LSL 实时流模式（本文件是副本，位于课程空间 LabPulse）
rem  前提：OpenBCI_GUI 已连接设备，并已打开 LSL outlet
rem  双击运行后，脚本会自动查找 LSL 流并收 2-3 分钟数据
rem ============================================================

echo 请确认：OpenBCI_GUI 已连接设备，且 LSL outlet 已打开。
echo 确认后按任意键开始接收数据……
pause >nul
echo.

set "HERE=%~dp0"
set "CANON=%HERE%..\..\EEG\scripts"

if not exist "%CANON%\acceptance_check.py" (
  echo.
  echo [错误] 找不到验收脚本主本：
  echo        %CANON%\acceptance_check.py
  echo        请确认科研空间仍在 D:\Notes\EEG\EEG
  pause
  exit /b 1
)

cd /d "%CANON%"
"C:\Users\wshix\.workbuddy\binaries\python\envs\default\Scripts\python.exe" acceptance_check.py lsl

echo.
pause
