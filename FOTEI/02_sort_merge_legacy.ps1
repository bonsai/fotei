# 設定
$baseFolder = "j:\2021"

Write-Host "🚀 フォルダの統合を開始します (2021MM -> MM)..."

for ($i = 1; $i -le 12; $i++) {
    $month = $i.ToString("00")
    $sourceName = "2021$month"
    $targetName = $month
    
    $sourcePath = Join-Path $baseFolder $sourceName
    $targetPath = Join-Path $baseFolder $targetName
    
    if (Test-Path $sourcePath) {
        Write-Host "📂 統合中: $sourceName -> $targetName"
        
        # ターゲットフォルダがない場合は作成
        if (-not (Test-Path $targetPath)) {
            New-Item -Path $targetPath -ItemType Directory | Out-Null
            Write-Host "📁 フォルダ作成: $targetName"
        }
        
        # ソースフォルダ内のファイルを移動
        $items = Get-ChildItem -Path $sourcePath
        foreach ($item in $items) {
            $destItemPath = Join-Path $targetPath $item.Name
            
            # 同名ファイルがある場合は上書き (-Force)
            try {
                Move-Item -Path $item.FullName -Destination $destItemPath -Force -ErrorAction Stop
            }
            catch {
                Write-Warning "❌ 移動失敗: $($item.FullName)"
            }
        }
        
        # 空になったソースフォルダを削除
        if ((Get-ChildItem -Path $sourcePath).Count -eq 0) {
            Remove-Item -Path $sourcePath -Force
            Write-Host "🗑️ 削除完了: $sourceName"
        }
        else {
            Write-Warning "⚠️ フォルダ $sourceName が空ではないため削除をスキップしました。"
        }
    }
}

Write-Host "✅ フォルダの統合が完了しました"
