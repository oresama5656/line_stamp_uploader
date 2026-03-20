"""
main.py - LINE Creators Market スタンプ登録自動化ツール

使い方:
  1. stamps_data.csv にスタンプ情報を記入
  2. python main.py を実行
  3. ブラウザが開くので、LINEにログインする
  4. スタンプの新規登録画面まで移動する
  5. コンソールで Enter を押す → 自動入力開始

デバッグモード:
  python main.py --debug
  → 各ステップで一時停止し、確認しながら進められる
"""

import csv
import sys
import os
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

# --- セレクタ・設定の読み込み ---
from config import (
    TITLE_EN_SELECTOR, DESC_EN_SELECTOR,
    ADD_LANGUAGE_SELECTOR, ADD_LANGUAGE_BUTTON, LANGUAGE_JAPANESE_VALUE,
    TITLE_JA_SELECTOR, DESC_JA_SELECTOR,
    COPYRIGHT_SELECTOR,
    AI_GENERATED_SELECTOR,
    TASTE_CATEGORY_SELECTOR, CHARACTER_CATEGORY_SELECTOR,
    SAVE_BUTTON_SELECTOR,
    DEFAULT_COPYRIGHT, DEFAULT_AI_FLAG,
    VALID_TASTE_CATEGORIES, VALID_CHARACTER_CATEGORIES,
)


