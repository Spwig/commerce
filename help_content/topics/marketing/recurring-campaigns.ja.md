---
title: 定期キャンペーン
---

Campaign Studio の **定期キャンペーン** を使用すると、ニュースレターを一度設定するだけで（例：毎週の商品まとめ、毎月のブログダイジェスト）、毎回手動で新しいキャンペーンを作成・送信する代わりに、Spwig が繰り返しスケジュールに基づいて自動的に送信してくれます。

## 一斉送信と定期送信

Campaign Studio のすべてのキャンペーンには **キャンペーンタイプ** があります：

| タイプ | 動作 |
|------|-----------|
| **一斉送信** | 一度だけ送信されます — 即時、または単一のスケジュールされた日時で。これは、一回限りの告知、セール、または商品ローンチのメールに使用します。 |
| **定期** | 繰り返しスケジュールで送信されるテンプレートとして機能します。各送信は、**発生（occurrence）** と呼ばれる新しい日付付きのコピーです — テンプレート自体は直接「送信」されることはありません。 |

キャンペーンを定期キャンペーンに変更するには、**Campaign Studio > Campaigns** でキャンペーンを開き、**キャンペーンタイプ** を **定期** に設定して保存してください。キャンペーンを再度開くと、**スケジュール** セクションが表示されます — これは定期キャンペーンでのみ表示されます。

![キャンペーンタイプが定期に設定されている](/static/core/admin/img/help/recurring-campaigns/campaign-type-selector.webp)

## スケジュールの設定

キャンペーンが定期になると、その **スケジュール** セクションが送信タイミングを制御します：

| フィールド | 説明 |
|-------|-------------|
| **有効** | スケジュールを削除せずに、繰り返しをオンまたはオフにします。 |
| **頻度** | **毎日**、**毎週**、または **毎月**。 |
| **間隔** | N 単位の頻度ごとに送信 — 例：頻度が **毎週** で間隔が `2` の場合、2 週間ごとに送信されます。 |
| **曜日** | 毎週の頻度で送信する曜日（`0` = 月曜日 … `6` = 日曜日）。 |
| **日付** | 毎月の頻度で送信する日（`1`–`28`、すべての月にその日があるように）。 |
| **送信時刻** | キャンペーンが送信される時刻。 |
| **タイムゾーン** | IANA タイムゾーン名、例：`Europe/London` または `America/New_York` — 送信時刻はこのゾーンで解釈され、サーバーのゾーンではありません。 |

![定期キャンペーンの週間スケジュールセクション](/static/core/admin/img/help/recurring-campaigns/schedule-section.webp)

アクティブなスケジュールを保存すると、すぐに**アーム（待機状態）**になります — Spwig は次の発火時刻を計算し、**次回実行時刻**に表示します。手動でトリガーする必要はありません。バックグラウンドタスクが期限が来たスケジュールをチェックし、時刻が来たら発生を送信します。**最終実行時刻**と**送信済み発生数**は、各送信後に自動的に更新されるため、スケジュールが稼働していることを確認できます。

## 新規コンテンツなしポリシー

定期ニュースレターには動的なコンテンツが頻繁に使用されます — 最も一般的なのは、ビジュアルビルダーで**新規送信以降**に設定された**ブログ記事**ブロック（または**商品グリッド**）です。これにより、キャンペーンの前の送信以降に公開された記事 — または追加された商品 — だけが取り込まれます。これにより、明らかな疑問が生じます：スケジュールされた実行が到着したが、フィーチャーする新しいコンテンツがない場合はどうなるのか？

Spwig は、スケジュールの**新規コンテンツなしポリシー**でこれに答えます：

