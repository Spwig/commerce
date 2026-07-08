---
title: アフィリエイトポータルのカスタマイズ
---

Spwigのアフィリエイトポータルは、潜在的なアフィリエイトがプログラムについて学び、登録するための公開用のランディングページです。このポータルのカスタマイズにより、メッセージ、ブランド、コール・トゥ・アクションを、あなたのストアの独自のポジショニングと一致させることができます。よく設計されたポータルは、高品質なアフィリエイトを引き寄せ、訪問者をアクティブなパートナーに変えることができます。

## アフィリエイトポータルとは？

アフィリエイトポータルは、あなたのストアのドメインの`/affiliate/`でアクセス可能です。以下のような役割を果たします：

- **発見ページ** — 潜在的なアフィリエイトがコミッション構造、利点、要件について学ぶ場所
- **登録エントリーポイント** — 新規アフィリエイトの登録フォーム（ゲスト登録またはアカウントベース）
- **ログインゲートウェイ** — 既存のアフィリエイトはダッシュボードにアクセスするためにログインできます
- **ブランド展示** — ストアのアイデンティティとアフィリエイトプログラムの価値提案を反映

ポータルは、アフィリエイト設定の管理画面を通じて完全にカスタマイズ可能です。ヒーロー・メッセージ、特徴のハイライト、ステップバイステップのフロー、登録オプションを含みます。

![アフィリエイトポータルランディングページ](/static/core/admin/img/help/affiliate-portal-customization/portal-landing.webp)

## 設定へのアクセス

**マーケティング > アフィリエイトプログラム > ポータル設定**に移動してポータルをカスタマイズしてください。

アフィリエイト設定モデルは**シングレトン**です — あなたのストア全体にわたって、正確に1つの設定レコードがあります。すべてのフィールドはSpwigの翻訳システムを使用して**翻訳可能**です。そのため、ストアがサポートする各言語でメッセージをカスタマイズできます。

## ヒーロー・セクション

ヒーロー・セクションは、潜在的なアフィリエイトが最初に見る部分です。以下を含みます：

- **タイトル** — メイン見出し（例："Join Our Affiliate Program"）
- **サブタイトル** — プログラムの価値を説明する補足テキスト（例："Earn commissions by promoting premium products to your audience"）
- **統計** — 自動表示されるメトリクス：
  - 現在アクティブなプログラムの合計
  - 現在アクティブなアフィリエイトの合計
  - 平均コミッション率（すべてのアクティブなプログラムにわたって計算）
- **CTAボタン** — 自動生成されます：
  - **Sign In** — 既存のアフィリエイト向け
  - **Become an Affiliate** — 登録フローをトリガー

### ヒーロー・メッセージのカスタマイズ

| フィールド | 例 | 目的 |
|----------|----|------|
| **ヒーロータイトル** | "Partner With Us & Earn" | ベネフィットに焦点を当てた見出しで注目を集める |
| **ヒーロー・サブタイトル** | "Join 500+ affiliates earning competitive commissions on every sale you refer" | ソーシャル証拠を提供し、オファーを明確にする |

統計は**自動的に計算**され、アクティブなプログラムとアフィリエイトに基づいてリアルタイムで更新されます。これらの値を手動で編集することはできません。

## フィーチャー・セクション

フィーチャー・セクションは、アフィリエイトがなぜあなたのプログラムに参加すべきかを説明する**6つのカスタマイズ可能なベネフィット・カード**を強調します。各フィーチャー・カードには以下が含まれます：

- **アイコン** — FontAwesomeアイコンクラス（例：`fa-dollar-sign`, `fa-chart-line`, `fa-headset`）
- **タイトル** — ベネフィットの見出し（例："Competitive Commissions"）
- **説明** — 1〜2文の説明（例："Earn up to 15% on every sale you refer"）

### デフォルトのフィーチャー

アフィリエイトアプリを最初にインストールしたとき、Spwigはデフォルトのフィーチャーを提供します：

| アイコン | タイトル | 説明 |
|--------|--------|------|
| `fa-dollar-sign` | Competitive Commissions | あなたが紹介するすべての販売で、豊富なコミッションを獲得 |
| `fa-link` | Easy Tracking Links | どこでも使用できるユニークなトラッキングリンクを取得 |
| `fa-chart-line` | Real-Time Analytics | ダッシュボードでクリック数、コンバージョン数、収益を追跡 |
| `fa-calendar-check` | Reliable Payouts | PayPalまたは銀行振込で、期日通りに支払いを受け取る |
| `fa-headset` | Dedicated Support | 私たちのチームは、あなたの成功を支援するためにここにいます |
| `fa-gift` | Marketing Materials | バナー、画像、プロモーションコンテンツにアクセス |

### フィーチャーのカスタマイズ

フィーチャーはデータベース内の**JSON配列**として保存されます。管理画面のフォームで直接編集してください：

