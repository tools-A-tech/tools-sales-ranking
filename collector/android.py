"""
Google Play ゲームカテゴリ トップセールス寄りランキング取得

Play Store のゲームカテゴリページから appId を順序付きで抽出し、
詳細情報（タイトル・アイコン）を取得します。
"""
import re
import time
import requests
from typing import List, Dict, Any
from collections import OrderedDict
from datetime import timezone, timedelta

JST = timezone(timedelta(hours=9))


def fetch_android_game_top50(limit: int = 50) -> List[Dict[str, Any]]:
    url = "https://play.google.com/store/apps/category/GAME?hl=ja&gl=jp"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Accept-Language": "ja-JP,ja;q=0.9",
    }

    try:
        resp = requests.get(url, headers=headers, timeout=30)
        resp.raise_for_status()
        html = resp.text
    except Exception as e:
        print(f"[Android] ページ取得失敗: {e}")
        return []

    app_ids = re.findall(r'/store/apps/details\?id=([a-zA-Z0-9\._]+)', html)
    unique_ids = list(OrderedDict.fromkeys(app_ids))[:limit]

    results = []
    try:
        from google_play_scraper import app as gplay_app
        has_detail = True
    except Exception:
        has_detail = False
        print("[Android] google-play-scraper の app() が使えません")

    for idx, app_id in enumerate(unique_ids, start=1):
        title = app_id
        icon = ""
        developer = ""
        if has_detail:
            try:
                detail = gplay_app(app_id, lang="ja", country="jp")
                title = detail.get("title", app_id)
                icon = detail.get("icon", "")
                developer = detail.get("developer", "")
                time.sleep(0.15)  # 優しめ
            except Exception as e:
                print(f"[Android] detail失敗 {app_id}: {e}")

        results.append({
            "rank": idx,
            "title": title,
            "app_id": app_id,
            "bundle_id": app_id,
            "developer": developer,
            "icon": icon,
            "platform": "android",
            "store_url": f"https://play.google.com/store/apps/details?id={app_id}&hl=ja&gl=jp"
        })

    print(f"[Android] {len(results)}件取得")
    return results


if __name__ == "__main__":
    apps = fetch_android_game_top50(3)
    print(f"取得数: {len(apps)}")
    for a in apps:
        print(f"{a['rank']:2d}. {a['title'][:40]}")
