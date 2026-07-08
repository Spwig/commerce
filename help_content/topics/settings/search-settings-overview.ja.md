---
title: 検索設定の理解
---

SearchSettings インターフェースは、Spwig ストアのすべてのグローバルな検索動作を制御します。この単一の設定ページは、8タブインターフェースを使用して、基本的な有効化から高度なパフォーマンス調整に至る検索オプションを整理しています。ここでの変更は、エンジンレベルで上書きされない限り、すべての検索エンジンに適用されます。

このガイドでは、各タブを順に説明し、各設定の役割と調整するべきタイミングについて説明します。

![Search Settings General Tab](/static/core/admin/img/help/search-settings-overview/search-settings-general.webp)

## The 8-Tab Interface

SearchSettings はシングルトンモデルです - ご全体のストアに対して、1つの設定レコード (pk=1) だけが存在します。インターフェースは8つのタブに分割されています:

| Tab | Purpose |
|-----|---------|
| **General** | 検索の有効/無効、基本パラメータの設定 |
| **Autocomplete** | 予測検索ドロップダウンの動作を構成 |
| **Content Types** | 検索可能なコンテンツの種類を選択 |
| **Deep Indexing** | 検索に含まれる商品データを制御 (パフォーマンスへの影響) |
| **Fuzzy Matching** | 漏字への寛容度と類似度のしきい値 |
| **Weights** | 検索結果のランキングに使用される関係性の倍率 |
| **Caching** | レスポンス時間と新鮮さのトレードオフ |
| **Analytics** | クエリの追跡とプライバシー設定 |

各タブは、検索設定の特定の側面に焦点を当てています。

## General Tab

General タブには、すべての検索に影響を与えるコア設定が含まれています:

**Enable Search** - 検索システムのマスターティグル。無効にすると、ストア全体で検索機能が無効になります。包括的に、オートコンプリートと検索結果ページも無効になります。

**Minimum Query Length** - デフォルト: 2文字。この長さ未満の検索は拒否されます。これを1に設定すると、1文字の検索 (例: "A") が可能になりますが、サーバーの負荷が増加します。

**Results Per Page** - デフォルト: 20項目。検索結果ページのページネーションを制御します。値を高く設定 (30-50) すると、ページネーションのクリック回数は減少しますが、ページの読み込み時間が増加します。

## Content Types Tab

![Content Types Settings](/static/core/admin/img/help/search-settings-overview/search-settings-content-types.webp)

検索結果に表示されるコンテンツタイプを切り替えます:

- **Products** - 物理的、デジタル的、サブスクリプション商品
- **Categories** - 商品カテゴリ
- **Brands** - 商品ブランド
- **Blog Posts** - ブログコンテンツ

**Performance Note**: コンテンツタイプが少ないほど検索が速くなります。有効にしたタイプごとに追加のデータベースクエリが発生します。ブログがない場合は、Blog Posts を無効にして応答時間を改善してください。

## Deep Indexing Tab

⚠️ **PERFORMANCE WARNING** - これらの設定には、パフォーマンスに大きな影響があります。

![Deep Indexing Settings](/static/core/admin/img/help/search-settings-overview/search-settings-deep-indexing.webp)

Deep indexing は、検索に含まれる商品関連データを制御します:

**Index SKUs** - デフォルト: ON, 低影響。商品とバリアントのSKUを検索に含めます。顧客が商品コードで検索する必要があるB2Bストアでは必須です。

**Index Attributes** - デフォルト: ON, 中程度の影響。商品属性 (色、サイズ、素材) を検索に含めます。属性テーブルへのJOINを追加します。ファッションや設定可能な商品にとって重要です。

**Index Custom Fields** - デフォルト: ON, 中程度の影響。販売業者が定義したカスタムフィールドを検索結果に含めます。JSONFieldのトラバースが必要です。

**Index Reviews** - デフォルト: ON, 中程度-高影響 ⚠️

レビューのインデックス化は、承認済みのレビューのタイトルとコメントを検索に含めます。レビューテーブルへのJOINとテキスト検索のオーバーヘッドを追加します。レビューが多いカタログには役立ちます。

**Index Documents** - デフォルト: OFF, **VERY HIGH IMPACT** ⚠️

ドキュメントインデックス化は、デジタル商品に添付されたPDF、DOCX、XLSXファイルからテキストを抽出します。この機能:

- 初期インデックス化に非常に高価なコストがかかる
- すべての検索でクエリのオーバーヘッドを大幅に増加させる
- 大きなファイルでタイムアウトを引き起こす可能性がある
- **デジタル商品ストアで検索可能なドキュメントがある場合にのみ有効にしてください**
- **気軽に有効にしないでください** - まずパフォーマンスへの影響をテストしてください

