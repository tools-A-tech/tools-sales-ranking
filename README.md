# ゲームセルラン TOP50

App Store / Google Play の **ゲームカテゴリ** 売上ランキング（セルラン）を1時間おきに取得し、GitHub Pages に自動反映するサイトです。

## あなたがやること

### 1. GitHub リポジトリを用意する

1. 新しいリポジトリを作成（例: `cellrank`）
2. このフォルダの中身をすべてアップロード
3. Settings → Pages → Source を `main` / `(root)` に設定
4. 公開URL: `https://あなたのユーザー名.github.io/リポジトリ名/`

### 2. メインPCで運用する（推奨：git clone する）

```bash
git clone https://github.com/あなたのユーザー名/リポジトリ名.git
cd リポジトリ名
```

または既にダウンロードしたフォルダを使う場合は、そのフォルダで:

```bash
git init
git remote add origin https://github.com/あなたのユーザー名/リポジトリ名.git
git pull origin main
```

### 3. GitHub 自動反映を有効にする（推奨）

1. GitHub で Personal Access Token を発行  
   （Settings → Developer settings → Personal access tokens → Fine-grained or classic）  
   **repo** 権限を付けてください
2. プロジェクト直下に `.env` ファイルを作成（`.env.example` をコピー）

```
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
GITHUB_REPO=あなたのユーザー名/リポジトリ名
```

### 4. 起動

`start.bat` をダブルクリックするだけ

- 起動直後に1回収集
- 以降 **1時間おき** に収集
- `.env` が設定されていれば、収集後に自動で GitHub に push → サイト更新

ローカル確認: http://127.0.0.1:8000

---

## ファイル構成

```
cellrank-site/
├── index.html                 ← GitHub Pages 表示ページ
├── start.bat                  ← これを実行するだけ
├── .env.example               ← これを .env にコピーして設定
├── data/rankings_latest.json  ← 最新データ（自動更新・自動push）
├── collector/
│   ├── ios.py
│   ├── android.py
│   ├── main.py
│   └── github_push.py         ← 自動push処理
└── api/main.py                ← FastAPI + 1時間スケジューラ
```

## 表示内容

- iOS / Android タブ切り替え
- 1位〜50位
- アプリアイコン + ゲームタイトル + 開発者名
- ストアへのリンク

## 注意

- 非公式集計です。スクレイピングは自己責任でお願いします。
- Apple / Google の仕様変更で一時的に取得できなくなることがあります。
- Token は絶対に公開リポジトリにコミットしないでください（`.gitignore` に `.env` を入れています）
