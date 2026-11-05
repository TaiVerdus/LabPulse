@echo off
chcp 65001 >nul
set PYTHONUTF8=1
cd /d "%~dp0.."
if not exist ".venv\Scripts\python.exe" (
  echo 请先联网运行 scripts\setup_offline.bat
  pause
  exit /b 1
)
set "LP_PY=.venv\Scripts\python.exe"
"%LP_PY%" -X utf8 -m offline.health
if errorlevel 1 goto failed
"%LP_PY%" -X utf8 -m offline.pipeline
if errorlevel 1 goto failed
"%LP_PY%" -X utf8 -m offline.replay --limit 20
if errorlevel 1 goto failed
echo 已完成公开数据离线回放。结果位于 reports\offline。本次不验证设备。
pause
exit /b 0
:failed
echo 运行失败，请保存本窗口完整报错。不要把失败结果作为完成证据。
pause
exit /b 1
