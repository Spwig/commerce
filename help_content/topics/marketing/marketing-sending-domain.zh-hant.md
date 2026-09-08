---
title: 行銷發送網域
---

您的商店會發送兩種截然不同的電子郵件：

- **交易性郵件** — 訂單確認、出貨通知、密碼重設。這些郵件必須總是送達收件匣。
- **行銷郵件** — 電子報、促銷活動、購物車挽回、補貨提醒。

預設情況下，兩者都使用相同的發送身分，這意味著它們**共享同一個發送者聲譽**。如果行銷活動引發垃圾郵件投訴或寄送到失效地址，該聲譽就會下降——您的訂單確認和密碼重設郵件也可能開始進入垃圾郵件資料夾。

**行銷發送網域**可以解決這個問題。您設定第二個發送身分——在專屬的子網域上，例如 `news.yourstore.com`——並將其標記為行銷用途。Spwig 會從該身分發送所有行銷活動，並讓交易性郵件繼續使用您的主要網域。這樣，效果不佳的行銷活動就不會再拖累客戶*必須*收到的郵件。

> 這適用於自架商店。在 Spwig 託管方案中，發送聲譽由我們為您管理。

## Spwig 如何決定使用哪個身分

一旦建立了行銷發送帳戶，路由即為自動——您不需要標記任何內容：

- **行銷郵件**（行銷活動、旅程、電子報、購物車挽回、補貨提醒）→
  行銷發送網域。
- **交易性郵件**（訂單、出貨、密碼重設、驗證）→ 您的主要
  網域。

如果您從未設定行銷網域，則一切不變：所有郵件仍會從您的預設帳戶發送，與之前完全相同。

## 設定步驟

您可以從以下任一入口開始：

- 行銷活動工作室儀表板橫幅上的**「設定行銷網域」**按鈕，或
- **電子郵件帳戶 →「行銷發送網域」**。

![行銷活動工作室儀表板，顯示「保護您的交易性郵件」橫幅及其設定行銷網域按鈕](/static/core/admin/img/help/marketing-sending-domain/marketing-domain-nudge.webp)

[![The Marketing sending domain button on the Email Accounts list, next to Browse Providers](/static/core/admin/img/help/marketing-sending-domain/marketing-domain-button.webp)](https://spwig.com)

Both open the email setup wizard pre-flagged for a marketing account. Then:

1. **Choose a subdomain.** Use something like `news.yourstore.com` or
   `mail.yourstore.com`. This is the most important step: the marketing identity must be a
   **different (sub)domain** from the one your transactional email uses — that separation
   is exactly what protects your transactional reputation. Sending marketing from your
   main domain gives you no isolation.
2. **Enter the sender address** on that subdomain, e.g. `news@news.yourstore.com`.
3. **Add the DNS records.** The wizard generates SPF, DKIM, and DMARC records for the
   subdomain — including a DKIM key that is unique to this marketing identity. Add them at
   your DNS provider (the wizard has copy buttons and per-provider tabs), then run the
   check until all records pass.
4. **Finish.** The account is created and marked **Marketing only**. From now on your
   campaigns send from it.

You can confirm it worked on the **Email Accounts** list: you'll see a second account with
a **Marketing only** purpose, and the Campaign Studio banner disappears.

## Good to know

- **You can't accidentally break transactional email.** Spwig won't let you set your only
  account to "Marketing only", or disable/delete your last transactional account — there
  is always somewhere for order confirmations and password resets to go.
- **Warm up gradually.** A brand-new sending domain has no reputation yet.

Ramp your
  volume up over a couple of weeks rather than blasting your whole list on day one.
- **Keep the subdomain's DNS healthy.** SPF, DKIM, and DMARC on the marketing subdomain
  need to stay valid, just like your main domain.

Preserve all markdown formatting, image paths, code blocks, and technical terms.

請參閱
  [電子郵件送達率操作手冊](deliverability) 以了解完整資訊。
- **同意機制仍然適用。** 行銷郵件僅發送給已選擇訂閱的用戶，
  且每封行銷郵件都包含取消訂閱連結 — 分離網域不會改變這些規定。