@echo off
chcp 65001 >nul
echo LINE スタンプ登録自動化ツール (デバッグモード) を起動します...
echo ※ 各ステップで一時停止します
echo.
python main.py --debug
pause
