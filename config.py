# ============================================================
# config.py - LINE Creators Market セレクタ定義
# ============================================================
# 画面が変わった場合はここだけ修正すればOKです。
# セレクタは Chrome の F12 > 要素選択 > Copy selector で取得。
# ============================================================

# --- English 入力欄 ---
TITLE_EN_SELECTOR = '#layout > main > form > section:nth-child(2) > div:nth-child(1) > div.MdCMN09FormTbl > table > tbody > tr:nth-child(3) > td > table > tr:nth-child(4) > td > div > div.mdInputItem.mdInputTxt > input[type=text]'
DESC_EN_SELECTOR = '#layout > main > form > section:nth-child(2) > div:nth-child(1) > div.MdCMN09FormTbl > table > tbody > tr:nth-child(3) > td > table > tr:nth-child(5) > td > div:nth-child(1) > span > span.mdInputTxtArea > textarea'

# --- 言語追加ドロップダウン + 追加ボタン ---
ADD_LANGUAGE_SELECTOR = '#layout > main > form > section:nth-child(2) > div:nth-child(1) > div.MdCMN09FormTbl > table > tbody > tr:nth-child(4) > td > div > span > span.mdInputSelect > select'
ADD_LANGUAGE_BUTTON = '#layout > main > form > section:nth-child(2) > div:nth-child(1) > div.MdCMN09FormTbl > table > tbody > tr:nth-child(4) > td > div > span > span.MdBtn01 > button'
LANGUAGE_JAPANESE_VALUE = "ja"  # リスト内の Japanese の value 値

# --- Japanese 入力欄 (言語追加後に出現) ---
TITLE_JA_SELECTOR = '#layout > main > form > section:nth-child(2) > div:nth-child(1) > div.MdCMN09FormTbl > table > tbody > tr:nth-child(4) > td > table > tr:nth-child(4) > td > div > div.mdInputItem.mdInputTxt > input[type=text]'
DESC_JA_SELECTOR = '#layout > main > form > section:nth-child(2) > div:nth-child(1) > div.MdCMN09FormTbl > table > tbody > tr:nth-child(4) > td > table > tr:nth-child(5) > td > div > span > span.mdInputTxtArea > textarea'

# --- コピーライト ---
COPYRIGHT_SELECTOR = '#layout > main > form > section:nth-child(3) > div:nth-child(1) > div.MdCMN09FormTbl > table > tbody > tr:nth-child(2) > td > div > div.mdInputItem.mdInputTxt > input[type=text]'

# --- AI使用 ラジオボタン ---
AI_GENERATED_SELECTOR = '#layout > main > form > section:nth-child(3) > div:nth-child(1) > div.MdCMN09FormTbl > table > tbody > tr:nth-child(3) > td > div:nth-child(1) > label > span.mdInputRadio > input[type=radio]'

# --- カテゴリ リストボックス ---
TASTE_CATEGORY_SELECTOR = '#layout > main > form > section:nth-child(3) > div:nth-child(1) > div.MdCMN09FormTbl > table > tbody > tr:nth-child(4) > td > div > span > span > select'
CHARACTER_CATEGORY_SELECTOR = '#layout > main > form > section:nth-child(3) > div:nth-child(1) > div.MdCMN09FormTbl > table > tbody > tr:nth-child(5) > td > div:nth-child(1) > span > span > select'

# --- 保存ボタン ---
SAVE_BUTTON_SELECTOR = '#layout > main > form > div.MdCMN15Submit > span.MdBtn01.mdBtn01Cr01 > label'

# --- 申請フロー 10ステップ関連 (実行中に確定) ---
STAMP_IMAGES_TAB_SELECTOR = 'button.cm-product-tablist-tab:has-text("スタンプ画像")' # (1) 「スタンプ画像」タブ
SAVE_CONFIRM_MODAL_OK_SELECTOR = '.cm-confirm-panel button.cm-confirm-button-primary' # 保存ボタン後の確定ボタン
EDIT_IMAGES_BUTTON_SELECTOR = '#layout > main > div > div:nth-child(1) > div.cm-product-tablist > div:nth-child(2) > section > div.MdCMN15Submit > span > a' # (2) 「編集」ボタン
STAMP_COUNT_SELECT_SELECTOR = '#number_of_images' # (3) スタンプ個数選択リスト
CONFIRM_COUNT_MODAL_OK_SELECTOR = 'button.cm-confirm-button-primary' # (4) 個数変更確認ダイアログのOKボタン (カスタムモーダル)
# --- ZIPアップロード ---
ZIP_UPLOAD_BUTTON_SELECTOR = '#layout > main > div.MdCMN30ThemeTbl > div.mdCMN30ListCtrlGroup > div.mdCMN30ListCtrl > div.mdCMN30CtrlMain > form > p > label' # (5) 「ZIPファイルをアップロード」
ZIP_FILE_INPUT_SELECTOR = 'input[type="file"]' # (6) ファイル選択 (form内のinput)
BACK_TO_MANAGE_BUTTON_SELECTOR = '#layout > main > div.MdCMN30ThemeTbl > div.outer > div > a' # (7) 「戻る」ボタン
REQUEST_APPROVAL_BUTTON_SELECTOR = '#layout > main > div > div:nth-child(1) > div.cm-product-heading > div.cm-product-heading-button-panel > span > a' # (8) 「リクエスト」ボタン
CONSENT_CHECKBOX_SELECTOR = '#layout > main > div > div:nth-child(1) > div.cm-product-heading > div.cm-modal.cm-modal-dialog-centered > div > div.cm-confirm-content > div > div > div:nth-child(3) > label > input' # (9) 同意チェックボックス (1つ目)
FINAL_SUBMIT_BUTTON_SELECTOR = '#layout > main > div > div:nth-child(1) > div.cm-product-heading > div.cm-modal.cm-modal-dialog-centered > div > div.cm-confirm-panel > button.plain-btn-reset.cm-confirm-button.cm-confirm-button-primary > span' # (10) 最終確定ボタン

# --- デフォルト値 ---
DEFAULT_COPYRIGHT = "©ryo"
DEFAULT_AI_FLAG = "true"

# --- 有効なカテゴリ選択肢（LINE Creators Market 準拠） ---
VALID_TASTE_CATEGORIES = [
    "未設定",
    "カワイイ・キュート",
    "ラブリー",
    "カッコいい",
    "ほんわか・癒し",
    "方言・スラング",
    "シュール",
    "面白い・ネタ",
    "挨拶",
    "敬語・丁寧",
    "季節・行事",
    "吹き出し",
]

VALID_CHARACTER_CATEGORIES = [
    "未設定",
    "男性キャラ",
    "女性キャラ",
    "家族・カップル",
    "ネコ",
    "ウサギ",
    "イヌ",
    "クマ",
    "トリ",
    "パンダ",
    "アザラシ",
    "食べ物",
    "名前・名字",
    "その他",
]

