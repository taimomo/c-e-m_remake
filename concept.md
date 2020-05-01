# サイト刷新

## 製作ページ

1. トップページ（index.html）
2. 会社概要(about.html)
3. 製品紹介(product.html)
4. 事例紹介(case.html)
5. お問い合わせ（contact.html）
   **※ 追々検討**

## 必要要件

- [x] 各種ページの作成（雛形）
- [ ] 各種ページコンテンツ作成
- [ ] リンク作成
- [ ] スタイルセッテイング
- [ ] 画像用意
- [ ] マルチデバイス対応

## 製作過程
 ### sanitize.css適用
  - レイアウト用にsanitize.cssを作成
  - style.cssにて```@import url(sanitize.css)```記述

 ### sectionの追加
  - index.html内に```header```や```footer```などのセクションを設定

 ### トップページのtext作成
  - メインとなるタグや文章を大まかに記載。
  - 画像やデザインは追々設定
  - bootstrapやfontawesomeのCDN記述
  
 ### 共通部分のinclude設定
  - headerやfooterなどの共通部分を個別に切り分け全ページで共有。
  - SSIが使えるか分からないのでjavascriptで記述
  - [ ] ウィンドウを縮めるとheaderのメニュー部分が欠けている。修正必要。(後々変更)

 ### aboutページの作成
  - 会社概要と業務内容を記述<br>
    取り敢えず文章のみでデザインは後ほど