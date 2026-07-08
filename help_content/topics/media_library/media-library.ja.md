---
title: メディアライブラリ
---

メディアライブラリは、ストア全体で使用される画像、動画、3Dモデル、ファイルを管理するための中心的なハブです。ファイルをドラッグ＆ドロップしてアップロードし、フォルダやタグで整理し、システムが画像を高速ロードのために自動的に最適化します。

![メディアギャラリー](/static/core/admin/img/help/media-library/media-gallery.webp)

## ギャラリーインターフェース

サイドバーの **メディアライブラリ** に移動してギャラリーを開きます。インターフェースには3つのエリアがあります：

| Area | Location | Purpose |
|------|----------|---------|
| **Upload Zone** | Left sidebar, top | Drag and drop files to upload (images, videos, 3D models up to 100MB) |
| **Folders & Tags** | Left sidebar, below | Browse folders, filter by tags, access Recycle Bin |
| **Media Grid** | Main area | Search, filter, browse, and manage all your assets |

### Toolbar Controls

メディアグリッドの上にあるツールバーには以下が提供されます：

- **Search** — find assets by title, alt text, description, or tag name
- **Type filter** — show only Images, Videos, or 3D Models
- **Size filter** — filter by file size (Small, Medium, Large)
- **Bulk actions** — Select Items, Edit Details, Delete Selected
- **View modes** — Grid (large), Small Grid, or List view (persisted across sessions)

## ファイルのアップロード

左サイドバーの **Upload** ゾーンに1つまたは複数のファイルをドラッグしてアップロードするか、ゾーンをクリックしてファイル選択ダイアログを開きます。

### サポートされているフォーマット

| Type | Formats |
|------|---------|
| **Images** | JPEG, PNG, GIF, WebP, SVG, BMP, TIFF |
| **Videos** | MP4, WebM, MOV, MKV, AVI |
| **3D Models** | GLB, glTF |

### アップロードキュー

複数のファイルをアップロードする場合、キュー管理者が表示され、以下を示します：

- 各ファイルの名前とアップロード進行状況バー
- 並列アップロード（パフォーマンスのため、同時に最大2つ）
- アップロード後のファイルの最適化処理状態
- 個々のアップロードをキャンセルするか、完了した項目をクリアするオプション

キューはドラッグ可能で、最小化できます。これにより、アップロードが完了する間にも作業を続けることができます。

## 自動画像最適化

アップロードするすべての画像は自動的に最適化されます：

- **WebP変換** — 原本の画像と一緒にWebPバージョンが生成されます（品質85％）で、より高速なロードを実現
- **サムネイル生成** — 画像のプリセットに基づいて複数のサイズのバージョンが作成されます
- **EXIF方向** — 画像は正しい方向に自動的に回転されます

### システム画像プリセット

プラットフォームには、一般的な使用ケースをカバーする21の組み込みプリセットが含まれています：

| Preset | Dimensions | Crop | Used For |
|--------|-----------|------|---------|
| **Thumbnail** | 150 x 150 | Cover | Admin lists, quick previews |
| **Small** | 300 x 300 | Cover | Small product cards |
| **Medium** | 600 x 600 | Contain | Product cards, blog thumbnails |
| **Large** | 1200 x 1200 | Contain | Product detail pages |
| **Gallery** | 800 x 800 | Contain | Image galleries |
| **Hero** | 1920 x 1080 | Cover | Hero sections, page banners |
| **Banner** | 1200 x 400 | Cover | Promotion banners |
| **Card** | 400 x 300 | Cover | Feature cards, content cards |
| **Avatar** | 200 x 200 | Crop | Customer and staff avatars |
| **Product Listing** | 400 x 400 | Cover | Product grid cards |
| **Product Detail** | 1200 x 1200 | Cover | Full product images |
| **Product Thumbnail** | 100 x 100 | Cover | Variant selectors, mini carts |
| **Category Banner** | 1920 x 480 | Cover | Category page headers |
| **Category Thumbnail** | 300 x 200 | Cover | Category cards |
| **Logo Header** | 300 x 80 | Pad | Site header logo |
| **Logo Footer** | 200 x 60 | Pad | Site footer logo |
| **Logo Email** | 400 x 100 | Pad | Email template logos |
| **Logo Square** | 160 x 160 | Pad | Square logo placements |
| **Brand Logo** | 200 x 100 | Pad | Brand/partner logos |
| **Announcement Banner** | 800 x 300 | Cover | Announcement images |
| **Announcement Background** | 1200 x 800 | Cover | Announcement backgrounds |

システムプリセットは名前変更や削除ができません。デフォルトではカバーされていないサイズが必要な場合は、**メディアライブラリ > 画像サイズプリセット** で追加のカスタムプリセットを作成できます。

### クロップモード

| Mode | Behavior |
|------|----------|
| **Cover** | 全ての領域を埋め、必要に応じて端を切り取る — カードやバナーに適しています |
| **Contain** | 全ての画像を領域内に収め、必要に応じて透明なスペースを追加 — 商品画像に適しています |
| **Crop** | 中心を切り取って正確な寸法にします |
| **Pad** | 画像を収め、パディング（透明、白、黒）を追加 — ロゴに適しています |

## ファイルの整理

### フォルダ

