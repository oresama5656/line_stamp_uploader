# セレクタ収集チェックリスト

## やり方
1. Chrome で LINE Creators Market のスタンプ新規登録画面を開く
2. F12 で開発者ツールを開く
3. 左上の矢印マーク（要素選択ボタン）をクリック
4. 対象の入力欄やボタンをクリック → 右側のコードが青くハイライトされる
5. 青い部分を右クリック → **Copy > Copy selector** を選択
6. 下の「ここに貼る」にペーストする

※ Copy selector が分かりにくければ Copy element でもOKです

---

## 1. 英語タイトル入力欄
```
#layout > main > form > section:nth-child(2) > div:nth-child(1) > div.MdCMN09FormTbl > table > tbody > tr:nth-child(3) > td > table > tr:nth-child(4) > td > div > div.mdInputItem.mdInputTxt > input[type=text]

```

## 2. 英語説明文入力欄
```
#layout > main > form > section:nth-child(2) > div:nth-child(1) > div.MdCMN09FormTbl > table > tbody > tr:nth-child(3) > td > table > tr:nth-child(5) > td > div:nth-child(1) > span > span.mdInputTxtArea > textarea:

```

## 3.「言語を追加」のリスト（ドロップダウン）
```
#layout > main > form > section:nth-child(2) > div:nth-child(1) > div.MdCMN09FormTbl > table > tbody > tr:nth-child(4) > td > div > span > span.mdInputSelect > select


##追加ボタン（言語を追加したあと押す必要あり）
#layout > main > form > section:nth-child(2) > div:nth-child(1) > div.MdCMN09FormTbl > table > tbody > tr:nth-child(4) > td > div > span > span.MdBtn01 > button
```

## 4. 日本語タイトル入力欄（言語追加後に出現する欄）
```
#layout > main > form > section:nth-child(2) > div:nth-child(1) > div.MdCMN09FormTbl > table > tbody > tr:nth-child(4) > td > table > tr:nth-child(4) > td > div > div.mdInputItem.mdInputTxt > input[type=text]

```

## 5. 日本語説明文入力欄（言語追加後に出現する欄）
```
#layout > main > form > section:nth-child(2) > div:nth-child(1) > div.MdCMN09FormTbl > table > tbody > tr:nth-child(4) > td > table > tr:nth-child(5) > td > div > span > span.mdInputTxtArea > textarea

```

## 6. コピーライト入力欄
```
#layout > main > form > section:nth-child(3) > div:nth-child(1) > div.MdCMN09FormTbl > table > tbody > tr:nth-child(2) > td > div > div.mdInputItem.mdInputTxt > input[type=text]

```

## 7. AI使用のラジオボタン（「AIが生成しています」の方）
```
#layout > main > form > section:nth-child(3) > div:nth-child(1) > div.MdCMN09FormTbl > table > tbody > tr:nth-child(3) > td > div:nth-child(1) > label > span.mdInputRadio > input[type=radio]

```

## 8. テイストカテゴリのリスト
```
#layout > main > form > section:nth-child(3) > div:nth-child(1) > div.MdCMN09FormTbl > table > tbody > tr:nth-child(4) > td > div > span > span > select

```

## 9. キャラクターカテゴリのリスト
```
#layout > main > form > section:nth-child(3) > div:nth-child(1) > div.MdCMN09FormTbl > table > tbody > tr:nth-child(5) > td > div:nth-child(1) > span > span > select:

```
##追加。販売開始設定：自動で販売を開始
csvのauto_sellに1が入力されていたらこれを押してほしい。
#layout > main > form > section:nth-child(3) > div:nth-child(1) > div.MdCMN09FormTbl > table > tbody > tr:nth-child(13) > td > div:nth-child(2) > label > span.mdInputRadio > input[type=radio]



## 10.「保存」ボタン
```
#layout > main > form > div.MdCMN15Submit > span.MdBtn01.mdBtn01Cr01 > label

```