# ============================================================
# 1. データ読み込み（Python標準のcsvモジュールのみ使用）
# ============================================================
def load_stamps_data(csv_path: str) -> tuple[list[dict], list[str]]:
    """CSVファイルからスタンプ情報を読み込む。done=1の行はスキップする。"""
    if not os.path.exists(csv_path):
        print(f"エラー: CSVファイルが見つかりません: {csv_path}")
        sys.exit(1)

    with open(csv_path, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        all_data = [row for row in reader]

    if not all_data:
        print("エラー: CSVにデータが1件もありません。")
        sys.exit(1)

    # done列がなければ全行に空値を追加
    if "done" not in fieldnames:
        fieldnames = list(fieldnames) + ["done"]
        for row in all_data:
            row["done"] = ""

    # done=1 の行をスキップ
    todo = [row for row in all_data if row.get("done", "").strip() != "1"]
    done_count = len(all_data) - len(todo)

    print(f"✅ 全 {len(all_data)} 件中、{done_count} 件は処理済み。残り {len(todo)} 件を処理します。")

    if not todo:
        print("すべてのスタンプが処理済みです。CSVのdone列をクリアして再実行してください。")
        sys.exit(0)

    return todo, fieldnames


def validate_categories(stamps: list[dict]) -> tuple[list[dict], list[dict]]:
    """カテゴリの値をチェックし、有効な行と無効な行を分離する"""
    valid = []
    invalid = []

    for stamp in stamps:
        errors = []
        taste = stamp.get("taste_category", "").strip()
        character = stamp.get("character_category", "").strip()

        if taste and taste not in VALID_TASTE_CATEGORIES:
            errors.append(f"taste_category='{taste}'")
        if character and character not in VALID_CHARACTER_CATEGORIES:
            errors.append(f"character_category='{character}'")

        if errors:
            invalid.append((stamp, errors))
        else:
            valid.append(stamp)

    return valid, invalid


def mark_done(csv_path: str, fieldnames: list[str], stamp: dict):
    """処理が完了した行のdone列を1に更新してCSVを上書き保存する"""
    import time

    with open(csv_path, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        all_data = [row for row in reader]

    # 同じNo の行を探して done=1 にする
    for row in all_data:
        if row.get("No", "") == stamp.get("No", ""):
            row["done"] = "1"
            break

    # CSVがエクセル等で開かれている場合のリトライ
    for attempt in range(3):
        try:
            with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(all_data)
            return  # 書き込み成功
        except PermissionError:
            if attempt < 2:
                print(f"  ⚠️ CSVが他のアプリで開かれています。閉じてください...（リトライ {attempt+1}/3）")
                time.sleep(3)
            else:
                print(f"  ⚠️ CSV書き込み失敗（ファイルが開かれています）。")
                print(f"     → LINEへの保存は成功しています。")
                print(f"     → No.{stamp.get('No', '?')} のdone列は手動で1にしてください。")


# ============================================================
# 2. メタデータ入力（1件分のフォーム操作）
# ============================================================
def fill_stamp_form(page, stamp: dict, debug: bool = False):
    """
    1件分のスタンプ情報をフォームに入力する。
    memo.md の手順 1〜10 に対応。
    """

    # --- 手順1: 英語タイトルを入力 ---
    print("  [1/10] 英語タイトルを入力中...")
    page.fill(TITLE_EN_SELECTOR, stamp["title_en"])

    # --- 手順2: 英語説明文を入力 ---
    print("  [2/10] 英語説明文を入力中...")
    page.fill(DESC_EN_SELECTOR, stamp["desc_en"])

    # --- 手順3: 言語を追加 → Japanese を選択 → 追加ボタンを押す ---
    print("  [3/10] 言語を追加リストから Japanese を選択中...")
    page.select_option(ADD_LANGUAGE_SELECTOR, LANGUAGE_JAPANESE_VALUE)
    print("  [3/10] 追加ボタンをクリック中...")
    page.click(ADD_LANGUAGE_BUTTON)
    # 日本語入力欄の出現を待つ
    page.wait_for_selector(TITLE_JA_SELECTOR, state="visible")

    if debug:
        input("  [DEBUG] 日本語入力欄が表示されたか確認してください。Enter で続行...")

    # --- 手順4: 日本語タイトルを入力 ---
    print("  [4/10] 日本語タイトルを入力中...")
    page.fill(TITLE_JA_SELECTOR, stamp["title_ja"])

    # --- 手順5: 日本語説明文を入力 ---
    print("  [5/10] 日本語説明文を入力中...")
    page.fill(DESC_JA_SELECTOR, stamp["desc_ja"])

    # --- 手順6: コピーライトを入力 ---
    copyright_text = stamp.get("copy_right", "") or DEFAULT_COPYRIGHT
    print(f"  [6/10] コピーライトを入力中... ({copyright_text})")
    page.fill(COPYRIGHT_SELECTOR, copyright_text)

    # --- 手順7: AI使用フラグを選択 ---
    ai_flag = stamp.get("ai_flag", "") or DEFAULT_AI_FLAG
    print(f"  [7/10] AI使用を選択中... (AI生成={ai_flag})")
    page.click(AI_GENERATED_SELECTOR)

    # --- 手順8: テイストカテゴリをリストから選択 ---
    taste = stamp.get("taste_category", "")
    if taste:
        print(f"  [8/10] テイストカテゴリを選択中... ({taste})")
        page.select_option(TASTE_CATEGORY_SELECTOR, label=taste)
    else:
        print("  [8/10] テイストカテゴリ: スキップ（未指定）")

    # --- 手順9: キャラクターカテゴリをリストから選択 ---
    character = stamp.get("character_category", "")
    if character:
        print(f"  [9/10] キャラクターカテゴリを選択中... ({character})")
        page.select_option(CHARACTER_CATEGORY_SELECTOR, label=character)
    else:
        print("  [9/10] キャラクターカテゴリ: スキップ（未指定）")

    # [将来の拡張用：ZIP登録処理]
    # zip_path = stamp.get("zip_path", "")
    # if zip_path:
    #     upload_sticker_images(page, zip_path)

    if debug:
        input("  [DEBUG] 保存ボタンを押す前の最終確認。Enter で保存を実行...")

    # --- 手順10: 保存ボタンをクリック ---
    print("  [10/10] 保存ボタンをクリック中...")
    page.click(SAVE_BUTTON_SELECTOR)

    # ページ遷移を待機
    page.wait_for_load_state("networkidle")
    print("  ✅ 保存完了！")


# ============================================================
# 3. メイン処理
# ============================================================
def main():
    debug = "--debug" in sys.argv
    
    # コマンドライン引数からCSVパスを取得（引数があればそれを使用、なければデフォルト）
    if len(sys.argv) > 1 and not sys.argv[1].startswith("--"):
        csv_path = sys.argv[1]
    else:
        csv_path = os.path.join(os.path.dirname(__file__), "stamps_data.csv")

    if not os.path.isabs(csv_path):
        csv_path = os.path.abspath(csv_path)

    print(f"DEBUG: 使用するCSV = {csv_path}")

    # データ読み込み（done=1 の行は自動スキップ）
    stamps, fieldnames = load_stamps_data(csv_path)

    # カテゴリの事前チェック
    stamps, invalid = validate_categories(stamps)

    if invalid:
        print(f"\n⚠️  カテゴリが不正な {len(invalid)} 件をスキップします：")
        for stamp, errors in invalid:
            no = stamp.get("No", "?")
            theme = stamp.get("theme", "不明")
            print(f"   No.{no} [{theme}] → {', '.join(errors)}")
        print("   → CSVのカテゴリを修正して再実行すれば処理されます。")

    if not stamps:
        print("\n処理対象のスタンプがありません。CSVを確認してください。")
        sys.exit(0)

    print("\n" + "=" * 50)
    print("LINE Creators Market スタンプ登録自動化ツール")
    print("=" * 50)

    with sync_playwright() as p:
        # ブラウザ起動 (常にGUI表示 & ゆっくり動作)
        browser = p.chromium.launch(
            headless=False,
            slow_mo=200,  # 各操作の間に1秒待機（目視確認用）
        )
        page = browser.new_page()

        # LINE Creators Market を開く
        page.goto("https://creator.line.me")

        print("\n" + "-" * 50)
        print("ブラウザが開きました。")
        print("以下の手順で進めてください：")
        print("  1. LINEアカウントでログインする")
        print("  2. スタンプの新規登録画面まで移動する")
        print("-" * 50)
        input("\n準備ができたら Enter を押してください...")

        completed = 0

        # --- 登録ループ ---
        for i, stamp in enumerate(stamps):
            theme = stamp.get("theme", f"No.{i+1}")
            print(f"\n{'=' * 50}")
            print(f"📝 [{i+1}/{len(stamps)}] {theme}")
            print(f"{'=' * 50}")

            if i > 0:
                # 2件目以降：ユーザーに新規登録画面を開いてもらう
                print("\n  次のスタンプの新規登録画面を開いてください。")
                input("  準備ができたら Enter を押してください...")

            try:
                fill_stamp_form(page, stamp, debug=debug)

                # 保存成功 → CSVのdone列を1に更新
                mark_done(csv_path, fieldnames, stamp)
                completed += 1
                print(f"  📄 CSVのdone列を更新しました（No.{stamp.get('No', '?')}）")

            except PlaywrightTimeout as e:
                print(f"\n❌ エラー: 要素が見つかりませんでした。")
                print(f"   詳細: {e}")
                print(f"   → config.py のセレクタを確認してください。")

                # エラー時のスクリーンショット保存
                screenshot_path = os.path.join(
                    os.path.dirname(__file__), f"error_{i+1}.png"
                )
                page.screenshot(path=screenshot_path)
                print(f"   → スクリーンショットを保存しました: {screenshot_path}")

                # 即停止（ここまでの完了分はCSVに保存済み）
                print(f"   → {completed} 件完了済み。プログラムを停止します。")
                print(f"   → 再実行すれば、未完了分から再開します。")
                browser.close()
                sys.exit(1)
            except Exception as e:
                print(f"\n❌ 予期せぬエラー: {e}")
                screenshot_path = os.path.join(
                    os.path.dirname(__file__), f"error_{i+1}.png"
                )
                page.screenshot(path=screenshot_path)
                print(f"   → スクリーンショットを保存しました: {screenshot_path}")
                print(f"   → {completed} 件完了済み。再実行で未完了分から再開します。")
                browser.close()
                sys.exit(1)

        # --- 全件完了 ---
        print("\n" + "=" * 50)
        print(f"🎉 全 {completed} 件の登録が完了しました！")
        print("=" * 50)
        input("\nブラウザを閉じるには Enter を押してください...")
        browser.close()


if __name__ == "__main__":
    main()
