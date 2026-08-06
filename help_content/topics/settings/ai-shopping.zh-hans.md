---
title: AI购物
---

AI购物允许AI购物助手找到您的产品，并在您允许的情况下，代表客户从您的商店购买商品。默认情况下，它是**关闭的**——开启它是有意为之的选择，直到您开启，您的商店不会向这些助手暴露任何内容。

## 启用功能

打开**设置 → AI购物**，并将**启用代理式商业**切换为开启状态。从那时起，支持通用商业协议的助手可以发现您的商店并阅读您的商品目录。您的正常商店前端不会有任何变化。

## 准备状态仪表板

AI购物页面顶部用一句话回答了一个问题：**目前AI助手是否真的可以从您的商店购买商品？**

- **"AI助手可以从您的商店购买"** — 所有购买所需的内容都已就绪。
- **"AI助手可以浏览您的商店，但还不能购买"** — 您的商店可以被发现，但在完成购买之前还缺少某些内容（通常是连接的支付提供商）。
- **"紧急停止已启用"** 或 **"代理式商业已关闭"** — 没有任何内容提供给助手。

在判断结果下方，您会看到一个简短的检查清单——已连接支付提供商、可以报价运输、产品对助手可见——任何仍需关注的项目旁边都有提示。计数器显示助手可以销售的产品数量、您隐藏的产品数量、已访问的助手数量以及您阻止的助手数量。

检查清单反映的是您的**实时**配置：连接支付提供商或添加运输方式后，下次打开页面时判断结果会更新。

## 紧急停止

**紧急停止**是与主开关分开的独立开关。使用它立即停止所有助手活动——例如，当您发现某些异常时——而无需更改您的配置。清除它以恢复。可以将主开关视为"此功能是否已配置"，而紧急停止则视为"立即停止所有操作"。

## 助手可以执行的操作

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

Spwig 使您的商店做好准备；某个助手是否将您列入名单，取决于该助手。