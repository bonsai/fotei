param (
    [ValidateSet("Log", "Move", "Other")]
    [string]$Mode = "Log"
)

$baseFolder = "J:\2022"
$logFile = Join-Path $baseFolder "move_plan_log.txt"

function Create-MoveLog {
    Write-Host "🔍 比較ログを作成中..."

    # 直下のファイル（サブフォルダ除く）
    $rootFiles = Get-ChildItem -Path $baseFolder -Filter *.jpg -File

    # 月別フォルダ（01～12）にあるファイル（再帰的）
    $monthFiles = Get-ChildItem -Path $baseFolder -Include *.jpg -File -Recurse |
        Where-Object { $_.DirectoryName -match '\\(0[1-9]|1[0-2])$' }

    # 月別ファイルを辞書に
    $monthFileMap = @{}
    foreach ($file in $monthFiles) {
        $monthFileMap[$file.Name] = $file.FullName
    }

    # ログファイル初期化
    if (Test-Path $logFile) { Remove-Item $logFile }

    # 比較してログ出力
    foreach ($file in $rootFiles) {
        if ($monthFileMap.ContainsKey($file.Name)) {
            $from = $file.FullName
            $to = $monthFileMap[$file.Name]
            $log = "MATCH: $($file.Name)`nFROM: $from`nTO:   $to`n"
            Add-Content -Path $logFile -Value $log
        }
    }

    Write-Host "✅ 比較ログを作成しました: $logFile"
}

function Execute-Move {
    if (-not (Test-Path $logFile)) {
        Write-Warning "ログファイルが見つかりません: $logFile"
        return
    }

    Write-Host "🚚 ログに基づいてファイルを移動中..."

    $lines = Get-Content $logFile -Encoding UTF8
    $from = $null
    $to = $null

    foreach ($line in $lines) {
        if ($line -match "^FROM:\s*(.+)$") {
            $from = $Matches[1].Trim()
        } elseif ($line -match "^TO:\s*(.+)$") {
            $to = $Matches[1].Trim()

            if ($from -and $to) {
                if (Test-Path $from) {
                    try {
                        Move-Item -Path $from -Destination $to -Force
                        Write-Host "✔️ Moved: $from → $to（上書きあり）"
                    } catch {
                        Write-Warning "❌ 移動失敗: $from → $to"
                    }
                } else {
                    Write-Warning "⚠️ スキップ: $from（存在しない）"
                }
                # 次のセットに備えて初期化
                $from = $null
                $to = $null
            } else {
                Write-Warning "⚠️ ログの形式に問題があります（FROM/TO 不完全）"
            }
        }
    }

    Write-Host "✅ 移動完了"
}

function Do-Other {
    Write-Host "🛠 その他の処理はまだ未実装です"
}

# 実行モードに応じて処理を分岐
switch ($Mode) {
    "Log"  { Create-MoveLog }
    "Move" { Execute-Move }
    "Other" { Do-Other }
}
