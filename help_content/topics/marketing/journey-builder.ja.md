---
title: Journey Builder
---

<!-- screenshots-needed:
- url: /admin/campaigns/journeys/  (open any journey's builder, click Templates)
  filename: journey-builder-templates.webp
  description: The template picker with all eight starters visible (Welcome series,
    First-order onboarding, Post-purchase & review, VIP vs. standard offer, Abandoned
    cart recovery, Win-back lapsed customers, Post-delivery review request,
    Back-in-stock alert) — replaces the existing four-template screenshot at the same
    path, which is now stale.
  save-to: core/static/core/admin/img/help/journey-builder/
  viewport: 1440x900
-->

**Journey Builder** は、[Journey](/help/triggered-journeys) が実際に何を行うかを設計するための、ビジュアルなドラッグ＆ドロップキャンバスです。どのメールを送信するか、メール間の待機時間はどれくらいにするか、異なる購読者が異なるパスをたどるべきかどうかを定義します。フォームに記入するのではなく、フローチャートとしてフローを構築します。キャンバス上の接続されたボックスを並べ替え、分岐し、一目でプレビューできます。

## ビルダーを開く

各 Journey には独自のビルダーキャンバスがあります。2 つの方法でアクセスできます。

- 新しい Journey を作成する — 設定ページで **Name**、**Trigger**、対象オーディエンスを入力し、**Save** をクリックすると、すぐに設計を開始できるようビルダーに直接移動します。
- 既存の Journey の設定ページを開き、上部の **Design journey** をクリックする。

ビルダーは、左側にステップタイプの **palette**、中央に **canvas**、選択した項目が表示された際に右側に **step settings** パネルが表示される、フルスクリーンのワークスペースです。

![Yes/No 分岐を含むウェルカムシリーズを示す Journey Builder キャンバス](/static/core/admin/img/help/journey-builder/journey-builder-canvas.webp)

キャンバスの上部には、Journey の **Trigger** と **audience**（セグメントが設定されていない場合は「All subscribers」）が繰り返し表示されるヘッダーがあり、ビルダーを離れることなく、常に誰を対象に設計しているかを確認できます。

「**戻る**」ボタンを使用して、ジャーニーの設定ページに戻ります。

## ステップの種類

左側のパレットからステップをキャンバスにドラッグするか、パレットの項目をクリックして自動的に配置します。利用可能なステップの種類は4つです：

| ステップ | 機能 |
|------|--------------|
| **メール送信** | サブスクライバーにキャンペーンの1つを送信します。 |
| **待機** | 一定の時間または日数だけ停止してから続行します。 |
| **分岐** | 選択したセグメントにサブスクライバーが属しているかどうかに基づいて、パスを**はい**または**いいえ**の2つに分岐します。 |
| **終了** | サブスクライバーのジャーニーを終了します。 |

すべてのジャーニーは、ビルダーを初めて開いたときに自動的に作成される単一の**エントリー**ステップから始まります。ジャーニーのトリガーを表示し、削除することはできません。これは単に、サブスクライバーがフローに入る場所です。

## ステップの接続

各ステップには小さな円形の**ポート**があります：上部に1つ（入力）、下部に1つ以上（出力）。2つのステップを接続するには、1つのステップの下部ポートから別のステップの上部ポートへドラッグします。それらを結ぶ曲線が表示されます。

**分岐**ステップには、1つの代わりに2つの出力ポートがあります：緑色の**はい**と赤色の**いいえ**。それぞれのパスが向かうべき場所に接続します。後で同じステップで再結合させることも（上記の例では、両方のパスが同じ**終了**に戻っています）、完全に別々の方向に進ませることもできます。

レイアウトを再配置するには、ステップの本体をドラッグして位置を移動します。接続された線は自動的に追従します。キャンバスの背景の空の部分をドラッグしてパンし、スクロールホイールを使用してズームインまたはズームアウトします。フローの追跡を失った場合は、ツールバーの**フィット**をクリックして、すべてを画面に収めるように再中心合わせとズームを実行します。

## ステップの設定

任意のステップをクリックすると、右側のパネルでその設定が開きます：

| ステップ | 設定 |
|------|---------|
| **メール送信** | キャンペーンの一覧から、**送信するメール** をドロップダウンで選択します。 |
| **待機** | **待機時間** を設定します — 数値と **時間** または **日** を指定します。 |
| **分岐** | **サブスクライバーがセグメントに属する場合** を選択します — はい/いいえを決定するセグメントです。 |
| **終了** | 設定はありません — 単なるエンドポイントです。 |

![分岐ステップを設定する右側のパネル、背景のキャンバスは暗く表示されています](/static/core/admin/img/help/journey-builder/journey-builder-branch-config.webp)

値を選択するとすぐに自動的に保存されます — キャンバスには個別の **保存** ボタンはありません。 **開始** 以外のすべてのステップには、設定パネルの下部に **ステップを削除** ボタンがあります。

**メール送信** ステップで選択するメールは、Campaign Studio の通常のビジュアルビルダーで設計する通常のキャンペーンです — 件名、コンテンツブロック、すべてです。それらを **下書き** のままにし、ここでドロップダウンから選択するだけです。ジャーニーが代わりに送信しますので、自分で送信をクリックする必要はありません。

## テンプレートから開始

空白のキャンバスからフローを構築する必要があるとは限りません — ツールバーの **テンプレート**（または空のキャンバス上の **テンプレートを参照**）をクリックして、8つの完成済みスターターを含むピッカーを開きます：

{"| Template | What it builds |\n|----------|-----------------|\n| **Welcome series** | Greet new subscribers, share what you're about, then a first-order nudge. |\n| **First-order onboarding** | Turn a first-time buyer into a repeat customer with a gentle onboarding sequence. |\n| **Post-purchase & review** | Say thanks after any order, then ask for a review once it's arrived. |\n| **VIP vs. standard offer** | After an order, branches on your VIP segment to send the right follow-up offer to each group. |\n| **Abandoned cart recovery** | Remind a shopper who left items behind, then a follow-up nudge a day later. |\n| **Win-back lapsed customers** | Re-engage a customer who hasn't bought in a while with a reason to return. |\n| **Post-delivery review request** | Ask for a review a few days after an order is marked Delivered. |\n| **Back-in-stock alert** | Tell a waiting shopper the moment a product they wanted is available again. |\n|\nEach template is pre-wired to the matching trigger — for example, applying **Win-back lapsed customers** to a new journey also expects that journey's **Trigger** to be **Customer lapsed (win-back)**. See [Triggered journeys](/help/triggered-journeys) for what fires each of these trigger events and how the recovery-focused ones behave (idle windows, guest checkout, once-per-order review requests, and how a back-in-stock journey takes over from the plain one-off alert).|n|n![The template picker showing the ready-made starter journeys](/static/core/admin/img/help/journey-builder/journey-builder-templates.webp)|n|nApplying a template **replaces the current flow** on the canvas, so use it at the start of designing a journey rather than partway through. Spwig re-links each step to a real email or segment wherever the names match something you already have; anywhere it can't find a match, the header reports how many steps still need an email or segment chosen so you know exactly what to finish before going live.|n|n## Sharing journeys|n|nPreserve all markdown formatting, image paths, code blocks, and technical terms."}

移動するジャーニーのデザインをステップ間やストア間で操作するためのツールバーのボタンが2つあります:

- **エクスポート** は、ジャーニーを `.journey.json` ファイルとしてダウンロードします。これは、フローの形状（ステップ、ウェイト、分岐、Yes/Noパス）に加え、各ステップで使用するメールとセグメントの*名前*を示すポータブルな記述です。メールのデザインそのものは含まず、購読者のデータも含みません。
- **インポート** は、現在のジャーニーに `.journey.json` ファイルを読み込み、キャンバス上のものを置き換えます。

これは、自信のあるフローをバックアップするのにも役立ち、認証されたウェルカムシリーズを他の Spwig ストアに渡すのにも役立ち、新しいインストールにストアをクローンした後のジャーニーを再構築するのにも役立ちます。テンプレートと同様に、Spwig はターゲットストアで一致する名前がある場合、メールやセグメントを名前で再リンクし、一致しなかったものはフラグが立てば、設定を完了できるようにします。

## ジャーニーの有効化

フローが準備できたら、ビルダーの右上にあるステータスコントロールを使用してください。ポストイットのような表示が、ジャーニーの現在のステータス（**下書き**、**有効**、または**一時停止**）を示し、**有効化**ボタンが表示されます。

**有効化**をクリックすると、**まずフローをチェックします**。動作を妨げるものが何かあると、有効化はブロックされ、バナーに問題がリストされます。たとえば、**メールの送信**ステップでメールが選択されていない、**分岐**でセグメントが選択されていない、またはYes/Noパスが設定されていない、以降に削除されたメールまたはセグメント、無限ループになる可能性があるなどです。各問題はクリック可能で、問題のあるステップにジャンプします。問題のあるステップは赤で囲まれ、修正するまでそのままです。警告（たとえば、到達不能なステップや、遅延が設定されていない**待機**など）も一覧表示されますが、有効化をブロックすることはありません。

![有効化がブロックされ、問題がバナーに表示され、問題のあるステップが赤で囲まれています](/static/core/admin/img/help/journey-builder/journey-builder-activate-blocked.webp)

フローが正常に動作すれば、ポストイットが**有効**に変わり、トリガーが作動するたびに購読者が登録されます。

ボタンは**一時停止**に変わり、新しい登録を停止します — すでに進行中のサブスクライバーは、残りのステップを受け取り続けます。

登録、クールダウン、ステータスの相互作用については、[トリガー型ジャーニー](/help/triggered-journeys)を参照してください。

## ジャーニーに参加している人の確認

ジャーニーが公開されると、各ステップの隅に小さな**カウントバッジ**が表示されます。これは、現在そのステップに留まっているサブスクライバーの数です。人々がどこに流れ、どこに滞留しているかを素早く把握する便利な方法です。**待機**ステップに大きな数字が表示されるのは想定内ですが、特定のメール直前に滞留が起きている場合は、確認する価値があります。カウントは、ビルダータブに戻った際に更新されます。

![ステップにライブカウントバッジが表示され、ツールバーにアクティベートボタンがあるキャンバス](/static/core/admin/img/help/journey-builder/journey-builder-live-counts.webp)

## ヒント

- フローを**下書き**の段階で設計してください — **アクティベート**するまで誰も登録されません。ビルダーからアクティベートすると、まず簡単なチェックが実行され、壊れたフローが公開されることはないので、未完成のジャーニーでサブスクライバーが登録されるリスクはありません。
- 大幅にカスタマイズする予定があっても、**テンプレート**から始めてください — 既存のフローを編集する方が、ノードを1つずつ構築するよりも速く、以前に使用したことがなくても分岐パターンを示してくれます。
- テンプレートを適用したりファイルをインポートしたりした後、ヘッダーに未一致ステップの通知があるか確認し、アクティベートする前に一致しなかった**メール送信**または**分岐**ステップを埋めてください。
- フローが広くなった場合（特に分岐がある場合）、**フィット**をクリックしてください — ズームやパンの後に全体の形状を再び確認する最速の方法です。
- 各**待機**ステップを、遅延させるメールの直前に配置し、複数の待機をまとめて配置しないようにすることで、ステップ名をスキャンしやすく保ってください。
- 大きな変更を加える前に、動作しているジャーニーを**エクスポート**してください — 結果に満足しなかった場合に再インポートできるフォールバックコピーを素早く保持する方法です。