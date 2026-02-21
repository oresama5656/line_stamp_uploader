@echo off
chcp 65001 >nul
echo ========================================
echo  LINE スタンプ登録自動化ツール セットアップ
echo ========================================
echo.

echo [1/2] 必要なライブラリをインストール中...
pip install playwright
if errorlevel 1 (
    echo エラー: pip install に失敗しました。Pythonがインストールされているか確認してください。
    pause
    exit /b 1
)

echo.
echo [2/2] Chromiumブラウザをインストール中...
playwright install chromium
if errorlevel 1 (
    echo エラー: Chromiumのインストールに失敗しました。
    pause
    exit /b 1
)

echo.
echo ========================================
echo  セットアップ完了！
echo  以下のコマンドで実行できます:
echo    python main.py
echo  デバッグモード:
echo    python main.py --debug
echo ========================================
pause
