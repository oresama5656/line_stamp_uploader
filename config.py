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

