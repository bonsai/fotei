# 設定
$baseFolder = "J:\2022" # 処理対象のフォルダ
$targetFolderName = "VV"
$targetPath = Join-Path $baseFolder $targetFolderName

# 対象の拡張子（両方のスクリプトから統合）
$videoExtensions = @(".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv", ".mts", ".m2ts", ".3gp", ".m4v")

Write-Host "🚀 動画ファイルの整理を開始します..."
Write-Host "📍 対象フォルダ: $baseFolder"

# VVフォルダがなければ作成
if (-not (Test-Path $targetPath)) {
    New-Item -Path $targetPath -ItemType Directory | Out-Null
    Write-Host "📁 移動先フォルダを作成しました: $targetFolderName"
}

# 全ての子フォルダから動画ファイルを検索 (VVフォルダ自体は除外)
Write-Host "🔍 動画ファイルを検索中..."
$files = Get-ChildItem -Path $baseFolder -File -Recurse | Where-Object {
    $_.FullName -notlike "*\$targetFolderName\*" -and $videoExtensions -contains $_.Extension.ToLower()
}

$count = $files.Count
Write-Host "🎬 見つかった動画ファイル数: $count"

if ($count -gt 0) {
    foreach ($file in $files) {
        $destination = Join-Path $targetPath $file.Name
        
        # 同名ファイルがある場合の処理（必要に応じて調整）
        try {
            Move-Item -Path $file.FullName -Destination $destination -Force -ErrorAction Stop
            Write-Host "✅ Moved: $($file.Name)"
        }
        catch {
            Write-Warning "❌ 移動失敗: $($file.FullName)"
        }
    }
    Write-Host "`n✨ すべての移動が完了しました。"
}
else {
    Write-Host "ℹ️ 移動対象の動画ファイルは見つかりませんでした。"
}
