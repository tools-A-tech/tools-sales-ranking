"""
セルラン収集メイン
1時間おきに iOS / Android ゲームTOP50を取得して rankings_latest.json を更新
"""
import json
import os
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

# 親ディレクトリをパスに追加
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from collector.ios import fetch_ios_game_top50
from collector.android import fetch_android_game_top50

JST = timezone(timedelta(hours=9))
DATA_DIR = ROOT / "data"
LATEST_PATH = DATA_DIR / "rankings_latest.json"


def collect_once() -> dict:
    print(f"[{datetime.now(JST).strftime('%Y-%m-%d %H:%M:%S')}] 収集開始...")

    ios_list = fetch_ios_game_top50(50)
    android_list = fetch_android_game_top50(50)

    now = datetime.now(JST)
    payload = {
        "updated_at": now.isoformat(),
        "updated_at_display": now.strftime("%Y-%m-%d %H:%M JST"),
        "ios": ios_list,
        "android": android_list,
        "meta": {
            "ios_count": len(ios_list),
            "android_count": len(android_list),
            "limit": 50,
            "category": "Games"
        }
    }

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(LATEST_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print(f"  iOS   : {len(ios_list)}件")
    print(f"  Android: {len(android_list)}件")
    print(f"  保存先: {LATEST_PATH}")

    # GitHub 自動反映（.env に設定がある場合のみ）
    try:
        from collector.github_push import push_to_github
        push_to_github()
    except Exception as e:
        print(f"[GitHub] push処理スキップ: {e}")

    return payload


if __name__ == "__main__":
    collect_once()
