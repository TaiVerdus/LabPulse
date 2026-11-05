@echo off
chcp 65001 >nul
set PYTHONUTF8=1
cd /d "%~dp0.."
.venv\Scripts\python.exe -X utf8 -m offline.health
if errorlevel 1 goto failed
.venv\Scripts\python.exe -X utf8 -m unittest discover -s tests -v
if errorlevel 1 goto failed
.venv\Scripts\python.exe -X utf8 -m offline.selftest
if errorlevel 1 goto failed
echo 软件检查已通过。本次仅测试模拟流。
pause
exit /b 0
:failed
echo 检查未通过，请保留报错。
pause
exit /b 1
