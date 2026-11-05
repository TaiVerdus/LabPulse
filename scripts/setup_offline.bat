@echo off
chcp 65001 >nul
set PYTHONUTF8=1
cd /d "%~dp0.."
python -X utf8 -m venv --without-pip --system-site-packages .venv
if errorlevel 1 goto failed
if exist "wheelhouse\pylsl-1.18.6-py3-none-win_amd64.whl" (
  python -m pip --python .venv install --no-index --find-links wheelhouse -r requirements-offline.txt
) else (
  python -m pip --python .venv install -r requirements-offline.txt
)
if errorlevel 1 goto failed
.venv\Scripts\python.exe -X utf8 -m offline.health
if errorlevel 1 goto failed
echo 依赖已就绪。数据未下载时，联网执行 .venv\Scripts\python.exe -m offline.fetch
pause
exit /b 0
:failed
echo 环境准备失败，请保留报错。需要64位 Python 和可用的 pip。
pause
exit /b 1
