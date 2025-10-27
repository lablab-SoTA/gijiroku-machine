# ぎじろくさくせい

GPT-4o Transcribe Diariz を利用して会議音声から議事録を生成するサンプルアプリケーションです。FastAPI バックエンドと React + Vite フロントエンドで構成されています。

## セットアップ

### 1. リポジトリのクローンと環境変数

```bash
cp .env.example .env.local
```

`.env.local` の `APP_OPENAI_API_KEY` に有効な OpenAI API キーを設定してください。

### 2. Python バックエンド

```bash
python -m venv .venv
source .venv/bin/activate  # Windows は .venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 3. フロントエンド

```bash
cd frontend
npm install
npm run dev
```

ブラウザで `http://localhost:5173` を開いてアップロードフォームを確認します。

## 動作確認

バックエンドが起動している状態で、サンプル音声を用意して以下を実行します。

```bash
python scripts/demo_pipeline.py --input samples/standup.m4a --lang ja
```

成功すると JSON 形式の議事録が出力されます。

## テスト

- バックエンド: `pytest`
- フロントエンド: `cd frontend && npm test`

より詳細な運用ルールは `AGENTS.md` を参照してください。

## 仮デプロイ（Render を利用する例）

1. Render アカウントを作成し、GitHub 連携を有効化します。
2. このリポジトリを GitHub にプッシュし、Render の「New +」→「Web Service」からリポジトリを選択します。
3. Build Command に下記が自動で設定されます（`render.yaml` に準拠）:
   ```
   pip install --upgrade pip
   pip install -r requirements.txt
   npm install --prefix frontend
   npm run build --prefix frontend
   ```
   Start Command は `uvicorn app.main:app --host 0.0.0.0 --port $PORT`。
4. 環境変数に `APP_OPENAI_API_KEY`（OpenAI APIキー）を追加します。
5. デプロイ後、Render の URL へアクセスするとフロントエンドが表示され、`/transcriptions/` エンドポイントが同一ホストで利用できます。
