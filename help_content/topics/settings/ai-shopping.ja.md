---
title: AIショッピング
---

AIショッピングは、AIショッピングアシスタントが商品を検索し、許可された場合、顧客の代わりにあなたのストアから購入できるようにします。これは**デフォルトでオフ**です — これを有効にするのは意図的な選択であり、それを行うまでは、あなたのストアはこれらのアシスタントに対して何も公開しません。

## 有効にする

**設定 → AIショッピング**を開き、**Agentic commerce enabled**をオンに切り替えます。この時点で、Universal Commerce Protocolをサポートするアシスタントは、あなたのストアを発見し、カタログを読み取ることができます。通常のストアフロントに変更はありません。

## 準備状態ダッシュボード

AIショッピングページの上部は、1つの質問に1つの文で答えます：**今すぐAIアシスタントは実際にあなたのストアから購入できますか？**

- **"AIアシスタントはあなたのストアから購入できます"** — 購入に必要なすべてのものが整っています。
- **"AIアシスタントはあなたのストアを閲覧できますが、まだ購入することはできません"** — ストアは検出可能ですが、購入を完了する前に何かが不足しています（通常は接続された支払いプロバイダー）。
- **"緊急停止がオン"** または **"Agentic commerceがオフ"** — アシスタントに対して何も提供されていません。

判断の下に、短いチェックリストが表示されます — 支払いプロバイダーが接続されている、送料が提示可能、商品がアシスタントに表示されている — 何かがまだ注意が必要な場合は、それにヒントが表示されます。カウンターは、アシスタントが販売できる商品の数、アシスタントから隠された商品の数、アシスタントが訪れた回数、ブロックした回数を示します。

チェックリストは**ライブ**設定を反映しています：支払いプロバイダーを接続したり、配送方法を追加したりすると、ページを開いた次のタイミングで判断が更新されます。

## 緊急停止

**緊急停止**は、メインのスイッチとは別個のスイッチです。何か問題が起きたように見える場合、構成を解除せずにすべてのアシスタントの活動を**即座に停止**するために使用します。停止を解除して再開します。メインスイッチを「この機能が構成されているか」、緊急停止を「今すぐすべてを停止する」ように考えるとよいでしょう。

## アシスタントが行えること

Two levels of access, controlled separately:

- **Reading** (discovery and browsing) is lower-risk. An assistant can find your store and read product details.
- **Checkout** (actually buying) is higher-stakes and stays closed to unverified assistants unless you allow it.

A store can be discoverable without being purchasable — a useful way to start.

## Hiding specific products

Every product has a **Visible to AI shopping agents** setting (on by default). Switch it off to keep a particular product off assistants while it stays on your storefront — handy for items you'd rather sell only through your own site.

## Managing individual assistants

When an assistant first buys — or tries to — Spwig records it under **AI Shopping → Agent Identities**. Each entry shows the assistant's verified home (the directory it signs with) and how many requests it has made. The name and logo an assistant presents are shown only as *claimed* details — treat them as a label, not proof of identity; the verified home is the part that can be trusted.

New assistants start **capped**: they can transact, but within limits. To stop one, select it and choose **Block selected assistants** — open checkouts end and the assistant can no longer buy, while any payment already taken is left untouched. **Unblock selected assistants** returns it to the capped state (never straight to unlimited — lifting limits is always a separate, deliberate step).

## The activity record

**AI Shopping → Agent Events** is a tamper-evident record of what assistants did — every verified request, every blocked attempt, every change you made. It is view-only and cannot be edited or deleted, so it stands as your evidence trail if a purchase an assistant made is ever disputed.

## A note on the assistant platforms

The companies running these assistants (and the rules for appearing in them) are new and change often.

Some require you to apply or meet regional conditions before your products can be bought through them.

Spwigは、あなたのストアを準備します。特定のアシスタントがあなたをリストするかどうかは、そのアシスタント次第です。