---
title: AI购物
---

AI购物让AI购物助手找到你的产品，并在你允许的情况下，代表客户从你的商店购买。默认是关闭的——开启它是一个有意的选择，直到你开启之前，你的商店不会向这些助手暴露任何内容。

## 如何开启

打开 **设置 → AI购物** 并开启 **代理购物功能**。从那时起，支持通用购物协议的助手可以发现你的商店并查看你的目录。你正常的商店界面不会发生任何变化。

## 准备就绪仪表板

AI购物页面顶部用一句话回答一个问题：**AI助手现在真的能从你的商店购买吗？**

- **"AI助手可以从你的商店购买"** —— 购买所需的一切都已就绪。
- **"AI助手可以浏览你的商店，但还不能购买"** —— 你的商店可以被发现，但在购买完成之前有些东西缺失（通常是连接的支付提供商）。
- **"紧急停止已开启"** 或 **"代理购物功能已关闭"** —— 没有任何内容被提供给助手。

在判断结果下方你会看到一个简短的检查清单——支付提供商已连接，可以提供运费报价，产品对助手可见——任何仍需关注的内容旁边都有提示。计数器显示助手可以销售多少产品，你隐藏了多少给他们，有多少助手访问过，以及你阻止了多少。

检查清单反映你的 **实时** 设置：连接支付提供商或添加运输方式后，下次打开页面时判断结果会更新。

## 紧急停止

**紧急停止** 是一个与主开关分开的开关。在出现问题时，可以立即停止所有助手活动——例如如果看起来有问题——而无需更改你的配置。清除它以恢复。将主开关视为“此功能是否已配置”，而紧急停止视为“立即停止一切”。

## 助手能做什么

Two levels of access, controlled separately:

- **Reading** (discovery and browsing) is lower-risk. An assistant can find your store and read product details.
- **Checkout** (actually buying) is higher-stakes and stays closed to unverified assistants unless you allow it.

A store can be discoverable without being purchasable — a useful way to start.

## Hiding specific products

Every product has a **Visible to AI shopping agents** setting (on by default). Switch it off to keep a particular product off assistants while it stays on your storefront — handy for items you'd rather sell only through your own site.

## Managing individual assistants

When an assistant first buys — or tries to — Spwig records it under **AI Shopping → Agent Identities**. Each entry shows the assistant's verified home (the directory it signs with), its trust level, and how many requests it has made. The name and logo an assistant presents are shown only as *claimed* details — treat them as a label, not proof of identity; the verified home is the part that can be trusted.

Every assistant sits in one of three trust levels:

| Trust level | What it means |
|---|---|
| **Capped (verified, limited)** | The default for a new assistant. Spwig has recorded its identity, and it carries the order-value cap, spend cap, and tender restrictions set on its policy (see below). |
| **Verified (limits removed)** | A deliberate decision by you to trust this assistant fully. Its order-value and daily spend caps are cleared. |
| **Blocked** | The assistant can no longer buy from your store. Open checkouts end, though any payment already taken is left untouched. |

To stop an assistant, select it in the list and choose **Block selected assistants**. **Unblock selected assistants** always returns it to **Capped** — never straight to Verified — because lifting limits is a separate, deliberate step.

To lift an assistant's limits entirely, select it and choose **Promote to verified (remove limits)**.

This clears its max order value and daily spend cap and moves the assistant to the Verified state.

A blocked assistant is skipped — unblock it first, then promote it.

Treat this as a real trust decision: only promote an assistant you're confident about, since verification removes the guardrails a new assistant starts with.

## Setting an assistant's limits

Open an assistant's detail page and use the **Policy (limits & allowed tenders)** section to set what it's allowed to do:

| Field | What it controls |
|---|---|
| **Max order value** | The largest single order this assistant can place. Leave blank for no cap. |
| **Daily spend cap** | The most this assistant can spend across all orders in a day. Leave blank for no cap. |
| **Allow discount codes** | Whether the assistant can apply voucher codes at checkout. |
| **Allow gift cards** | Whether the assistant can redeem gift cards. |
| **Allow digital goods** | Whether the assistant can buy digital products. |
| **Rate limit (per minute)** | How many requests the assistant can make to your store per minute. |

A new assistant starts capped with concrete order-value and spend caps, and with discount codes, gift cards, and digital goods switched off — the deliberately conservative default. Change any of these fields and save; every change is written to **Agent Events** with the before and after values, so you always have a record of who changed what, and when. Promoting an assistant to Verified clears its Max order value and Daily spend cap for you — you don't need to blank them out by hand first.

## The activity record

**AI Shopping → Agent Events** is a tamper-evident record of what assistants did — every verified request, every blocked attempt, every change you made. It is view-only and cannot be edited or deleted, so it stands as your evidence trail if a purchase an assistant made is ever disputed.

## A note on the assistant platforms

Preserve all markdown formatting, image paths, code blocks, and technical terms.

这些助手的运营公司（以及在其中出现的规则）是新的，经常发生变化。

有些助手要求您在产品可通过它们购买之前先申请或满足地区条件。

Spwig 会将您的店铺准备好；是否列出您取决于该助手。
