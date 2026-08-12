"""
セルラン API (FastAPI)
- GET /api/rankings   → 最新のTOP50
- GET /api/health
静的ファイルも配信可能（ローカル確認用）
"""
import json
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from collector.main import collect_once, LATEST_PATH

app = FastAPI(title="Cell Rank API", version="1.0.0")

# CORS（GitHub Pages から直接叩く場合に備える）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静的ファイル（index.html など）
STATIC_DIR = ROOT
if (ROOT / "index.html").exists():
    app.mount("/static", StaticFiles(directory=str(ROOT / "static")), name="static")


@app.on_event("startup")
def startup_event():
    """起動時に一度収集し、スケジューラを開始"""
    print("=== Cell Rank API 起動 ===")
    # 起動直後に1回収集
    try:
        collect_once()
    except Exception as e:
        print(f"初期収集エラー（続行）: {e}")

    # 1時間おきに収集
    scheduler = BackgroundScheduler(timezone="Asia/Tokyo")
    scheduler.add_job(collect_once, "interval", hours=1, id="hourly_collect")
    scheduler.start()
    print("スケジューラ開始: 1時間おきに収集")


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/rankings")
def get_rankings():
    if not LATEST_PATH.exists():
        raise HTTPException(status_code=404, detail="まだデータがありません。しばらく待つか手動で収集してください。")
    with open(LATEST_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@app.get("/")
def root():
    """ローカル確認用に index.html を返す"""
    index_path = ROOT / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return HTMLResponse("<h1>Cell Rank API</h1><p><a href='/api/rankings'>/api/rankings</a></p>")


@app.get("/data/rankings_latest.json")
def get_json_file():
    if not LATEST_PATH.exists():
        raise HTTPException(status_code=404, detail="data not found")
    return FileResponse(LATEST_PATH, media_type="application/json")
