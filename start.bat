@echo off
chcp 65001 >nul
title Cell Rank - ゲームセルラン収集 & API

echo ========================================
echo   ゲームセルラン TOP50  収集 & API
echo ========================================
echo.

cd /d "%~dp0"
echo 作業フォルダ: %CD%
echo.

REM Pythonがあるか確認
where python >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python が見つかりません。
    echo Python 3.10以上をインストールしてから再実行してください。
    pause
    exit /b 1
)

echo 使用するPython:
python --version
echo.

REM 仮想環境がなければ作成
if not exist "venv\Scripts\python.exe" (
    echo 仮想環境を作成しています...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] 仮想環境の作成に失敗しました。
        pause
        exit /b 1
    )
    echo 仮想環境を作成しました。
) else (
    echo 仮想環境は既に存在します。
)

echo.
echo 依存パッケージをインストール中...（初回は数分かかります）
echo.

REM ★重要: activateに頼らず、venvのpythonを直接使う
venv\Scripts\python.exe -m pip install --upgrade pip
venv\Scripts\python.exe -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo [ERROR] パッケージのインストールに失敗しました。
    echo インターネット接続を確認してから再実行してください。
    pause
    exit /b 1
)

echo.
echo 必須パッケージの確認...
venv\Scripts\python.exe -c "import fastapi, uvicorn, apscheduler, requests; print('OK: fastapi / uvicorn / apscheduler / requests')"
if errorlevel 1 (
    echo [ERROR] 必要なパッケージが正しくインストールされていません。
    pause
    exit /b 1
)

echo.
echo ----------------------------------------
echo  API起動中  http://127.0.0.1:8000
echo  1時間おきに自動でセルランを収集します
echo  ブラウザで http://127.0.0.1:8000 を開くと確認できます
echo  終了するにはこのウィンドウを閉じてください
echo ----------------------------------------
echo.

REM ★重要: venvのpythonで直接uvicornを起動
venv\Scripts\python.exe -m uvicorn api.main:app --host 127.0.0.1 --port 8000

echo.
echo APIが終了しました。
pause
