# ゲームセルラン TOP50

App Store / Google Play の **ゲームカテゴリ** 売上ランキング（セルラン）を1時間おきに取得し、表示する簡易サイトです。

## あなたがやること（最小手順）

### 1. GitHub にページを公開する

1. 新しいリポジトリを作成（例: `cellrank`）
2. このフォルダの中身をすべてアップロード
   - 特に重要なもの: `index.html` と `data/` フォルダ
3. Settings → Pages → Source を `Deploy from a branch` → `main` / `/ (root)` に設定
4. 数分待つと `https://あなたのユーザー名.github.io/リポジトリ名/` で公開されます

> データが更新されるたびに `data/rankings_latest.json` を手動で上書きアップロードするか、  
> 後述の自動pushを設定すると自動更新されます。

### 2. メインPCで収集を開始する

1. このフォルダをメインPCにコピー
2. `start.bat` をダブルクリック
3. 初回は依存パッケージのインストールが走ります
4. 起動後、自動で1回収集し、以降 **1時間おき** に収集します
5. ブラウザで http://127.0.0.1:8000 を開くとローカルで確認できます

これだけで動作します。

---

## ファイル構成

```
cellrank-site/
├── index.html              ← GitHub Pages 用表示ページ
├── start.bat               ← これを実行するだけ
├── requirements.txt
├── data/
│   └── rankings_latest.json  ← 最新のTOP50データ（自動更新）
├── collector/
│   ├── ios.py              ← App Store (genre=6014 Games)
│   ├── android.py          ← Google Play GAME TOP_GROSSING
│   └── main.py
└── api/
    └── main.py             ← FastAPI + スケジューラ
```

## 表示内容

- iOS / Android 切り替えタブ
- 1位〜50位
- アプリアイコン + ゲームタイトル + 開発者名
- ストアへのリンク

## デザインについて

`index.html` の `<style>` 部分を自由に修正してください。  
気になる箇所があれば指示をいただければ調整します。

## 自動でGitHubに反映させたい場合（任意）

1. GitHub Personal Access Token（repo権限）を発行
2. プロジェクト直下に `.env` を作成:
   ```
   GITHUB_TOKEN=ghp_xxxxxxxxxxxx
   GITHUB_REPO=あなたのユーザー名/リポジトリ名
   ```
3. 必要であれば push 用スクリプトを追加可能です（現状は手動アップロードでも問題ありません）

## 注意

- 非公式の集計です。スクレイピングは自己責任でお願いします。
- Apple / Google の仕様変更で一時的に取得できなくなることがあります。
- 商用利用や大量アクセスは避けてください。
