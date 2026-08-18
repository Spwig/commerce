---
title: 購読プラン
---

購読プランを使用すると、製品に対して再発生する請求を提供できます。消耗品、サービス、カスタムボックス、または顧客が繰り返し購入する製品に最適です。このガイドでは、プランの作成と構成、価格層の設定、トライアル期間の追加、オプションの追加機能の添付方法について説明します。

## はじめに

管理サイドバーの**サブスクリプション > サブスクリプションプラン**に移動してください。プラン一覧には、料金モデル、アクティブな購読者数、表示状態が表示されます。

![サブスクリプションプラン一覧](/static/core/admin/img/help/subscription-plans/plan-list.webp)

新しいプランを作成するには、**ウィザードで作成**ボタンをクリックしてください。これにより、ステップバイステップで設定を完了するウィザードが開きます。それに隣接する**+ プランを追加**ボタンは、手作業ですべてを構成したいマーチャント向けに空のフォームを開きます。

単独のプランは購入可能ではありません。これはテンプレートです。ここで作成したものを、製品の**サブスクリプション**タブ（シンプル、変動、デジタル製品のみ）から1つ以上の製品に接続して、実際に購読できるようにしてください。そのステップについては、[製品をサブスクリプションとして販売する](/help/selling-products-as-subscriptions)を参照してください。

## プランエディタ

一覧からプラン名、または铅筆アイコンをクリックして既存のプランを開くと、プランエディタに移動します。ヘッダーには、プラン名、料金モデル、**有効**/**無効**、**パブリック**/**プライベート**のステータスバッジ、作成日が表示されます。ヘッダーの右上隅の2つのボタンで変更を保存します。チェックマークのアイコンは一覧に戻って保存し、チェックマークのないアイコンはページにとどまりながら引き続き編集を続けられます。

ヘッダーの下には、一目で確認できる統計スティックが表示されます。**アクティブなサブスクリプション**、**価格層**、**オプション追加**、**総収益**。

フォームの残りの部分は5つのタブに整理されています。

{"| Tab | What it contains |\n|-----|-------------------|\n| **General** | Plan Information (name, slug, description) and Status (active/public) |\n| **Pricing** | Pricing Configuration, Trial Period, and Limits & Restrictions |\n| **Tiers & Add-ons** | The Pricing Tiers and Add-ons editors |\n| **Lifecycle** | Cancellation Policy and Plan Change Behavior |\n| **Advanced** | Provider Integration and Statistics |\n|\nThe sections below walk through each tab's settings. When you create a brand-new plan directly from **+ Add Plan** (rather than the wizard), the same fields appear in a single scrollable form instead of tabs — save the plan once and reopen it to get the full tabbed editor.\n|\n## Plan information (General tab)\n|\nThe **Plan Information** card captures the core identity of your plan.\n|\n- **Plan Name** — The name customers see when subscribing. Click the globe icon to add translations for other store languages.\n- **Slug** — A URL-friendly identifier auto-generated from the name (e.g., `premium-plan`). This is used internally and in integrations.\n- **Description** — Optional text describing what the plan includes. Supports translations.\n|\nThe **Status** card on the same tab controls the **Active** and **Public** toggles — see [Visibility and status](#visibility-and-status) below.\n|\n![General tab of the plan editor](/static/core/admin/img/help/subscription-plans/edit-form-general-tab.webp)\n|\n## Pricing model (Pricing tab)\n|\nThe **Pricing Configuration** card controls how pricing is structured for this plan:\n|\n| Pricing Model | Best For |\n|---------------|----------|\n| **Tiered Pricing** | Offering monthly, quarterly, and annual commitment options with discounts for longer terms |\n| **Quantity-Based** | Per-seat or per-user pricing where the total scales with quantity (e.g., team licenses) |\n| **Flat Rate** | A single fixed price with no variations |\n|\nPreserve all markdown formatting, image paths, code blocks, and technical terms."}

For **Quantity-Based** plans, check **Allow Quantity** and set the **Minimum Quantity** (minimum seats required) and optionally a **Maximum Quantity** to cap how many seats a subscriber can purchase.

![Pricing tab of the plan editor](/static/core/admin/img/help/subscription-plans/edit-form-pricing-tab.webp)

## Pricing tiers (Tiers & Add-ons tab)

Pricing tiers define the billing frequency and discount options available to customers on this plan. Add them in the **Pricing Tiers** card on the **Tiers & Add-ons** tab, alongside the Add-ons editor.

Each tier has these fields:

- **Tier Name** — The label shown to customers (e.g., `Monthly`, `Annual — Save 20%`). Supports translations.
- **Billing Cycle** — How often the customer is charged: Daily, Weekly, Monthly, Quarterly, Semi-Annual, or Annual.
- **Billing Interval** — The multiplier for the billing cycle. Set to `2` with Monthly to bill every 2 months.
- **Discount Percentage** — The discount applied to the product price for this tier. Set to `0` for full price, or `20` to give 20% off. This discount stacks on top of any sale pricing on the product itself.
- **Default Tier** — Mark one tier as the default to pre-select it for customers when they view the subscription options.

