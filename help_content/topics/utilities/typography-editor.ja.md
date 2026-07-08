---
title: タイポグラフィー エディタ
---

タイポグラフィー エディタは、テキストの外観を完全に制御できる共有スタイルユーティリティです。ページビルダーやヘッダ/フッタービルダーやメニュービルダーの任意の要素でタイポグラフィーのプロパティを編集するたびに、ポップアップパネルとして表示されます。

![タイポグラフィー エディタ](/static/core/admin/img/help/typography-editor/typography-editor.webp)

## ライブプレビュー

エディタは、パネルの上部に並べて表示される比較を表示します：

| Box | Purpose |
|-----|---------|
| **Current** | 現在のタイポグラフィー スタイルで "The quick brown fox..." を表示 |
| **New** | 設定を調整するたびにリアルタイムで更新され、適用する前の結果を表示 |

これにより、変更を適用せずに変更前と変更後の比較が可能になります。

## フォントタブ

エディタを開くと、フォントタブがデフォルトの表示になります。

**フォントファミリ** — カテゴリごとに70以上のフォントが整理された検索可能なドロップダウン。各フォントは独自のフォントスタイルでプレビューされるため、選択する前に見た目を確認できます。必要に応じてGoogle Fontsからオンデマンドでフォントが読み込まれます。

**フォントサイズ** — px、em、rem、%をサポートする数値入力。デフォルトは16pxです。

**フォントウェイト** — 100（スリム）から900（ブラック）までのスライダー：

| Value | Name |
|-------|------|
| 100 | Thin |
| 200 | Extra Light |
| 300 | Light |
| 400 | Regular |
| 500 | Medium |
| 600 | Semi Bold |
| 700 | Bold |
| 800 | Extra Bold |
| 900 | Black |

すべての9つのウェイトをサポートしているフォントはすべてではありません。エディタは選択したフォントファミリで利用可能なウェイトを表示します。

**フォントスタイル** — Normal、Italic、Obliqueの切り替えボタン。

## スペースタブ

文字の周りや間のスペースを微調整します：

| Control | What It Does | Default |
|---------|-------------|---------|
| **Line Height** | 行と行の間の垂直スペース | normal |
| **Letter Spacing** | 個々の文字間の水平スペース | normal |
| **Word Spacing** | 単語間の水平スペース | normal |
| **Text Indent** | 段落の最初の行のインデント | 0 |

各スペースコントロールには、単位セレクタ（px、em、rem、%）が含まれています。

## スタイルタブ

テキストの装飾と視覚効果を制御します：

- **Text Decoration** — None、Underline、Overline、またはLine-through
- **Decoration Style** — Solid、Dashed、Dotted、Double、またはWavy（装飾が有効な場合に適用）
- **Decoration Color** — 装飾線の色選択、デフォルトはテキストの色
- **Text Shadow** — オフセット、ぼかし、色の制御を含むオプションのシャドウ効果

## 変換タブ

コンテンツを編集せずにテキストの文字の大小を変更します：

| Option | Result |
|--------|--------|
| **None** | テキストは書かれたまま表示 |
| **Uppercase** | ALL LETTERS ARE CAPITALIZED |
| **Lowercase** | all letters are lowercase |
| **Capitalize** | First Letter Of Each Word Is Capitalized |

このタブの追加コントロールには、**Text Align**（左、中央、右、両端揃え）、**Vertical Align**、**Text Direction**（LTRまたはRTL）が含まれます。

## 利用可能なフォントファミリ

エディタには、カテゴリごとにグループ化されたシステムフォントとGoogle Fontsのキュレーションされたライブラリが含まれています：

| カテゴリ | フォント |
|----------|-------|
| **システム** | システムデフォルト, Arial, Helvetica Neue, Helvetica, Segoe UI, Roboto, Ubuntu, Verdana, Tahoma, Trebuchet MS |
| **サンセリフ（モダン）** | Inter, Montserrat, Poppins, DM Sans, Space Grotesk, Plus Jakarta Sans, Outfit, Manrope, Figtree, Josefin Sans |
| **サンセリフ（クラシック）** | Open Sans, Lato, Nunito, Nunito Sans, Source Sans 3, Raleway, Rubik, Work Sans, Mulish, Cabin, Karla, Barlow, Lexend |
| **セリフ** | Playfair Display, Merriweather, Lora, Libre Baskerville, Cormorant Garamond, Source Serif 4, EB Garamond, Crimson Pro, Bitter, Fraunces, Spectral, Cardo, Alegreya |
| **セリフ（システム）** | Georgia, Times New Roman, Palatino, Book Antiqua, Garamond, Cambria |
| **モノスペース** | Source Code Pro, Fira Code, JetBrains Mono, Roboto Mono, IBM Plex Mono, Space Mono, Inconsolata, Consolas, Monaco, Menlo, Courier New, SF Mono |
| **ディスプレイ** | Oswald, Bebas Neue, Anton, Archivo Black, Rajdhani, Righteous, Abril Fatface, Archivo, Impact, Arial Black |

Google Fonts は選択されたときに自動的に読み込まれます。システムフォントは、プラットフォーム全体で信頼性のあるレンダリングを保証するため、適切な CSS フォールバックチェーンを使用します。

## 出現場所

Typography Editor は、テキストスタイルが必要な場所で利用できます:

- **Page Builder** — 任意の要素を選択し、Style タブを開き、Typography セクションをクリックします
- **Header/Footer Builder** — ナビゲーションリンク、ロゴテキスト、メニュー項目、フッターコンテンツのテキストをスタイル付けします
- **Menu Builder** — メニューのラベルとサブメニュー項目のタイポグラフィを制御します
- **Catalog Admin** — プロダクト説明やコンテンツエディタで、タイポグラフィのコントロールが公開されている場所で使用されます

エディタは、コンテキストに関係なく常に同じ一貫したインターフェースを通じてアクセスできます。

## ヒント

- **フォントを意図的にペアリングする** — ヘッダーにはディスプレイまたはセリフフォントを使用し、本文にはクリーンなサンセリフフォントを使用します。Playfair Display + Inter または Montserrat + Merriweather のようなクラシックな組み合わせが効果的です。
- **ページごとのフォントファミリを制限する** — 通常、ページごとに2〜3つのフォントファミリで十分です。それ以上になると、読み込み時間が遅くなり、視覚的な混乱を引き起こす可能性があります。
- **レスポンシブテキストのために相対単位を使用する** — em と rem は基本フォントサイズに合わせてスケールするため、テキストがさまざまな画面サイズに自動的に適応します。
- **ウェイトの可用性を確認する** — 400 と 500 でテキストが同じように見える場合、選択したフォントはそのウェイトをサポートしていない可能性があります。エディタは各フォントが提供するウェイトを示します。
- **すべてのデバイスでプレビューを確認する** — デスクトップサイズで見た目が良いテキストも、モバイルでは小さすぎるか大きすぎる可能性があります。Page Builder のデバイスプレビューを使用して確認してください。
- **ライブプレビューを使用する** — 変更を適用する前に、プレビューボックスで Current vs New を常に比較して、予期せぬ変更を避けてください。