| ポリシー | 何が起こる | 向いているのは | 
|--------|---------------|----------| 
| **この送信をスキップ** *(デフォルト)* | このイベントは完全にスキップされます。-- 何も送信されません。スケジュールはその次の予定された実行に直接進みます。 | 読者にすでに見たことのあるメールを繰り返し送らないようにする、ブログや製品のダイジェスト向けです。 | 
| **いつでも送信する（空のブロックは無視）** | 予定どおりのタイミングでメールが送信されます。「最後の送信から新規」ブログ投稿ブロックのような新しいものが何もなければ、その場所に何も表示されません。 | 1つのブロックが空でも、他のコンテンツ（ウェルカムメッセージ、エバーグリーンセクション、いくつかのダイナミックブロックなど）があるニュースレター向けです。 | 
| **遅延して送信する** | 送信が遅れます。Spwigは、**ホールドウィンドウ（日）** まで、1日1回新しいコンテンツがあるか確認します。そのウィンドウ内で新しいコンテンツが表示されれば、遅れて送信されます。ウィンドウが経過しても新しいコンテンツがなければ、そのイベントは諦め、スケジュールは次のスロットに進みます。 | 週に1回のペースで、新しいコンテンツがない場合でも、何かは送りたいというニーズがあります。 | 
| 
| これ以上のチェックは、**デルタアンサー**コンテンツ（ブログ投稿ブロックや「最後の送信から新規」に設定された製品グリッド）を使用しているキャンペーンにのみ適用されます。**デルタアンサー**コンテンツを持っていない繰り返しキャンペーンは、常に新しいコンテンツがあると見なし、予定どおりスケジュールされます。 | 
| 
| **ホールドウィンドウ（日）** は **「遅延して送信する」** ポリシーにのみ適用され、そのオカズに対して何日間リトライするかを設定します。 | 
| 
## それぞれのオカズでA/Bテストする | 
| 再発行ニュースレターは、**件名**のA/Bテストに最適な場所です。同じオーディエンスに定期的に送信するため、どの表現がより多くの開封をもたらすかを学び続けることができます。Spwigは、**すべてのオカズ**で新しい件名のA/Bテストを自動的に行うことができます。 | 
| 
| **スケジュール**セクションで設定してください： | 
| 1. | 
| 
| マークダウンフォーマット、画像パス、コードブロック、技術用語を保持してください。

In **A/B subject lines**, enter **two to four** subject lines, one per line.

Leave it blank to send occurrences normally with the template's own subject.
2.

Set the **A/B test sample %** — the share of each occurrence's audience used to test, split evenly across the subjects.

The rest is the holdout that receives the winner.
3.

Choose the **A/B winner metric** (open or click rate), the **A/B test window (hours)** to gather results before deciding, and whether to **auto-send the winner** to the holdout.

From then on, each time the schedule fires, that occurrence splits its audience, sends each subject line to a slice, waits out the test window, then picks the winning subject and sends it to everyone else — with no further action from you. Each occurrence is its own self-contained test, so you get a fresh read every send and can watch which subjects win over the weeks. Each occurrence's result shows up under **Occurrence history** below, linking straight to its results page with the per-variant rates, the winner, and how confident Spwig is (see [A/B Testing](ab-testing) for how to read those results).

Two things worth knowing:

- **A/B testing here is subject-line only.** To compare entirely different designs, use a one-off broadcast A/B test — the full wizard, which supports content variants, is for broadcast campaigns.
- If an occurrence's audience is ever **too small to split** across the variants, Spwig quietly sends that occurrence as a normal newsletter instead — a lean week never means a missed send.

## Occurrence history

Every time a recurring campaign actually sends, Spwig creates a dated **occurrence** — a real, independent campaign record with its own subject, recipients, and send statistics (sent, failed, skipped, opens, clicks). The occurrence is named after the template with the send date appended, e.g. "Weekly Blog Digest — 2026-08-19".


定期キャンペーンの編集ページには、**発生履歴** が一覧表示されます。これは最近の発生分であり、各発生分は該当するキャンペーンレコードにリンクしているため、正確に何が送信され、どのようにパフォーマンスがであったかをレビューできます。

![定期キャンペーンの発生履歴一覧](/static/core/admin/img/help/recurring-campaigns/occurrence-history.webp)

## ヒント

- 定期キャンペーンに、**ブログ記事** ブロックを **前回送信以降の新規** に設定して組み合わせることで、自己維持型の「今週の新しい記事」ダイジェストを作成できます。あなたは記事を書くだけで、Spwig がメール送信を処理します。
- コンテンツダイジェストでは、**この送信をスキップ** から始めることをお勧めします。これが最も安全なデフォルト設定です。購読者は、前回のコンテンツの繰り返しを受け取ることはありません。
- ダイナミックブロックが空の場合でも、テンプレート自体に送信する価値のある他のコンテンツがある場合のみ、**それでも送信する** に切り替えてください。
- 間隔の1回程度の遅れは許容できるが、数週間連続で遅れるのは許容できない場合は、**保留して遅れて送信** を使用してください。保留ウィンドウは、許容できるギャップの長さに合わせて設定してください。
- スケジュールを保存した後、**次回実行時刻** を確認し、特にタイムゾーンをまたいで作業している場合、期待した日付と時刻に設定されたことを確認してください。
- **発生履歴** を定期的にレビューしてください。テンプレートが繰り返しスキップされるのは、ダイナミックコンテンツソース（例：ブログ）が静かになった（更新が止まった）ことを示す兆候です。 