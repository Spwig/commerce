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

The customer wallet is a store credit system that gives customers a balance they can spend on future orders. Store credit can be added as a result of refunds, referral rewards, promotional campaigns, or manual adjustments made by your team. Customers can then apply their wallet balance at checkout to reduce the amount they pay.

Navigate to **Customers > Customer Wallets** to view and manage wallets.

## Understanding wallet balances

Each customer wallet shows four balance figures:

| Balance | Description |
|---|---|
| **Available Balance** | The amount the customer can spend right now at checkout |
| **Pending Balance** | Credits that are not yet spendable — for example, a refund that is still within its confirmation window |
| **Lifetime Credited** | The total amount ever credited to this wallet, including all past credits |
| **Lifetime Used** | The total amount the customer has spent from their wallet across all orders |

The available balance is the only figure that matters at checkout. Pending credits become available once the pending period expires.

## Viewing a customer's wallet

1. Navigate to **Customers > Customer Wallets**
2. Use the search field to find the customer by name or email
3. Click the wallet entry to open the detail view

The detail view shows the current balances at the top and a full transaction history below. The **Last Credited At** and **Last Used At** timestamps tell you when the wallet was last active.

### Filtering the wallet list

Use the **Active** filter to separate live wallets from frozen ones. A wallet marked as inactive cannot be used at checkout even if it has a positive balance.

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
- **Debit** — funds spent at checkout
- **Refund** — credit added specifically as a result of a returned or cancelled order
- **Adjustment** — a manual correction made by your team
- **Reversal** — a transaction that cancels out an earlier entry

### Transaction sources explained

- **Order Refund** — credit issued when an order was refunded back to the wallet
- **Referral Reward** — credit earned through the referral programme
- **Promotion** — credit granted as part of a marketing campaign
- **Manual Adjustment** — credit added or removed directly by a staff member
- **Order Payment** — funds spent at checkout to pay for an order

## Manual wallet adjustments

You cannot add or remove funds directly from the wallet detail view — wallet transactions are created through the relevant processes (refunds, rewards, promotions). However, staff members with the appropriate permissions can create manual adjustment transactions through the **Wallet Transactions** section.

Navigate to **Customers > Wallet Transactions** and use **+ Add Wallet Transaction** if you need to apply a credit that doesn't fit another source — for example, a goodwill credit following a service complaint.

When creating a manual adjustment:

1. Select the **Wallet** you are adjusting (search by customer email)
2. Set **Transaction Type** to `Adjustment`
3. Set **Source** to `Manual Adjustment`
4. Enter the **Amount** — always a positive number regardless of direction
5. Set the **Status** to `Completed` for an immediate credit
6. Add a clear **Description** explaining the reason — this is visible in the transaction history
7. Click **Save**

> **Note:** Because wallet transactions are immutable, double-check the amount and wallet before saving. If you make a mistake, you will need to create a reversal transaction to correct it.

## Freezing a wallet

If you need to prevent a customer from using their wallet balance — for example, during a fraud investigation — you can deactivate it without deleting it or removing the balance.

1. Open the customer's wallet detail view
2. Uncheck the **Active** toggle
3. Click **Save**

The balance is preserved and the wallet can be reactivated at any time. While inactive, the customer cannot apply the wallet balance at checkout.

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
- Use wallet credits as a customer retention tool — a goodwill credit after a difficult order experience can cost less than a refund while keeping the customer spending in your store
- Frozen wallets retain their balance permanently; there is no expiry — if you deactivate a wallet temporarily, remember to reactivate it when the issue is resolved
- The **Reference ID** on each transaction links back to the originating record, making it straightforward to verify why a credit or debit was applied without having to search elsewhere
