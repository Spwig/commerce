---
slug: customer-wallet
title_i18n_key: Customer Wallet
category: customers
component: wallet
keywords:
  - customer wallet
  - store credit
  - wallet balance
  - wallet transactions
  - store credit balance
  - refund to wallet
  - manual credit
  - credit adjustment
  - transaction history
  - wallet ledger
  - pending balance
  - referral reward
  - promotional credit
related:
  - customer-analytics
  - customer-segments
  - abandoned-carts
url_patterns:
  - /admin/wallet/customerwallet/
  - /admin/wallet/wallettransaction/
published: true
---

The customer wallet is a store credit ledger that tracks a running balance for each customer. Store credit can be added as a result of refunds, referral rewards, promotional campaigns, or manual adjustments made by your team.

> **Wallet balances are spendable at checkout.** A signed-in customer with store credit sees it on the payment step and can apply it with one click. The credit comes off the final bill — after tax and delivery — and any remainder is charged to their card as usual. If the credit covers the whole order, no card is needed at all. Credit is reserved when applied and only actually deducted once payment is confirmed, so an abandoned checkout never costs the customer anything.

Navigate to **Customers > Customer Wallets** to view and manage wallets.

## Understanding wallet balances

Each customer wallet shows four balance figures:

| Balance | Description |
|---|---|
| **Available Balance** | The customer's current, usable credit — this will be what's spendable at checkout once that feature ships |
| **Pending Balance** | Credits that aren't in the available balance yet — for example, a refund that is still within its confirmation window |
| **Lifetime Credited** | The total amount ever credited to this wallet, including all past credits |
| **Lifetime Used** | The total amount ever debited from this wallet |

The available balance is the figure that will matter once checkout spending is live. Pending credits move into it once the pending period expires.

## Viewing a customer's wallet

1. Navigate to **Customers > Customer Wallets**
2. Use the search field to find the customer by name or email
3. Click the wallet entry to open the detail view

The detail view shows the current balances at the top and a full transaction history below. The **Last Credited At** and **Last Used At** timestamps tell you when the wallet was last active.

### Filtering the wallet list

Use the **Active** filter to separate live wallets from frozen ones. A wallet marked as inactive is frozen — no credits or debits can be recorded against it, even though it keeps its balance.

## Reading the transaction history

Every change to a wallet balance is recorded as an individual transaction. The transaction history is a complete, permanent ledger — transactions are never edited or deleted. If an error needs to be corrected, a new compensating transaction is added instead.

Each transaction shows:

| Field | Description |
|---|---|
| **Type** | Credit, Debit, Refund, Adjustment, or Reversal |
| **Amount** | The value of this transaction (always shown as a positive number) |
| **Balance After** | The wallet balance immediately after this transaction was applied |
| **Source** | Where the credit or debit originated |
| **Status** | Completed, Pending, or Reversed |
| **Description** | A short explanation of the transaction |
| **Reference ID** | A link to the originating record (e.g., an order number or reward ID) |
| **Created At** | When the transaction was recorded |

### Transaction types explained

- **Credit** — funds added to the wallet (from a refund, promotion, or manual adjustment)
- **Debit** — funds removed from the wallet. Once checkout spending ships this will mean "spent on an order" — for now the only way a debit happens is a manual adjustment
- **Refund** — credit added specifically as a result of a returned or cancelled order
- **Adjustment** — a manual correction made by your team
- **Reversal** — a transaction that cancels out an earlier entry

### Transaction sources explained

- **Order Refund** — credit issued when an order was refunded back to the wallet
- **Referral Reward** — credit earned through the referral programme
- **Promotion** — credit granted as part of a marketing campaign
- **Manual Adjustment** — credit added or removed directly by a staff member
- **Order Payment** — funds spent at checkout to pay for an order. Not yet in use — reserved for when wallet checkout spending ships

## Manual wallet adjustments

You cannot add or remove funds from the admin panel — wallet transactions are created only by the processes that own them: order refunds, loyalty rewards, and referral rewards. This is deliberate. Every movement carries a reference back to what caused it, and a nightly check verifies each wallet's balance against its own history; hand-entered rows are what break that chain.

For a goodwill credit — a service complaint, a gesture after a problem — issue a **gift card** by hand instead (see the **Gift Cards** help topic). A gift card is designed for exactly this: you control the value, the customer gets a code by email, and it spends at checkout the same way store credit does.

## Freezing a wallet

If you need to prevent a customer from using their wallet balance — for example, during a fraud investigation — you can deactivate it without deleting it or removing the balance.

1. Open the customer's wallet detail view
2. Uncheck the **Active** toggle
3. Click **Save**

The balance is preserved and the wallet can be reactivated at any time. While inactive, no new credits or debits — manual or otherwise — can be recorded against the wallet.

## Viewing all transactions

For a store-wide view of wallet activity, navigate to **Customers > Wallet Transactions**. This list shows every transaction across all customer wallets, with filters for:

- **Transaction Type** — filter by credit, debit, adjustment, etc.
- **Source** — filter by where transactions originated
- **Status** — filter by completed, pending, or reversed
- **Date** — use the date hierarchy at the top to drill into a specific day, month, or year

The transaction list is read-only — transactions cannot be edited or deleted from this view.

## Tips

- Check **Lifetime Credited** versus **Lifetime Used** to understand how actively a customer uses their store credit — a large unused balance may indicate the customer has forgotten it exists
- If a customer reports their balance looks wrong, review the full transaction history to trace exactly how the balance changed over time; the **Balance After** column on each entry makes this easy
- A large unspent balance is worth a nudge — customers see their store credit on the account dashboard and on the payment step at checkout, but a short email pointing it out often converts it into an order
- Frozen wallets retain their balance permanently; there is no expiry — if you deactivate a wallet temporarily, remember to reactivate it when the issue is resolved
- The **Reference ID** on each transaction links back to the originating record, making it straightforward to verify why a credit or debit was applied without having to search elsewhere
