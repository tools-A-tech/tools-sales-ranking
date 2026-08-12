"""
iOS App Store ゲームカテゴリ トップセールス（セルラン）取得
genre=6014 = Games
"""
import requests
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any


JST = timezone(timedelta(hours=9))


def fetch_ios_game_top50(limit: int = 50) -> List[Dict[str, Any]]:
    """
    Apple RSS (旧形式) で日本のゲーム トップセールスを取得
    """
    url = f"https://itunes.apple.com/jp/rss/topgrossingapplications/limit={limit}/genre=6014/json"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    }

    try:
        resp = requests.get(url, headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"[iOS] 取得失敗: {e}")
        return []

    entries = data.get("feed", {}).get("entry", [])
    if not isinstance(entries, list):
        entries = [entries] if entries else []

    results = []
    for idx, entry in enumerate(entries[:limit], start=1):
        try:
            name = entry.get("im:name", {}).get("label", "不明")
            app_id = entry.get("id", {}).get("attributes", {}).get("im:id", "")
            bundle_id = entry.get("id", {}).get("attributes", {}).get("im:bundleId", "")
            artist = entry.get("im:artist", {}).get("label", "")
            # アイコンは複数サイズがあるので一番大きいものを優先
            images = entry.get("im:image", [])
            icon_url = ""
            if images:
                # height属性が大きいものを選ぶ
                sorted_imgs = sorted(
                    images,
                    key=lambda x: int(x.get("attributes", {}).get("height", 0)),
                    reverse=True
                )
                icon_url = sorted_imgs[0].get("label", "")

            results.append({
                "rank": idx,
                "title": name,
                "app_id": app_id,
                "bundle_id": bundle_id,
                "developer": artist,
                "icon": icon_url,
                "platform": "ios",
                "store_url": f"https://apps.apple.com/jp/app/id{app_id}" if app_id else ""
            })
        except Exception as e:
            print(f"[iOS] エントリ解析エラー rank={idx}: {e}")
            continue

    return results


if __name__ == "__main__":
    apps = fetch_ios_game_top50()
    print(f"取得数: {len(apps)}")
    for a in apps[:5]:
        print(f"{a['rank']:2d}. {a['title']} | {a['icon'][:60]}...")
