# 📸 FOTEI: Hybrid Cloud Media Pipeline

このディレクトリは、カメラから取り込んだメディアを整理・最適化し、用途別にクラウドへ振り分けてAI解析する統合パイプラインです。

---

## 🏗 システム構成 (The Pipeline)

### Phase 1: [SORT] ローカル整理・分離
散らばったファイルを物理的に正しい場所へ移動し、ノイズを隔離します。
1. `01_sort_photos_by_month.ps1`: 写真を日付（月）ごとに振分
2. `02_sort_merge_legacy.ps1`: 旧形式（YYYYMM）のフォルダを統合
3. `03_sort_isolate_videos.ps1`: 動画ファイルを `VV/` フォルダへ隔離
4. `04_sort_isolate_screenshots.ps1`: PNG/スクショを抽出して `Screenshots_PNG/` へ隔離
5. `05_sort_verify_log.ps1`: ログに基づいた最終的な移動・照合

### Phase 2: [VOLUME] 容量の最適化
クラウドストレージの無料枠を最大限に活かす圧縮戦略。
6. `06_volume_resize_images.py`: 写真をターゲットサイズ（200KB等）へ一括圧縮

### Phase 3: [PHOTO CLOUD] 思い出のバックアップ (GPhotos)
7. `07_photo_cloud_list.py`: Google Photos上の既存ファイルをリスト化
8. `08_photo_cloud_sync.py`: 圧縮済み写真を Google Photos へ差分バックアップ

### Phase 4: [SCREENSHOT CLOUD] 情報の知能化 (Drive/AI)
スクショのみを「情報資産」として別ルートで管理。
9. `09_screenshot_drive_sync.py`: スクショのみを Google Drive/GCP へ同期
10. `10_semantic_ai_processor.py`: AI (VLM) によるタグ付け・自動フォルダ整理

---

## 🎯 運用ルール
- **写真は Google Photos**: 高速な閲覧と顔認識を優先。
- **スクショは Google Drive**: AIによる文書的・機能的なフォルダ整理を優先。
- **マスターはローカル**: 整理されたHDDをすべての起点とする。

---

## 🔧 セットアップ・環境分け
効率化のため、「PCパワーが必要な処理」と「クラウド連携・AI」で環境を分離しました。

### 1. ローカル環境 (Local Windows)
リサイズなど、PCのCPUをフル活用する物理的な整理に使用します。
- **venv作成済**: `FOTEI/venv_volume` (リサイズ用のPillow含む)
- **使用スクリプト**: `01`〜`06`
- **実行方法**: `.\venv_volume\Scripts\python FOTEI\06_volume_resize_images.py`

### 2. クラウド環境 (Google Colab)
API連携やAI解析に使用します。ローカルを汚さず、安全にAPIを叩けます。
- **Notebook**: `FOTEI/FOTEI_Cloud_Hub.ipynb` (作成済)
- **使用スクリプト**: `07`〜`10` (ロジックをColabへ移行)

---
*Created by Antigravity AI for Efficient Digital Life.*
