@echo off
chcp 65001 >nul
title Cell Rank - ゲームセルラン収集 & API

echo ========================================
echo   ゲームセルラン TOP50  収集 & API
echo ========================================
echo.

cd /d "%~dp0"

REM Pythonがあるか確認
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python が見つかりません。
    echo Python 3.10以上をインストールしてから再実行してください。
    pause
    exit /b 1
)

REM 仮想環境がなければ作成
if not exist "venv\" (
    echo 仮想環境を作成しています...
    python -m venv venv
)

call venv\Scripts\activate.bat

echo 依存パッケージを確認・インストール中...
pip install -r requirements.txt -q

echo.
echo ----------------------------------------
echo  API起動中  http://127.0.0.1:8000
echo  1時間おきに自動でセルランを収集します
echo  ブラウザで http://127.0.0.1:8000 を開くと確認できます
echo  終了するにはこのウィンドウを閉じてください
echo ----------------------------------------
echo.

python -m uvicorn api.main:app --host 127.0.0.1 --port 8000 --reload

pause