```json
[
  {
    "icon": "fa-percent",
    "title": "Up to 20% Commission",
    "description": "Earn industry-leading commissions on premium product sales"
  },
  {
    "icon": "fa-rocket",
    "title": "Fast Approval",
    "description": "Get approved in 24 hours and start promoting immediately"
  },
  {
    "icon": "fa-mobile-alt",
    "title": "Mobile Dashboard",
    "description": "Manage your links and track earnings from any device"
  }
]
```

**アイコンリファレンス：** FontAwesome 5 Freeのアイコンクラスを使用してください。アイコンをブラウズするには [fontawesome.com/icons](https://fontawesome.com/icons) にアクセスし、クラス名（例：`fa-trophy`, `fa-users`, `fa-star`）を使用してください。

## How It Works セクション

"How It Works"セクションは、アフィリエイトの旅を説明する**4ステップのビジュアルフロー**を表示します。各ステップには以下が含まれます：

- **タイトル** — ステップ名（例："Sign Up"）
- **説明** — 何が起こるかの1〜2文の説明

### デフォルトのステップ

| ステップ | タイトル | 説明 |
|--------|--------|------|
| 1 | Sign Up | 数分で無料のアフィリエイトアカウントを作成 |
| 2 | Get Your Links | 任意の製品やページに対してユニークなトラッキングリンクを生成 |
| 3 | Promote | コンテンツ、ソーシャルメディア、またはメールを通じて、あなたのアカウントにアクセスする人々にリンクを共有 |
| 4 | Earn Commissions | 顧客があなたの紹介リンクを使用して購入すると支払いを受け取る |

### ステップのカスタマイズ

ステップは**JSON配列**として保存されます。管理画面で編集可能です：

```json
[
  {
    "title": "Apply to Join",
    "description": "Submit your application and tell us about your platform"
  },
  {
    "title": "Get Approved",
    "description": "Our team reviews your application within 24 hours"
  },
  {
    "title": "Create Links",
    "description": "Access your dashboard and generate tracking links instantly"
  },
  {
    "title": "Start Earning",
    "description": "Earn commissions on every sale you refer — paid monthly via PayPal"
  }
]
```

ビジュアルフローは、ランディングページで各ステップを自動的に番号付け（1, 2, 3, 4）します。

## CTA セクション

登録フォームの直前に表示される**コール・トゥ・アクション（CTA）セクション**は、登録を促す最後の推奨です。

| フィールド | 例 | 目的 |
|----------|----|------|
| **CTAタイトル** | "Ready to Start Earning?" | 直接的な質問で緊急性を生み出す |
| **CTA説明** | "Join our affiliate program today and start earning commissions on products you already love and recommend." | ベネフィットを強調し、摩擦を排除 |

CTAセクションは、テキストの下に**Become an Affiliate**ボタンを自動的に表示します。

## 登録設定

新規アフィリエイトがどのように登録し、どの情報を提供するかを制御します。

### カスタム登録フォーム

**フィールド：** `custom_form`（FormBuilderフォームへのForeignKey）

SpwigのForm Builderを使用してカスタム登録フォームを構築している場合、ここに選択してください。これにより、登録時に追加情報を収集できます（例：ウェブサイトURL、対象者数、プロモーションチャネル）。

**空白のままに**して、デフォルトのアフィリエイト登録フォーム（メール、パスワード、支払い情報）を使用してください。

### ゲスト登録を許可

**フィールド：** `allow_guest_registration`（ブール値）

- **チェック済み** — まずSpwigアカウントを作成せずに申請可能
- **チェックされていない** — 申請する前にログインまたは顧客アカウントを作成する必要があります

**推奨：** ゲスト登録を有効にして摩擦を減らしてください。アフィリエイトを承認する前に、いつでも承認を要求して検証できます。

### 承認を必要とする

**フィールド：** `require_approval`（ブール値）

- **チェック済み** — 新規アフィリエイトはダッシュボードにアクセスする前に手動承認を待つ必要があります
- **チェックされていない** — 新規アフィリエイトは即座にリンクを作成できます

**推奨：** ブランド適合性、不正防止、または限定プログラムを検証したい場合は、手動承認を有効にしてください。

### 利用規約URL

**フィールド：** `terms_url`（URL）

アフィリエイトプログラムの利用規約へのオプションリンク。提供された場合、登録フォームはアフィリエイトが利用規約に同意するチェックボックスを表示します。

**例：** `/pages/affiliate-terms/`

### ウェルカムメッセージ

**フィールド：** `welcome_message`（テキスト）

成功した登録の直後にアフィリエイトに表示されるメッセージ。以下のように使用できます：

- ご登録ありがとうございます
- 次のステップを説明（例："24時間以内に申請を確認します"）
- スタートガイドリソースへのリンク

**例：**
```
Welcome to our affiliate program! We've received your application and will review it within 24 hours. Check your email for approval confirmation and login instructions.
```

## 多言語サポート

アフィリエイト設定内のすべてのテキストフィールドは、Spwigの翻訳ウィジェットを使用して**翻訳可能**です：

- ヒーロータイトル
- ヒーロー・サブタイトル
- フィーチャー（言語ごとにJSONを翻訳）
- How It Works ステップ（言語ごとにJSONを翻訳）
- CTAタイトル
- CTA説明
- ウェルカムメッセージ

### 翻訳の仕組み

可翻訳なフィールドを編集する際、各有効な言語のコンテンツを提供できる翻訳ウィジェットが表示されます。JSONフィールド（フィーチャー、ステップ）については、言語ごとに個別のJSONオブジェクトを提供します：

**英語：**
```json
[
  {"icon": "fa-dollar-sign", "title": "Competitive Commissions", "description": "Earn up to 15% on every sale"}
]
```

**スペイン語：**
```json
[
  {"icon": "fa-dollar-sign", "title": "Comisiones Competitivas", "description": "Gana hasta el 15% en cada venta"}
]
```

ポータルは、訪問者の言語設定に基づいて正しい言語バージョンを自動的に表示します。

## 変更のプレビュー

ポータル設定をカスタマイズした後：

1. **管理画面で変更を保存**
2. ストアのフロントエンドで`/affiliate/`にアクセスしてください（新しいタブで開く）
3. **登録フローをテスト**して"Become an Affiliate"をクリック
4. **ブランドの一貫性を確認** — ポータルはストアのデザインとメッセージに合っていますか？

繰り返しの変更を行い、ページをリフレッシュして即座に更新を確認できます。

## 例示的なカスタマイズ

### シナリオ1：Eコマースファッションストア

**目的：** ファッションインフルエンサーやブログライターを募集。

| 設定 | 値 |
|------|----|
| ヒーロータイトル | "Promote Styles You Love & Earn" |
| ヒーロー・サブタイトル | "Join 1,200+ influencers earning 12% commissions on every sale" |
| フィーチャー1 | アイコン：`fa-tshirt`、タイトル："Curated Fashion Collections"、説明："Premium apparel and accessoriesをプロモーション" |
| フィーチャー2 | アイコン：`fa-percentage`、タイトル："12% Commission"、説明："すべての製品に対する業界リーディングレート" |
| フィーチャー3 | アイコン：`fa-camera`、タイトル："Exclusive Content"、説明："製品の写真、動画、キャンペーンアセットにアクセス" |
| ゲスト登録を許可 | チェック済み |
| 承認を必要とする | チェック済み（ブランド適合性のための手動レビュー） |

### シナリオ2：B2B SaaSパートナープログラム

**目的：** エンタープライズソフトウェアの紹介に向けたビジネスコンサルタントやエージェンシーを募集。

| 設定 | 値 |
|------|----|
| ヒーロータイトル | "Partner With Us to Grow Revenue" |
| ヒーロー・サブタイトル | "Earn $500 per enterprise referral through our B2B partner program" |
| フィーチャー1 | アイコン：`fa-handshake`、タイトル："$500 Per Referral"、説明："資格のあるエンタープライズリードに対する固定コミッション" |
| フィーチャー2 | アイコン：`fa-clock`、タイトル："180-Day Cookie"、説明："複雑な販売サイクルのための長い属性期間" |
| フィーチャー3 | アイコン：`fa-user-tie`、タイトル："Dedicated Partner Manager"、説明："クライアント向けのホワイト・グローブサポート" |
| ゲスト登録を許可 | チェックされていない（B2Bはアカウントが必要） |
| 承認を必要とする | チェック済み（招待制プログラム） |
| 利用規約URL | `/pages/partner-program-terms/` |

## ヒント

- **ヒーロータイトル**をカスタマイズして、利点に焦点を当て、"Earn While You Sleep"のように"Affiliate Program Sign-Up"よりも魅力的なものにしましょう。
- サブタイトルに**ソーシャル証拠**（例："Join 500+ affiliates"）を使用して、信頼と信頼性を構築してください。
- 各利点を**FontAwesomeアイコン**で視覚的に強化してください — アイコンは、価値をすぐに伝える必要があります。
- フィーチャーの説明は**1〜2文**に保つ — ポータルはコンバージョンを目的としており、詳細な説明ではありません。
- ポータルを宣伝する前に、**登録フロー**を自分でテストしてください — 混乱するフォームフィールドや破損したリンクなどの摩擦ポイントをキャッチしてください。
- **ゲスト登録**を有効にして登録の摩擦を減らし、その後に**承認を必要とする**オプションを使用して、申請後にアフィリエイトを検証してください。
- **ウェルカムメッセージ**を使用して、期待値（承認のタイムライン、次のステップ、サポート連絡先）を設定し、サポートの問い合わせを減らしてください。
- ポータルを**季節的に更新**してキャンペーンと合わせてください — 特別なコミッションプロモーションや製品ローンチを強調してください。

すべてのMarkdownのフォーマット、画像パス、コードブロック、技術用語を、保存ルールに厳密に従って保持してください。