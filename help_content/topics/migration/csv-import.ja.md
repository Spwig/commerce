---
title: CSVファイルからのインポート
---

CSVインポートは、Spwigが直接接続できないストア向けの代替となる移行ルートです。BigCommerce、PrestaShop、Squarespace、Wix、手動で管理しているスプレッドシート、またはSpwigが理解できないカスタムシステムからの移行が必要な場合、ここが目的地になります。ライブ接続ではなく、データをCSVファイルにエクスポートしてここにアップロードしてください。

このガイドでは、CSVを使用するべきタイミング、CSVが移行できない内容、関与する5つのファイル、それらの準備方法、および列のマッピングの仕組みについて説明します。

## API接続の代わりにCSVを使用するべきタイミング

SpwigはWooCommerce、Shopify、Magento 2/Adobe Commerceと直接接続できます。それらについては[データ移行概要](migration-overview)をご覧ください。他のプラットフォームではCSVが唯一のオプションです。BigCommerce、PrestaShop、Squarespace、Wixには直接の統合がありません。また、スプレッドシートからのデータ統合、カスタム構築されたストアの廃止、またはインポートする内容を完全にコントロールしたい場合にもCSVが適しています。

## CSVができないこと

何かを準備する前に、このルートが残すものを把握してください。これはCSVインポートを使用する小売業者にとって最大の驚きの原因です。

- **商品画像はなし。** 商品は画像が添付されてインポートされます。インポート後、画像をアップロードしてください。
- **バリエーションはなし。** すべての商品は単純商品として作成されます。インポート後、Spwigでサイズ/色/スタイル構造を再構築してください。
- **クーポンはなし。** ディスカウントコードやプロモーションはCSV形式には含まれていません。
- **ブログコンテンツはなし。** 投稿や記事のためのCSVファイルはありません。

これらはインポートを妨げるわけではありません。ただ、商品がSpwigにインポートされた後、追加の作業が必要になることを意味します。インポート後の完全なチェックリストについては[移行後の確認](after-migration-review)をご覧ください。

## 関与する5つのファイル

CSVステップのウィザードでは、5つのファイル入力が提供され、それぞれに**テンプレートのダウンロード**ボタンがあります。ファイルをから頭で作成するのではなく、これらのテンプレートから始めてください。これにより、正しい列名が保証され、ステップ4で自動検出がより多くの作業を代行できます。

すべてのマークダウンの書式、画像のパス、コードブロック、および技術用語を保持してください。

| ファイル | 必須？ |
|---|---|
| 商品 | **必須** |
| カテゴリ | オプション |
| 顧客 | オプション |
| 注文 | オプション |
| レビュー | オプション |

Spwig が必須とするファイルは **商品** のみです — それ以外のファイルは、まだそのデータをお持ちでない場合は空のままにすることもできます。

### 商品 (必須)

| カラム | 説明 |
|---|---|
| `id` | ソースデータ内のユニークな識別子; 顧客には表示されません。 |
| `name` | 商品のタイトル。**必須です。** |
| `slug` | 名前の URL 友好的なバージョン; 空欄の場合は `name` から自動生成されます。 |
| `description` | 店舗表示で表示される説明。 |
| `price` | 商品の通常価格。**必須です。** |
| `sku` | 在庫管理単位 — **既存のアイテムをスキップ** が有効になっている場合に一致させるために使用されます。 |
| `stock_quantity` | 現在在庫にある単位数。 |
| `category` | この商品が所属するカテゴリ名。カテゴリファイル内の `name` と一致する必要があります。 |

### カテゴリ

| カラム | 説明 |
|---|---|
| `id` | ソースデータ内のユニークな識別子。 |
| `name` | カテゴリ名。**必須です。** |
| `slug` | 名前の URL 友好的なバージョン; 空欄の場合は自動生成されます。 |
| `description` | カテゴリの説明文。 |
| `parent_id` | このカテゴリの親カテゴリの `id`。空欄の場合はトップレベルを意味します。 |

### 顧客

| カラム | 説明 |
|---|---|
| `id` | ソースデータ内のユニークな識別子。 |
| `email` | 顧客のメールアドレス。**必須** — 注文とレビューを正しい顧客にリンクします。 |
| `first_name` | 顧客の名前。 |
| `last_name` | 顧客の姓。 |
| `phone` | 顧客の電話番号。 |

### 注文


| Column | Description |
|---|---|
| `id` | Unique identifier in your source data. |
| `customer_email` | Email of the customer who placed the order. **Essential** — links the order to a customer record. |
| `order_date` | The date the order was placed. |
| `status` | The order's status (e.g. completed, processing). |
| `total` | The order total. **Essential.** |
| `currency` | Currency code for the order total. |

### Reviews (Optional)

