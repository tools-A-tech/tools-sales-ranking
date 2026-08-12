"""
収集後に data/rankings_latest.json を GitHub に自動 push する
.env に GITHUB_TOKEN と GITHUB_REPO が設定されている場合のみ動作
"""
import os
import subprocess
from pathlib import Path
from datetime import datetime, timezone, timedelta

ROOT = Path(__file__).resolve().parent.parent
JST = timezone(timedelta(hours=9))


def load_env():
    try:
        from dotenv import load_dotenv
        load_dotenv(ROOT / ".env")
    except Exception:
        pass


def push_to_github() -> bool:
    """
    rankings_latest.json を commit & push する
    成功したら True
    """
    load_env()
    token = os.getenv("GITHUB_TOKEN", "").strip()
    repo = os.getenv("GITHUB_REPO", "").strip()  # 例: username/cellrank

    if not token or not repo:
        print("[GitHub] GITHUB_TOKEN / GITHUB_REPO が未設定のためスキップ")
        return False

    if not (ROOT / ".git").exists():
        print("[GitHub] このフォルダは git リポジトリではありません。スキップ")
        print("         → GitHub のリポジトリを clone したフォルダで運用してください")
        return False

    try:
        # 変更があるか確認
        status = subprocess.run(
            ["git", "status", "--porcelain", "data/rankings_latest.json"],
            cwd=ROOT, capture_output=True, text=True, encoding="utf-8"
        )
        if not status.stdout.strip():
            print("[GitHub] 変更なし（pushスキップ）")
            return True

        # add
        subprocess.run(
            ["git", "add", "data/rankings_latest.json"],
            cwd=ROOT, check=True, capture_output=True
        )

        # commit
        msg = f"update rankings {datetime.now(JST).strftime('%Y-%m-%d %H:%M JST')}"
        subprocess.run(
            ["git", "commit", "-m", msg],
            cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8"
        )

        # remote URL を token 付きに一時設定して push
        # origin の URL を取得
        remote = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=ROOT, capture_output=True, text=True, encoding="utf-8"
        )
        original_url = remote.stdout.strip()

        # https://github.com/user/repo.git → https://token@github.com/user/repo.git
        if original_url.startswith("https://"):
            # 既に token が入っている場合もあるので一旦正規化
            if "@github.com" in original_url:
                push_url = original_url
            else:
                push_url = original_url.replace(
                    "https://", f"https://{token}@"
                )
        elif original_url.startswith("git@"):
            # SSH の場合はそのまま（鍵が設定されている前提）
            push_url = original_url
        else:
            push_url = f"https://{token}@github.com/{repo}.git"

        # push
        result = subprocess.run(
            ["git", "push", push_url, "HEAD"],
            cwd=ROOT, capture_output=True, text=True, encoding="utf-8"
        )

        if result.returncode == 0:
            print("[GitHub] push 成功 → サイトが更新されます")
            return True
        else:
            print(f"[GitHub] push 失敗: {result.stderr.strip() or result.stdout.strip()}")
            return False

    except subprocess.CalledProcessError as e:
        print(f"[GitHub] git コマンドエラー: {e}")
        return False
    except Exception as e:
        print(f"[GitHub] 予期しないエラー: {e}")
        return False


if __name__ == "__main__":
    push_to_github()
