---
title: AI購物
---

AI購物讓AI購物助手能夠找到您的產品，並在您允許的情況下，代表客戶從您的商店進行購買。預設情況下，此功能是**關閉的** — 啟用它是一個有意的選擇，直到您啟用為止，您的商店不會向這些助手暴露任何內容。

## 啟用功能

打開 **設定 → AI購物**，並將 **啟用代理式商務** 開關打開。從此之後，支援通用商務協議的助手可以發現您的商店並讀取您的目錄。您正常的商店前端不會有任何變化。

## 準備狀態儀表板

AI購物頁面頂部以一句話回答了一個問題：**目前AI助手實際上能否從您的商店購買商品？**

- **"AI助手可以從您的商店購買"** — 所有購買所需的條件都已具備。
- **"AI助手可以瀏覽您的商店，但還不能購買"** — 您的商店可以被發現，但在完成購買之前還缺少某些東西（通常是連接的支付提供商）。
- **"緊急停止已啟用"** 或 **"代理式商務已關閉"** — 沒有任何內容提供給助手。

在評估結果下方，您會看到一個簡短的檢查清單 — 支付提供商已連接、可以報價運費、產品對助手可見 — 並在任何仍需關注的項目旁邊提供提示。計數器顯示助手可以銷售的產品數量、您隱藏的產品數量、已訪問的助手數量以及您阻止的助手數量。

檢查清單反映的是您的**即時**設定：連接支付提供商或新增運費方式後，評估結果會在您下次打開頁面時更新。

## 緊急停止

**緊急停止** 是一個與主開關分離的開關。使用它立即停止所有助手活動 — 例如，當發現某些異常時 — 而無需取消您的設定。清除它即可恢復。將主開關視為 "此功能是否已配置"，而緊急停止則視為 "立即停止所有操作"。

## 助手可以執行的操作

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

Spwig 會讓您的商店準備好；某個助手是否列出您，取決於該助手。