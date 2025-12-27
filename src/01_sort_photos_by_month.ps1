# 設定
$baseFolder = "J:\2021"
$imageExtensions = @(".jpg", ".jpeg", ".png", ".gif", ".bmp", ".heic", ".heif", ".tiff")

Write-Host "🚀 写真の仕分けを開始します (J:\2021 直下の画像のみ)..."

# 2022直下のファイルをスキャン
$files = Get-ChildItem -Path $baseFolder -File

foreach ($file in $files) {
    $ext = $file.Extension.ToLower()
    
    # 画像ファイルかチェック
    if ($imageExtensions -contains $ext) {
        # ファイルの更新日時から月(01-12)を取得
        $month = $file.LastWriteTime.Month.ToString("00")
        $targetSubFolder = Join-Path $baseFolder $month
        
        # 移動先フォルダ（01-12）がなければ作成
        if (-not (Test-Path $targetSubFolder)) {
            New-Item -Path $targetSubFolder -ItemType Directory | Out-Null
            Write-Host "📁 フォルダ作成: $month"
        }
        
        # 移動実行
        $destination = Join-Path $targetSubFolder $file.Name
        try {
            # 同名ファイルがある場合は上書きする (-Force を追加)
            Move-Item -Path $file.FullName -Destination $destination -Force -ErrorAction Stop
            Write-Host "📸 Moved (Overwritten): $($file.Name) -> $month フォルダ"
        }
        catch {
            Write-Warning "❌ 移動失敗: $($file.Name)"
        }
    }
}

Write-Host "✅ 写真の仕分けが完了しました"
