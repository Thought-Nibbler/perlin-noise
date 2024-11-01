@echo off

if "%~1"=="" (
  echo 引数にPythonバージョンを指定してください。
  echo 例 : install.bat 3.13.0
  exit /b
)

del poetry.lock
if %errorlevel% neq 0 (
    echo エラーのため中断します。
    exit /b %errorlevel%
)
rmdir /S /Q .venv
if %errorlevel% neq 0 (
    echo エラーのため中断します。
    exit /b %errorlevel%
)

poetry config virtualenvs.in-project true
poetry env use "%HOMEDRIVE%%HOMEPATH%\.pyenv\pyenv-win\versions\%~1\python.exe"
if %errorlevel% neq 0 (
    echo エラーのため中断します。
    poetry env info
    exit /b %errorlevel%
)
poetry env info
poetry install