| Column | Description |
|---|---|
| `id` | Unique identifier in your source data. |
| `product_id` | The `id` of the product being reviewed, matching your products file. **Essential** — links the review to the right product. |
| `customer_email` | Email address of the reviewer. |
| `rating` | The star rating given. |
| `comment` | The review text. |
| `date` | The date the review was posted. |

## Preparing Your Files

- **Save as UTF-8** to avoid garbled accented characters, especially from a different source encoding.
- **Quote fields containing commas** — wrap a description or name containing a comma in double quotes so it isn't misread as a column break.
- **Include a header row.** The first row must contain your column names — a file with no header row is rejected.
- **Build category hierarchy with `parent_id`.** Give each category a unique `id`, then set a subcategory's `parent_id` to its parent's `id`. Blank means top-level.
- **Link orders to customers with `customer_email`**, matched against the `email` column in your customers file (or a guest record is created), rather than relying on internal ID numbers, which rarely line up across platforms.
- **Link reviews to products with `product_id`**, matching a value in the `id` column of your products file, or that review is skipped.

## Mapping Columns in Step 4

Step 4 shows a CSV Column Mapping panel.

Spwigはヘッダーをスキャンし、一般的な別名リストと自動的に一致する可能性のある項目を検出します。たとえば、`sku`フィールドは`barcode`、`part_number`、または`item_number`とも一致します。

他のプラットフォームから直接エクスポートされたヘッダーは、手動の作業なしに正しいマッピングが行われる場合があります。

各列について、自動検出された推測を承認するか、別の宛先フィールドを選択して上書きするか、「— この列をスキップ —」を選択して除外するかを選べます。マッピングは保存され、将来的なCSVのマイグレーションで再利用されます。ステップ4の全体像、自動フィールドマッピング、カテゴリマッピング、および税/送料のオプションについては、[Migration Field Mapping](migration-field-mapping)を参照してください。

<!-- screenshots-needed:
- url: /en/admin/migration/migrationjob/wizard/step4/
  filename: csv-column-mapping.webp
  description: Step 4 CSV Column Mapping panel showing auto-detected mappings with override dropdowns
  save-to: core/static/core/admin/img/help/csv-import/
  viewport: 1440x900
-->

## Common Errors and What They Mean

| Error | Meaning |
|---|---|
| `Products CSV is required.` | プロダクトファイルのアップロードを試みたにもかかわらず、ファイルをアップロードせずに進行しようとした場合に表示されます。Spwigが要求するのはこのファイルのみです。1つアップロードしてから続行してください。 |
| `{Type} CSV has no headers.` | 指定されたファイルの最初の行が空または欠落している場合に表示されます。列名を含むヘッダーロウを追加して再アップロードしてください。 |
| `{Type} CSV could not be read: ...` | Spwigが指定されたファイルを解析できなかった場合に表示されます。通常はファイルが破損している、エンコーディングが間違っている、または拡張子がCSVであるにもかかわらず実際にはCSVでないファイルのためです。再エクスポートし、再アップロードする前にファイルが正常に開けることを確認してください。 |

## Running the Import

マッピングが確認されたら、ステップ5からマイグレーションを開始してください。バックグラウンドで実行されるため、ウィンドウを閉じてもかまいません — 完了する前に戻って進捗状況とライブログを確認できます。結果を確認するには、[After Your Migration](after-migration-review)を参照してください。

CSVのインポートは特に**製品画像**と**バリエーション**を手動で完了するよう求めます — ファイルがどれほど完全であっても、これらは自動的に転送されません。

## Tips

- **すべてのファイルの「テンプレートをダウンロード」ボタンから始めてください** — これにより、列名のタイプミスを手動でマッピングする必要がある場合を避けることができます。
- **レビューのアップロード前に`product_id`の不一致を修正してください** — `product_id`がどの製品の`id`とも一致しないレビューは、何も接続することができず、スキップされます。
- **他のプラットフォームからのエクスポートでヘッダー名を変更しないでください** — 自動検出は多くの場合、エイリアスを通じてそれらをそのまま認識するため、マッピングに手動の作業が必要になることはほとんどありません。
- **インポート直後に画像とバリエーションに時間を割いてください** — これらはCSVが常に転送しない2つの要素であり、顧客が製品ページが空っぽであることに気づくまで忘れられがちです。
- **`parent_id`を使ってマルチレベルのカテゴリをモデル化してください** — サブカテゴリの`parent_id`をその親カテゴリの`id`に設定してネストさせ、トップレベルのカテゴリには空白にしてください。
- **「読み取ることができませんでした」エラーが発生した場合は、再エクスポートと再確認を行ってください** — これはほぼ常にソースファイルのエンコーディングや破損によるものであり、Spwig側で修正する必要はありません。