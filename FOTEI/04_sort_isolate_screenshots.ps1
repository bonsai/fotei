# 設定
$baseFolder = "J:\2022" # 処理対象のフォルダ
$targetFolderName = "Screenshots_PNG"
$targetPath = Join-Path $baseFolder $targetFolderName

# 検索条件（PNG拡張子、またはファイル名に Screenshot / スクリーンショット を含む）
$keywordPatterns = @("*Screenshot*", "*スクリーンショット*")

Write-Host "🚀 PNGおよびスクリーンショットの抽出を開始します..."
Write-Host "📍 対象フォルダ: $baseFolder"

# フォルダがなければ作成
if (-not (Test-Path $targetPath)) {
    New-Item -Path $targetPath -ItemType Directory | Out-Null
    Write-Host "📁 移動先フォルダを作成しました: $targetFolderName"
}

# 全ての子フォルダを検索 (移動先フォルダ自体は除外)
Write-Host "🔍 ファイルを検索中..."
$files = Get-ChildItem -Path $baseFolder -File -Recurse | Where-Object {
    $_.FullName -notlike "*\$targetFolderName\*" -and (
        $_.Extension.ToLower() -eq ".png" -or 
        $_.Name -like "*Screenshot*" -or 
        $_.Name -like "*スクリーンショット*"
    )
}

$count = $files.Count
Write-Host "📸 見つかった対象ファイル数: $count"

if ($count -gt 0) {
    foreach ($file in $files) {
        $destination = Join-Path $targetPath $file.Name
        
        # 同名ファイルがある場合は上書き
        try {
            Move-Item -Path $file.FullName -Destination $destination -Force -ErrorAction Stop
            Write-Host "✅ Moved: $($file.Name)"
        }
        catch {
            Write-Warning "❌ 移動失敗: $($file.FullName)"
        }
    }
    Write-Host "`n✨ すべての抽出が完了しました。"
}
else {
    Write-Host "ℹ️ 対象ファイルは見つかりませんでした。"
}
