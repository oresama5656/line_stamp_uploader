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
import zipfile
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

# --- セレクタ・設定の読み込み ---
from config import (
    TITLE_EN_SELECTOR, DESC_EN_SELECTOR,
    ADD_LANGUAGE_SELECTOR, ADD_LANGUAGE_BUTTON, LANGUAGE_JAPANESE_VALUE,
    TITLE_JA_SELECTOR, DESC_JA_SELECTOR,
    COPYRIGHT_SELECTOR,
    AI_GENERATED_SELECTOR,
    TASTE_CATEGORY_SELECTOR, CHARACTER_CATEGORY_SELECTOR,
    SAVE_BUTTON_SELECTOR, SAVE_CONFIRM_MODAL_OK_SELECTOR,
    STAMP_IMAGES_TAB_SELECTOR, EDIT_IMAGES_BUTTON_SELECTOR, STAMP_COUNT_SELECT_SELECTOR,
    CONFIRM_COUNT_MODAL_OK_SELECTOR,
    ZIP_UPLOAD_BUTTON_SELECTOR, ZIP_FILE_INPUT_SELECTOR,
    BACK_TO_MANAGE_BUTTON_SELECTOR, REQUEST_APPROVAL_BUTTON_SELECTOR,
    CONSENT_CHECKBOX_SELECTOR, FINAL_SUBMIT_BUTTON_SELECTOR,
    NEW_REG_SIDEBAR_SELECTOR, NEW_STAMP_BTN_SELECTOR,
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
    
    # id列の確認（ZIPアップロードに必須）
    if todo and "id" not in fieldnames:
        print("警告: CSVに 'id' 列がありません。ZIPアップロードをスキップします。")
    
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
# 1.5 画面遷移（自動化用）
# ============================================================
def navigate_to_new_stamp_form(page):
    """
    左側メニューの「新規登録」→「スタンプ」をクリックして、
    スタンプ編集画面へ移動する。
    """
    print("\n🚀 [自動遷移] スタンプ新規登録画面へ移動します...")
    
    try:
        # 左側フレームの「新規登録」をクリック
        print("  ▶️ 左メニューの「新規登録」をクリック中...")
        page.wait_for_selector(NEW_REG_SIDEBAR_SELECTOR, state="visible", timeout=10000)
        page.click(NEW_REG_SIDEBAR_SELECTOR)
        
        # 画面が切り替わるのを少し待つ
        page.wait_for_load_state("networkidle")
        
        # 右側フレームの「スタンプ」ボタンをクリック
        print("  ▶️ 右メイン画面の「スタンプ」ボタンをクリック中...")
        page.wait_for_selector(NEW_STAMP_BTN_SELECTOR, state="visible", timeout=10000)
        page.click(NEW_STAMP_BTN_SELECTOR)
        
        # 編集フォーム（英語タイトル入力欄）が出るまで待機
        page.wait_for_selector(TITLE_EN_SELECTOR, state="visible", timeout=15000)
        print("  ✅ 準備完了！")
        return True
        
    except Exception as e:
        print(f"  ❌ 遷移中にエラーが発生しました: {e}")
        print("  💡 手動でスタンプ登録画面を開いてください。")
        input("  [準備ができたら Enter を押してください] ")
        return False



# ============================================================
# 2. メタデータ入力（1件分のフォーム操作）
# ============================================================
def fill_stamp_form(page, stamp: dict, debug: bool = False):
    """
    1件分のスタンプ情報をフォームに入力する。
    memo.md の手順 1〜10 に対応。
    """
    # ダイアログハンドラの設定 (保存時の最終確認など)
    def handle_initial_dialog(dialog):
        print(f"  💬 ダイアログ出現: {dialog.message}")
        dialog.accept()
        print("  ✅ ダイアログを承認しました。")

    page.on("dialog", handle_initial_dialog)

    # --- ZIPパスの解決 ---
    # ZIPファイルが格納されているフォルダを指定
    ZIP_DIR_BASE = "d:\\StampHub\\assets\\export\\ready"
    
    id_val = stamp.get("id", "").strip()
    zip_path = ""
    if id_val:
        candidate = os.path.join(ZIP_DIR_BASE, f"{id_val}.zip")
        if os.path.exists(candidate):
            zip_path = candidate
            # print(f"  📦 連携: ZIPファイルを発見しました: {zip_path}") 
        else:
            print(f"  ⚠️ 連携: ZIPファイルが見つかりません: {candidate}")
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

    # --- 手順10: 保存ボタンをクリック ---
    print("  [Step 10/10] 保存ボタンをクリック中...")
    page.click(SAVE_BUTTON_SELECTOR)

    # 保存確定モーダルの出現を待って確定 (キーボード操作: Tab x3 + Enter)
    print("  💬 保存確定モーダルを待機中（キーボード操作で承認します）...")
    page.wait_for_timeout(500) # モーダル表示待ち
    try:
        # 要素の有無に関わらず、フォーカスがモーダルにあると信じてキー入力を送信
        for i in range(3):
            page.keyboard.press("Tab")
            page.wait_for_timeout(200)
        page.keyboard.press("Enter")
        print("  ✅ キーボード操作（Tab x3 + Enter）を送信しました。")
    except Exception as e:
        print(f"  ⚠️ キーボード操作中にエラーが発生しました: {e}")

    # ページ遷移を待機
    page.wait_for_timeout(2000)
    page.wait_for_load_state("networkidle")
    print("  ✅ メタデータ保存完了！")
    
    # ハンドラの解除
    page.remove_listener("dialog", handle_initial_dialog)
    
    return zip_path


def request_approval_flow(page, zip_path: str, debug: bool = False):
    """
    保存完了後の申請フロー 10ステップを実行する。
    """
    print("\n" + "-" * 30)
    print("🚀 申請（リクエスト）フローを開始します")
    print("-" * 30)

    # ダイアログハンドラの設定 (個数変更時のOKボタン)
    def handle_dialog(dialog):
        print(f"  💬 ダイアログ出現: {dialog.message}")
        dialog.accept()
        print("  ✅ ダイアログを承認しました。")

    page.on("dialog", handle_dialog)

    # ZIP内のスタンプ個数を判定
    stamp_count = 40  # デフォルト
    try:
        with zipfile.ZipFile(zip_path, 'r') as z:
            # main.png, tab.png, meta 等を除いた純粋な数字名のファイルをカウント
            all_files = z.namelist()
            # 拡張子を除いたファイル名が数字のものをカウント
            stamps = [f for f in all_files if f.lower().endswith(('.png', '.jpg')) 
                     and os.path.basename(f).split('.')[0].isdigit()]
            if stamps:
                stamp_count = len(stamps)
                print(f"  📊 ZIP内のスタンプ数を検知しました: {stamp_count}個")
    except Exception as e:
        print(f"  ⚠️ ZIP解析に失敗しました（デフォルトの40個を使用します）: {e}")

    steps = [
        ("1. スタンプ画像タブ", STAMP_IMAGES_TAB_SELECTOR, "click"),
        ("2. 編集ボタン", EDIT_IMAGES_BUTTON_SELECTOR, "click"),
        ("3. スタンプ個数選択", STAMP_COUNT_SELECT_SELECTOR, f"select_{stamp_count}"),
        ("4. 個数変更の確定", CONFIRM_COUNT_MODAL_OK_SELECTOR, "click"),
        # 5. ZIPアップロードボタン (統合済み)
        ("5. ZIPアップロードボタン", ZIP_UPLOAD_BUTTON_SELECTOR, "click"),
        # 6. はスキップ（5で完了）
        ("7. 戻るボタン", BACK_TO_MANAGE_BUTTON_SELECTOR, "click"),
        ("8. リクエストボタン", REQUEST_APPROVAL_BUTTON_SELECTOR, "click"),
        ("9. 同意チェックボックス", CONSENT_CHECKBOX_SELECTOR, "click"),
        ("10. 最終確定ボタン", FINAL_SUBMIT_BUTTON_SELECTOR, "click"),
    ]

    for name, selector, action in steps:
        print(f"  ▶️ {name} 実行中...")
        
        # セレクタがない（未設定）または要素が見つからない場合の対話的処理
        if not selector or not is_element_present(page, selector):
            print(f"\n  ⚠️ 【要確認】{name} の要素が見つかりません。")
            print(f"     1. ブラウザで {name} を手動で操作してください。")
            print(f"     2. (推奨) 開発者ツールでセレクタを取得し、config.py を更新してください。")
            input(f"     [準備ができたら Enter を押してください] ")
            # 手動操作後はスキップするか、再度試行する
            continue

        try:
            # --- 特別対応: 1. スタンプ画像タブ ---
            if name == "1. スタンプ画像タブ":
                # 要素の取得
                target_element = page.locator(selector).first
                target_element.wait_for(state="visible", timeout=10000)

                # 既に選択済みならスキップ
                class_attr = target_element.get_attribute("class") or ""
                if "selected" in class_attr:
                    print(f"  ⏭️ {name} は既に選択されているためスキップします。")
                    page.wait_for_timeout(500)
                    continue

                # 有効（Enabled）になるまで待機
                print(f"  ⏳ {name} が有効になるのを待機中...")
                for _ in range(20): # 最大10秒程度
                    if target_element.is_enabled():
                        break
                    page.wait_for_timeout(500)

            if action == "click":
                # --- 特別対応: 5. ZIPアップロードボタン ---
                if name == "5. ZIPアップロードボタン":
                    print("  📂 ファイル選択イベントを待機中...")
                    try:
                        with page.expect_file_chooser(timeout=10000) as fc_info:
                            page.click(selector)
                        file_chooser = fc_info.value
                        file_chooser.set_files(zip_path)
                        print(f"  ✅ ZIPファイルをアップロードしました: {os.path.basename(zip_path)}")
                        # 次のステップ（旧 6. ZIPファイル選択）は削除したためそのまま続行
                        continue
                    except Exception as e:
                        print(f"  ⚠️ ファイルアップロード中にエラーが発生しました（手動操作に切り替えます）: {e}")
                
                page.click(selector)
            elif action.startswith("select_"):
                # 動的な個数を選択
                target_count = action.split("_")[1]
                print(f"  🔢 個数を選択中: {target_count}個")
                page.select_option(selector, value=target_count)
            elif action == "upload":
                page.set_input_files(selector, zip_path)
            
            # 各操作の後に少し待機
            page.wait_for_timeout(1000)
            
            if debug:
                input(f"  [DEBUG] {name} 完了。次へ進むには Enter...")

        except Exception as e:
            print(f"  ❌ {name} でエラーが発生しました: {e}")
            input("  [手動で解決し、Enter で次へ進んでください] ")

    # ダイアログハンドラの解除
    page.remove_listener("dialog", handle_dialog)
    print("\n✅ 全ての申請プロセスが終了しました。")


def is_element_present(page, selector: str, timeout: int = 3000) -> bool:
    """要素が存在するか確認するヘルパー関数"""
    if not selector: return False
    try:
        page.wait_for_selector(selector, state="visible", timeout=timeout)
        return True
    except:
        return False


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
        print("  2. クリエイターズマーケットの「アイテム管理」から対象のスタンプセットを選択")
        print("  3. または「新規登録」ボタンを押して登録画面を表示する")
        print("-" * 50)
        print("\n💡 ヒント: 初回のZIPアップロード時、Antigravity（AI）がセレクタを確認します。")
        input("準備ができたら Enter を押してください...")

        # 初回の自動遷移
        navigate_to_new_stamp_form(page)

        completed = 0

        # --- 登録ループ ---
        for i, stamp in enumerate(stamps):
            theme = stamp.get("theme", f"No.{i+1}")
            print(f"\n{'=' * 50}")
            print(f"📝 [{i+1}/{len(stamps)}] {theme}")
            print(f"{'=' * 50}")

            if i > 0:
                # 2件目以降：自動で新規登録画面を開く
                navigate_to_new_stamp_form(page)

            try:
                zip_path = fill_stamp_form(page, stamp, debug=debug)
                
                # 申請フローの実行
                request_approval_flow(page, zip_path, debug=debug)

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