The discount applies starting from the customer's very first billing cycle, not just on renewals — a tier with a 20% discount charges 20% off from day one (or from the first charge after a trial, if the plan has one).

### Example: tiered plan with three options

For a "Coffee Club" subscription plan:

| Tier Name | Billing Cycle | Discount |
|-----------|---------------|----------|
| Monthly | Monthly | 0% |
| Quarterly — Save 10% | Quarterly | 10% |
| Annual — Save 20% | Annual | 20% |

## Trial period

A trial period lets customers try your subscription before their first full charge. Configure this in the **Trial Period** section:

- **Trial Period (Days)** — Number of free trial days.

Set to `0` to disable trials.

最大で365日です。
- **トライアル価格** — トライアル中のみの割引価格（例: 初月は$1）。

完全無料トライアルにするには空のままにしておいてください。

## キャンセルポリシー

**キャンセルポリシー**セクションで、カスタマーが購読をキャンセルできる方法を制御してください:

| ポリシー | 説明 |
|--------|-------------|
| **いつでもキャンセル可能** | 顧客はいつでもすぐにキャンセルできます |
| **期間終了時にキャンセル** | キャンセルは支払い期間の終わりに適用されます — 顧客は有効期限までアクセスを保持します |
| **最低限のコミットメントが必要** | 顧客はキャンセルする前に最低限の請求サイクル数を完了する必要があります |

追加設定:

- **最低限のコミットメント（サイクル）** — コミットメントポリシーを使用する場合、必要な請求サイクル数を設定してください（例: 3か月の最低限は`3`）。
- **クーラーパーリー（日）** — 支払い失敗後の継続アクセス日数で、購読が一時停止されるまでに設定されます。即時停止には`0`を設定してください。
- **再活性化期間（日）** — キャンセル後、再登録せずに購読を再活性化できる期間です。

## プラン変更の動作

顧客がプラン間でアップグレードまたはダウングレードするとき、変更が適用されるタイミングを制御できます:

- **アップグレードの動作** — **即時**（比例分の金額を現在の支払いに請求）または **満了時**（次の支払い日時に切り替え）に設定してください。
- **ダウングレードの動作** — **即時**（次の請求にクレジットを適用）または **満了時**（次の支払い日時に切り替え）に設定してください。

## 制限と制約

- **最大請求サイクル数** — 購読が自動的に終了するまでの合計請求サイクル数です。無制限の繰り返し請求には空のままにしておいてください。分割払いプランや期間限定の購読に役立ちます。
- **セットアップ料金** — 購読が初めて作成されるときに一回限りの料金が徴収されます（例: オンボーディングまたはアクティベーション料金）。設定料金なしの場合は`0.00`を設定してください。

## プランのオプション

オプションは、購読者がプランに追加できるオプションです。

すべてのマーケドフォーマット、画像パス、コードブロック、技術用語を保持してください。

以下の**プランアドオン**セクションに追加してください：

- **アドオン名** — 顧客に表示される名前です。翻訳をサポートしています。
- **説明** — アドオンが提供するものです。
- **価格** — アドオンの料金です。
- **請求頻度** — アドオンが**請求サイクルごと**（継続的）に課金されるか、**一度限り**に課金されるかを示します。
- **数量の購入可能** — 顧客がアドオンの複数ユニットを購入できるようにするには有効にしてください。
- **必須** — 新しいすべてのサブスクリプションに自動的に含めるにはチェックを入れてください。必須アドオンは顧客によって削除することができません。

## 表示設定とステータス

- **有効** — 新しいサブスクリプションを作成できなくするためにプランを非表示にします。既存のサブスクリプションには影響しません。
- **公開** — 顧客向けページからプランを非表示にしたい場合はチェックを外してください（既存のサブスクライバーがいるための内部的または古参のプランに役立ちます）。
- **表示順** — サブスクリプション選択ページでの表示順序を制御します。小さい番号が最初に表示されます。

## トipp

- **無料体験期間**を設定して、不安を軽減してください — 7日間の無料体験でも、サブスクリプション製品のコンバージョン率を大幅に向上させることができます。
- **3段階の価格設定**（月額、四半期、年額）を設定し、年間契約を促すために割引率を増加させることで、キャッシュフローを改善してください。
- サービスベースのサブスクリプションの場合、**解約ポリシー**を**期間終了時に解約**に設定して、顧客が支払い期間中にアクセスを維持できるようにしてください。これは公平に感じられ、クレジットバックを減らします。
- 支払い失敗時の**猶予期間**は3〜7日間程度にしてください。アクセスを失う前に支払い方法を更新する時間を作ります。
- **必須**フラグはアドオンに対して控えめに使用してください。これは本当に必須なものです（例：サービス契約）にのみ使用し、価格を吊り上げるために使うのはやめましょう。
- 既存の購入者がいる場合は、削除ではなく非表示にしてプランを無効にしてください。これにより、以前にサブスクライバーだった顧客のために歴史的なデータが保持されます。