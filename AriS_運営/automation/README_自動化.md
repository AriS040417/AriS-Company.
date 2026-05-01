## YouTubeショート自動化（半自動→高自動化）

このフォルダは、素材投入からYouTube予約投稿までを自動化する実行基盤です。  
まずは半自動（動画生成 + 投稿情報生成）で運用し、次にYouTube API連携を有効化します。

## 1. 事前準備
- PowerShell
- （高自動化時）Google CloudでYouTube Data API v3を有効化

## 2. 初回セットアップ（PCごとに1回）
```powershell
powershell -ExecutionPolicy Bypass -File ".\automation\setup_tools.ps1"
```

## 3. インストール（高自動化時のみ）
```powershell
automation\tools\python\python.exe -m pip install -r automation/requirements.txt
```

## 4. 初期設定
1) `automation/config.example.json` を `automation/config.json` にコピー  
2) `config.json` の値を埋める
   - 出力先
   - チャンネル向けデフォルトタグ
   - YouTubeクレデンシャルパス（高自動化時）

## 5. 実行フロー
### 半自動（推奨スタート）
```powershell
.\automation\run_pipeline_portable.ps1 `
  --song "歩道橋の上で" `
  --input-video "C:\path\to\source.mp4" `
  --publish-at "2026-05-02T12:00:00+09:00"
```

生成物:
- `output/shorts/*.mp4`
- `output/youtube/*.json`（タイトル・説明文・タグ）

### 高自動化（YouTube予約投稿まで）
```powershell
.\automation\run_pipeline_portable.ps1 `
  --song "歩道橋の上で" `
  --input-video "C:\path\to\source.mp4" `
  --publish-at "2026-05-02T12:00:00+09:00" `
  --upload
```

## 6. 運用ポリシー（今回の方針を反映）
- 説明文は短く、1〜3行で十分
- 主役は動画本編（フック・テンポ・音の気持ちよさ）
- 制作アピール文（例: 「これ一晩で作った」）は使わない

## 7. 補足
- 初回 `--upload` 実行時にOAuthブラウザ認証が発生します
- API投稿が難しい媒体は、生成物を使った半自動運用で継続可能です