## Fuzzy Matching Tab

![Fuzzy Matching Settings](/static/core/admin/img/help/search-settings-overview/search-settings-fuzzy-matching.webp)

Fuzzy matching は、Levenshtein距離を使用してタイプミスを処理します:

**Enable Fuzzy Matching** - 類似した語 (例: "laptop" が "labtop" に一致) に検索を一致させます。

**Similarity Threshold** - デフォルト: 0.80 (80% 類似)。範囲: 0.0-1.0。高い値はより近い一致を必要とし、実行速度が速くなります。低い値はより多くのタイプミスを補正しますが、関係性のない結果を返す可能性があります。

**Max Edit Distance** - デフォルト: 2文字の変更。挿入、削除、置換の最大数。低い値 (1) はパフォーマンスを向上させますが、タイプミスの補正は少なくなります。

## Weights Tab

Weights は、関係性スコアリングを制御します - 検索結果のランキング方法。Weights タブは、各検索可能なフィールドのデフォルトの倍率を表示します:

- weight_name: 1.50 (商品名が最も重要)
- weight_sku: 1.20
- weight_description: 0.80
- weight_categories: 0.80
- weight_attributes: 0.70
- weight_brands: 0.70
- weight_blog_posts: 0.60
- weight_reviews: 0.50

これらのデフォルト値は、ほとんどの電子商取引ストアに適しています。Weights の調整とその影響についての詳細な情報については、[Relevance Weights and Deep Indexing](/en/admin/help/relevance-weights-deep-indexing/) トピックを参照してください。

## Caching Tab

![Caching Settings](/static/core/admin/img/help/search-settings-overview/search-settings-caching.webp)

キャッシュは、最近の検索結果を保存することで検索パフォーマンスを大幅に向上させます:

**Autocomplete Cache TTL** - デフォルト: 60秒。オートコンプリート結果がキャッシュされる時間。TTLを短く設定 (30-45秒) すると、結果はより新鮮になりますが、データベースクエリが増加します。TTLを長く設定 (90-120秒) すると、より高速になりますが、結果が古くなる可能性があります。

**Results Cache TTL** - デフォルト: 300秒 (5分)。検索結果ページのキャッシュ期間。TTLを長く設定すると、パフォーマンスが大幅に向上しますが、新商品の表示が遅れます。

**Trade-offs**: キャッシュは、パフォーマンス最適化において最も効果的な方法です。検索が遅い場合は、機能を無効にする前に、これらの値を増やすことをお勧めします。

## Analytics Tab

![Analytics Settings](/static/core/admin/img/help/search-settings-overview/search-settings-analytics.webp)

**Track Search Queries** - 検索分析ダッシュボードを有効にします。クエリテキスト、結果数、応答時間、タイムスタンプを記録します。

**Track User Information** - ログインユーザーと検索を関連付けます。プライバシー規制 (GDPR、CCPA) に準拠するため、無効にすることをお勧めします。

**Track Session Information** - セッションIDを使用して、匿名ユーザーの検索を追跡します。個人データなしで検索パターンを特定するのに役立ちます。

## Singleton Pattern

SearchSettings はシングルトンパターンを使用しています - データベースには、1つの設定レコード (pk=1) だけが存在します。管理画面で検索設定にアクセスすると、常に同じレコードを編集中になります。

「Add」または「Delete」オプションはありません - ただ「Change」だけです。すべての検索エンジンは、これらの設定を継承しますが、エンジンごとの上書き設定を指定した場合 (まれ) は例外です。

## Tips

- **デフォルト値を変更しないでください、特定の必要がない限り** - デフォルト設定は、典型的な電子商取引ストアに最適化されています
- **ドキュメントインデックス化を気軽に有効にしないでください** - あくまでデジタル商品ストアで検索可能なドキュメントがある場合にのみ有効にしてください。パフォーマンスへの影響をまずテストしてください
- **分析で応答時間を監視してください** - オートコンプリートは<200ms、フル検索は<500msを目標にしましょう
- **パフォーマンスが遅い場合はキャッシュTTLを増やしてください** - キャッシュは、パフォーマンス改善の最も簡単な方法です
- **週に1回、ゼロ結果のクエリを確認してください** - これにより、欠落している商品や必要な同義語が明らかになります
- **使用していないコンテンツタイプを無効にしてください** - ブログがない場合は、Blog Postsを無効にして検索を速くしてください

Remember: Preserve all markdown formatting, image paths, code blocks, and technical terms exactly as shown in the preservation rules.