# Repository Guidelines

## プロジェクト構成とモジュール整理
GPT-4o Transcribe Diariz を使った「ぎじろくさくせい」ウェブアプリです。FastAPI バックエンドは `app/`（`main.py`、`routers/`, `services/transcribe.py`）、React + Vite フロントは `frontend/` に配置します。共通スキーマは `app/schemas/`、環境変数やモデル設定は `configs/`（例: `openai.yaml`, `prompts/diariz-summary.ja.md`）で管理します。デモ用音声は `samples/`、テストフィクスチャは `tests/fixtures/` に保存し、大容量の生音声はコミット禁止です。フロントで配布する画像やフォントは `frontend/public/` にまとめ、README でライセンス出典を記録してください。自動化スクリプトやセットアップ手順は `scripts/` に置き、リポジトリ直下の `README.md` から参照できるようにしてください。

## ビルド・テスト・開発コマンド
必須バージョンは Python 3.11 と Node.js 20 です。バックエンドは `python -m venv .venv && source .venv/bin/activate` → `python -m pip install -r requirements.txt` → `uvicorn app.main:app --reload` で起動します。フロントエンドは `cd frontend && npm install && npm run dev` を実行し、http://localhost:5173 を確認します。サンプル音声を使った動作確認は `python scripts/demo_pipeline.py --input samples/standup.m4a --lang ja`、フォーマットと静的解析は `ruff check app tests` と `npm run lint` で行います。ユニットテストは `pytest` と `npm test`、統合テストは `pytest tests/app -m integration` を利用してください。

## コーディング規約と命名
Python コードは PEP 8（4 スペースインデント）に従い、関数・モジュールは `snake_case`、クラスと React コンポーネントは `PascalCase`、定数は `SCREAMING_SNAKE_CASE` を使用します。React フックは `use` で始め、CSS モジュールはケバブケース（例: `meeting-timeline.module.css`）に統一します。プロンプトファイルはケバブケース、日本語版は `.ja.md` 拡張子で区別してください。公開関数や API には docstring / JSDoc でダイアリゼーション前提（最大話者数、タイムスタンプ形式）を明記し、保存前に `ruff`, `mypy`, `npm run lint` を必ず通します。

## テスト指針
バックエンドのテストは `tests/app/...` に、フロントエンドは `frontend/src/__tests__/` に配置し、ディレクトリ構造を本体とミラーリングします。GPT-4o のレスポンスは `tests/fixtures/diariz/` にある JSON をモックとして再利用し、話者統合ロジック（時間閾値、話者タグ変更）を Pytest で検証してください。カバレッジは `pytest --cov=app --cov-report=term-missing` で 80% 以上を維持します。Vitest + Testing Library でセグメントタイムラインや検索フィルタの動作を検証し、視覚差分ではなく挙動ベースのアサーションを優先します。CI 上の長時間テストは `@pytest.mark.slow` や `vitest --runInBand` で明示し、レビュー時に実行判断ができるようコメントを添えてください。

## コミットとプルリクエスト
コミットは Conventional Commits（例: `feat: add diarized timeline view`）を徹底し、バックエンドとフロントの変更は可能な限り別コミットに分けます。PR には概要（日本語可）、UI のスクリーンショットまたは GIF、サンプル出力、実行コマンドログ、関連タスクの参照（`Refs TASK-123`）を添付してください。CI（lint・pytest・Vitest）が通過した後でレビューを依頼し、最低 1 名のメンテナ承認を得てからマージします。

## セキュリティと設定
GPT-4o API キーは `.env.local`（バックエンドのみ読み取り）に保存し、クライアントへは露出させません。キーは月次でローテーションし、更新履歴を `configs/SECURITY.md` に追記してください。アップロード音声は 120 分・200 MB 以下に制限し、想定外コーデックはバリデーション層で即時拒否します。ログや添付資料に含まれる個人情報はマスクし、公開 Issue や PR コメントへ貼り付けないこと。また、共有リンクには有効期限を設定し、Slack やメールには直接ファイルを添付しないでください。モデル設定や料金影響がある変更は PR 説明に明記し、運用チームへ事前共有してください。
