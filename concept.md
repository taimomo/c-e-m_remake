# サイト刷新

## 製作ページ

1. トップページ（index.html）
2. 会社概要(about.html)
3. 製品紹介(product.html)
4. 事例紹介(delivery_record.html)
5. マイクロ水力の蘊蓄 1&2（micro-feature.html & micro-hydro.html）
6. お問い合わせ（contact.html）

    ### ※ ページの共通化（include）

    - ヘッダー部分（header.html）
    - フッター部分（footer.html）
    - ハンバーガーメニュー（モバイルのみ overlay.html）
    - サイドメニュー（取り敢えず用意 aside.html）

## 必要要件

-   [x] 各種ページの作成（雛形）
-   [x] 各種ページコンテンツ作成
-   [x] リンク作成
-   [x] 画像用意
-   [x] マルチデバイス対応
-   [ ] スタイルセッテイング(tailwind 採用)

## 製作過程

### sanitize.css 適用

-   レイアウト用にリセット css を選定 → tailwind を採用するなら*modern.css*が理想？
-   *a (moere) Modern css Reset*が存在するためコードを適当な css にコピー（`modern.css`）
-   *style.css*に`modern.css`記述

### section の追加

-   `header`や`footer`は*include*フォルダ内に共通化パーツとして配置。

    ***-include*部品の配置-**

    | 該当部  | ファイル名     |
    | ------- | -------------- |
    | header  | `header.html`  |
    | footer  | `footer.html`  |
    | overlay | `overlay.html` |
    | aside   | `aside.html`   |

### トップページの text 作成

-   メインとなるタグや文章を大まかに記載。
-   画像やデザインは追々設定。
-   *header*下の画像は下記を使用。
    ![いいことたくさんの水力発電](/img/energy2_img@2x.jpg)
-   ~~bootstrap や fontawesome の CDN 記述~~<br>
    tailwind を使用。fontawesome の使用は適宜。

### 共通部分(_include_)の設定

-   SSI が使えるか分からないので javascript で記述
-   [x] ウィンドウを縮めると header のメニュー部分が欠けている。修正必要。(修正済)

### about ページの作成

-   会社概要と業務内容を記述<br>
    取り敢えず文章のみでデザインは後ほど

### ~~water~~ micro-hydro & micro-feature ページ作成

-   水力発電関連のページを追加し、文章を作成。<br>
    取り敢えず文章と区切りのみでデザインは後ほど
-   ページは「マイクロ水力とは？」「特徴・設置場所」「弊社の取り組み」の３構成
-   会社業務に焦点を当て、水力の何ぞやについては最低限。

### product ページの作成

-   製品紹介ページを作成。基本的にはこれまでの作成資料を利用する形。
-   構造的な部分は図面も使うが寸法等は入らないようにする。

### ~~case~~ delivery-record ページの作成

-   納入事例ページを作成。表と画像をメインにして、文章はほとんど入れない。
-   表と画像を横並びにして表示（後々の話）

### aside ページの作成

-   サイドバーを表示。内容はとりあえず他へのリンク。
-   コンテンツの枠組みを抜本的に改良。全ページ（contact.html 以外）を`<main><main-contents><article></article><aside></aside></main-contents></main>`の構成にする。
-   header と footer に div が入っていたため削除

### ページ全体のタグ調整

-   main と aside の区切りや article の使い方などが変なので修正。
-   中央のメインコンテンツを main にし、class も main 絡みに変更。<br> サイドバーは aside にし、class も aside 絡みに変更。

### ページの配色とレイアウトを調整

-   ページ全体の配色を決定。
-   会社ロゴや文言の配置が適当なので header として相応しく配置する。

### ページデザインを決定

-   本格的にページのデザインを決定する。
-   細かい言い回しや margin 等は進めながら調整するが、基本的にここで決めたデザインに従ってコーディングを行う。

### ページテキストを編集

-   デザイン内容に基づいてテキストを編集。
-   テキスト以外は画像の位置やテーブルの有無等を適当に記載
