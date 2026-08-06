---
title: 購読プラン
---

購読プランを使用すると、製品に対して再発の請求を提供できます。消耗品、サービス、カスタムボックス、または顧客が繰り返し購入する製品に最適です。このガイドでは、プランの作成と構成、価格層の設定、トライアル期間の追加、オプションの追加機能の添付方法について説明します。

## はじめに

管理サイドバーの **サブスクリプション > サブスクリプションプラン** に移動してください。プラン一覧には、現在の価格モデル、アクティブな購入者数、表示状態が表示されます。

新しいプランを作成するには、**+ サブスクリプションプランを追加** ボタンをクリックしてください。これにより、セットアップの手順を順番に説明するプラン作成ウィザードが開きます。

![サブスクリプションプラン一覧](/static/core/admin/img/help/subscription-plans/plan-list.webp)

単独のプランでは購入できません。これはテンプレートです。ここに作成したものを、製品の **サブスクリプション** タブ（シンプル、変動、デジタル製品のみ）から1つ以上の製品に接続して、実際に購読できるようにしてください。そのステップについては、[製品をサブスクリプションとして販売する](/help/selling-products-as-subscriptions) を参照してください。

## プラン情報

最初のセクションでは、プランのコアなアイデンティティが収められます。

- **プラン名** — 顧客がサブスクライブするときに表示される名前です。他のストア言語用の翻訳を追加するには、地球のアイコンをクリックしてください。
- **スラッグ** — 名前から自動生成されたURLに最適な識別子（例: `premium-plan`）。これは内部で使用され、統合にも使用されます。
- **説明** — プランに含まれる内容を説明するオプションのテキスト。翻訳をサポートしています。

## 価格モデル

このプランの価格構造を選択してください:

| 価格モデル | 向いているもの |
|---------------|----------|
| **階層別価格** | 長期間の契約オプションを提供し、長期的な契約で割引を提供する |
| **数量ベース** | 1人当たりまたは1ユーザーあたりの価格で、総額が数量に応じて増加する（例: チームライセンス） |
| **フラットレート** | 変化のない単一の固定価格 |



For **Quantity-Based** plans, set the **Minimum Quantity** (minimum seats required) and optionally a **Maximum Quantity** to cap how many seats a subscriber can purchase.

## Pricing tiers

Pricing tiers define the billing frequency and discount options available to customers on this plan. Add them in the **Pricing Tiers** section below the main form.

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

- **Trial Period (Days)** — Number of free trial days. Set to `0` to disable trials. Maximum is 365 days.
- **Trial Price** — Optional reduced price during the trial (e.g., $1 for the first month). Leave empty for a completely free trial.

## Cancellation policy

Preserve all markdown formatting, image paths, code blocks, and technical terms.

購読のキャンセル方法を**キャンセルポリシー**セクションで制御します:

| ポリシー | 説明 |
|--------|-------------|
| **いつでもキャンセル可能** | 顧客はいつでも即座にキャンセルできます |
| **期間終了時にキャンセル** | キャンセルは支払い期間の終了時に適用されます。-- 顧客は有効期限までアクセスを保持します |
| **最低利用期間が必要** | 顧客はキャンセルする前に最低限の請求サイクル数を完了する必要があります |

追加設定:

- **最低利用期間（サイクル）** — 期間拘束ポリシーを使用する場合、必要な請求サイクル数（例: 3か月の最低期間の場合は`3`）を設定します。
- **クーラーパーリー（日）** — 支払い失敗後の継続アクセス日数を設定します。即時停止を希望する場合は`0`に設定してください。
- **再活性化期間（日）** — 顧客が再び購読を再開することができる期間を設定します。元の購入から再開する必要はありません。

## プラン変更の動作

顧客がプランをアップグレードまたはダウングレードする場合、変更が適用されるタイミングをコントロールできます:

- **アップグレードの動作** — **即時**（現在の比例分の料金を請求）または **満了時**（次の請求日時に切り替え）に設定します。
- **ダウングレードの動作** — **即時**（次の請求にクレジットを適用）または **満了時**（次の請求日時に切り替え）に設定します。

## 制限と制約

- **最大請求サイクル数** — 購読が自動的に終了するまでの合計請求サイクル数。無制限の繰り返し請求を希望する場合は空のままにしてください。分割払いプランや期間限定の購読に役立ちます。
- **登録料** — 購読が初めて作成されるときに従量課金される1回限りの料金（例: オンボーディングまたは有効化料）。登録料を設定したくない場合は`0.00`に設定してください。

## プランのオプション

オプションは、購読者が自分のプランに追加できるオプションです。**プランのオプション**セクションに追加します:

- **オプション名** — 顧客に表示される名前。

すべてのマーケドフォーマット、画像パス、コードブロック、技術用語を保持してください。

翻訳をサポートしています。
- **説明** — アドオンが提供するものです。
- **価格** — アドオンの料金です。
- **支払い頻度** — アドオンが**請求サイクルごと**（継続的）に課金されるか、**一度限り**に課金されるかを示します。
- **数量の許可** — 顧客がアドオンの複数ユニットを購入できるようにします。
- **必須** — 新しいサブスクリプションすべてに自動的にアドオンを含めるためにチェックを入れてください。

必須アドオンは顧客によって削除することができません。

## 一時表示とステータス
- **有効** — 新しいサブスクリプションを作成できなくなるように、プランを非アクティブにします。既存のサブスクリプションには影響しません。
- **公開** — 顧客向けページからプランを非表示にします（既存のサブスクライバーがいるための内部的または古くなったプランに役立ちます）。
- **ソート順** — サブスクリプション選択ページでの表示順序を制御します。小さい番号が最初に表示されます。

## トゥイク
- **無料体験期間** を設定して、不安を軽減してください — 7日間の無料体験でも、サブスクリプション製品のコンバージョン率を大幅に向上させることができます。
- **3段階の価格設定**（月額、四半期、年額）を設定し、年間契約を促すために割引率を増して、キャッシュフローを向上させましょう。
- サービスベースのサブスクリプションの場合、**解約ポリシー**を**期間終了時に解約**に設定て、顧客が支払い期間中にアクセスを維持できるようにしてください。これは公平に感じられ、チャージバックを減らします。
- 支払い失敗時の**猶予期間**は3〜7日間にしてください。アクセスを失う前に顧客が支払い方法を更新する時間を持たせます。
- アドオンの**必須**フラグは使用するたびに控えめにしてください。これは本当に必須なものです（たとえば、サービス契約）にのみ使用し、価格を吊り上げるために使うのはやめましょう。
- 削除ではなく非アクティブ化することを推奨します — これにより、以前にサブスクライブしていた顧客のための歴史的なデータが保持されます。