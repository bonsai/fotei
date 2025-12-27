# FOTEI Development Log - 2025-12-28

## 1. プロジェクト概要 (Project Overview)
FOTEI (Hybrid Cloud Media Pipeline) の構築。カメラからPC、そしてクラウド（Google Photos / Drive）へメディアを最適化して流す自動化システム。

## 2. 達成したこと (Current Achievements)

### Phase 1 & 2: [SORT] & [VOLUME]
- **物理整理**: 写真（月別）、動画（VV/）、スクショ（隔離）の自動振分スクリプト群（01-05）をFOTEIフォルダに集約。
- **最適化**: `06_volume_resize_images.py` を実装し、15GB制限対策の圧縮フローを確立。
- **環境分離**: ローカルのリサイズ処理用に `venv_volume` 仮想環境を作成。

### Phase 3 & 4: [CLOUD] & [SEMANTICS]
- **Google Photos連携**: メタデータ取得(`07`)と差分アップロード(`08`)の実装。
- **Screenshot連携**: Google Driveへの同期スクリプト(`09`)を実装。
- **AI解析案**: VLMによるタグ付けと自動フォルダ振分のロジックを設計。
- **Colab Hub**: クラウド連携とAI解析をブラウザ上で実行するための `FOTEI_Cloud_Hub.ipynb` を作成。

### Management & DevOps
- **Git管理**: `bonsai/fotei` リポジトリを初期化。`.gitignore` で不要ファイルを整理。
- **AI Reviewer**: `.coderabbit.yaml` を導入し、FOTEI専用のレビュー基準（API安全管理、エラーハンドリング等）を定義。

## 3. 現在の状態 (Current State)
- **Branch**: `feature/colab-integration` (CodeRabbit設定とColabロジックの実装)
- **Local Env**: `FOTEI/venv_volume`
- **Cloud Env**: Google Colab用ノートブック準備完了

## 4. 次のステップ (Next Steps)
- `10_semantic_ai_processor.py` の具体実装（Gemini API連携）。
- Google Drive上のスクショに対するAI自動フォルダ分けの動作検証。
- PRによる CodeRabbit レビューの確認。

---
*Save point created for Drive relocation. Session safe to resume.*