メディアを論理的なグループに整理するためにフォルダを作成します。フォルダは任意の深さまでネストできます。左サイドバーのフォルダをクリックして、そのフォルダ内のアセットのみを表示します。**All Files** リンクはすべてのファイルを表示します。

### タグ

アセットにタグを追加して、フォルダ間での柔軟な整理を可能にします。タグは左サイドバーのクラウドに表示されます。タグをクリックして、そのタグでアセットをフィルタリングします。アセットは複数のタグを持つことができます。

### 検索

検索バーは、タイトル、代替テキスト、説明、またはタグ名でアセットを検索します。検索をタイプとサイズフィルタと組み合わせて、正確な結果を得るために使用します。

## アセット詳細

アセットをクリックして、大きなプレビューと完全なメタデータを持つ詳細ビューを開きます。

![アセット詳細](/static/core/admin/img/help/media-library/media-detail.webp)

詳細ビューには以下が表示されます：

- **Preview** — 元の寸法を持つ大きな画像プレビュー
- **File info** — タイプ、寸法、ファイルサイズ、アップロード日
- **編集用タブ**：

| Tab | Fields |
|-----|--------|
| **General** | Title, Alt Text, Description (すべての多言語ストアで翻訳可能) |
| **Technical** | MIMEタイプ、ファイルハッシュ、オリジナルファイル名、WebPバージョンの状態 |
| **Organization** | フォルダ割り当て、タグ、公開/非公開切り替え |
| **Advanced** | 焦点点座標、外部ID、メタデータJSON |

### 翻訳可能なフィールド

タイトル、代替テキスト、説明は翻訳をサポートしています。各フィールドの隣にある翻訳アイコンをクリックして、有効な言語の翻訳を追加します。これにより、画像の代替テキストと説明がSEOとアクセシビリティのために適切にローカライズされます。

### 使用状況の追跡

システムは、各アセットがプラットフォーム全体でどこで使用されているかを追跡します。下部の **Media usages** セクションは、このアセットを参照しているすべてのモデルとフィールドを表示し、変更または削除する前の影響を理解するのに役立ちます。

## 動画サポート

メディアライブラリにアップロードされた動画は自動的に分析されます：

- **メタデータ抽出** — 持続時間、解像度、フレームレート、ビットレート、コーデックが取得されます
- **ポスター画像** — 動画からプレビュー用のサムネイルが生成されます
- **ストリーミング** — 動画は、フルファイルのダウンロードなしでシークするための範囲リクエストをサポートします
- **オプションの変換** — 動画を最適化されたWebM/AV1形式に変換して、より高速な配信が可能です

## 回收箱

アセットを削除すると、**回収箱**に移動し、永久に削除されません。これは、誤った削除を防ぎます。

| Action | What It Does |
|--------|-------------|
| **Delete** | アセットを回収箱に移動（ソフト削除） |
| **Restore** | 削除されたアセットを元の場所に戻します |
| **Permanent Delete** | アセットとすべてのサムネイルをストレージから永久に削除します |
| **Empty Recycle Bin** | 回収箱内のすべての項目を永久に削除します |

左サイドバーの **Recycle Bin** をクリックして、削除されたアセットを表示および管理します。

## メディアライブラリの使用場所

メディアライブラリは、プラットフォーム全体に統合されています：

| Feature | How It Uses Media |
|---------|------------------|
| **Product catalog** | 商品画像、バリエーション画像、カテゴリバナー |
| **Blog** | 特定画像、CKEditor経由でコンテンツ内の画像 |
| **Page Builder** | 画像要素、ヒーローバックグラウンド、ギャラリーコンポーネント |
| **Header/Footer Builder** | ロゴ画像、背景画像 |
| **Site Settings** | サイトロゴとファビコン |
| **Announcements** | 公告画像と背景 |
| **CKEditor** | すべての豊富なテキスト画像アップロードはメディアライブラリ経由でルーティングされます |
| **Loyalty Program** | リワードとティア画像 |

これらの機能のいずれかで画像を選択すると、メディアライブラリギャラリーがモーダルとして開き、簡単にブラウジングと選択が可能です。

## ヒント

- **説明的なタイトルと代替テキストを使用** — 良いメタデータはSEOとアクセシビリティを向上させます。システムは、ストアフロント全体で代替テキストを使用して画像タグにします。
- **ファイルをアップロードする前にフォルダで整理** — 複数のファイルをアップロードする前に、フォルダ構造（例：Products, Blog, Banners, Logos）を作成してください。アップロードしながら整理するよりも、後で再整理する方がはるかに簡単です。
- **クロスカットカテゴリにタグを使用** — 「seasonal」、「sale」、または「lifestyle」といったタグは、複数のフォルダにまたがるアセットを検索するのに役立ちます。
- **削除する前に使用状況を確認** — 使用状況追跡セクションは、アセットが参照されている場所を示します。使用されているアセットを削除すると、ストアフロントに破損した画像が残る可能性があります。
- **WebPに任せましょう** — 自動WebP変換は、JPEGと比較してファイルサイズを25-35％削減しつつ、品質の低下は目立ちません。アップロード前に画像を手動で変換する必要はありません。
- **カスタムプリセットを作成** — 特定の画像サイズが必要なユニークなレイアウトがある場合は、手動で画像をリサイズするのではなく、カスタムプリセットを作成してください。