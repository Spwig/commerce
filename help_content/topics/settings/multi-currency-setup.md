---
slug: multi-currency-setup
title_i18n_key: Multi-Currency Setup
category: settings
component: core
keywords:
  - multi-currency
  - multiple currencies
  - exchange rates
  - currency switcher
  - foreign currency
  - exchange rate provider
  - currency conversion
  - international selling
  - currency markup
  - rate selection strategy
  - supported currencies
  - locale formatting
  - manual exchange rate
  - sync interval
  - display only
  - checkout mode
  - rate lock
  - auto sync
url_patterns:
  - /admin/core/sitesettings/1/change/
  - /admin/exchange_rates/manualexchangerate/
related:
  - multi-currency-gift-cards
published: true
---

Multi-currency allows your customers to browse products and complete checkout in their preferred currency. Prices are automatically converted from your base currency using exchange rates from a connected provider or manually defined rates.

## Before you begin

Before enabling multi-currency, you need:

1. **An active exchange rate provider** - Go to **Settings > Multi-Currency tab > Exchange Rates Dashboard** and connect at least one provider (such as Open Exchange Rates, Fixer.io, or ExchangeRate-API). The provider must be active and syncing rates.
2. **At least two currencies** - Your base currency plus one or more additional currencies you want to support.

## Enabling multi-currency

Navigate to **Settings > Multi-Currency** and check **Enable Multi-Currency**. Once enabled, configure the following options:

| Setting | Description |
|---------|-------------|
| **Currency Selection Mode** | How customers choose their currency. *Auto* detects from their location, *Manual* lets them pick from a switcher, *Both* combines the two approaches. |
| **Show Currency Switcher** | Display a currency selector on your storefront so customers can change currency manually. |
| **Switcher Position** | Where the currency switcher appears (header, footer, or sidebar). |
| **Show Exchange Rate Info** | Display a notice to customers that prices are approximate conversions from your base currency. |
| **Enable Locale Formatting** | Format numbers and currency symbols according to each customer's locale (e.g., 1.234,56 for European formats). |

## Checkout mode

Choose how multi-currency works at checkout:

| Mode | Description |
|------|-------------|
| **Full Multi-Currency** | Customers browse, add to cart, and pay in their selected currency. The exchange rate is locked at checkout and recorded with the order. This is the default. |
| **Display Only** | Prices are shown in the customer's currency for convenience, but the cart and payment are always processed in your base currency. At checkout, customers see a notice showing the approximate converted amount alongside the actual charge amount in your base currency. |

**Display Only** is useful when your payment provider only supports your base currency, or when you want to avoid exchange rate risk entirely. Customers still see localised prices while browsing, giving them a sense of cost in their own currency.

## Exchange rate sync interval

Control how often your store fetches fresh rates from your connected provider:

| Interval | Description |
|----------|-------------|
| **Real-time** | Every 15 minutes. Best for stores with high-volume international sales. |
| **Hourly** | Once per hour. Good balance of freshness and API usage. |
| **Daily** | Once per day. Suitable for most stores. This is the default. |
| **Weekly** | Once per week. For stores with stable pricing. |
| **Monthly / Quarterly** | Less frequent updates for stores that rarely change rates. |
| **Manual Only** | Rates are never fetched automatically. You manage all rates manually. |

The sync interval affects how often the background task fetches rates from your provider. Between syncs, cached rates are used. If you need to force an immediate sync, use the **Sync Now** button on the Exchange Rates Dashboard or **Sync from Provider** on the Manual Exchange Rates page.

## Manual exchange rates

Manual exchange rates let you set exact conversion rates for specific currency pairs. They take precedence over provider-fetched rates, giving you full control over pricing.

Navigate to **Exchange Rates > Manual Exchange Rates** to manage them.

### Setting rates manually

Click **Add Rate** to create a rate for a currency pair. Specify the base currency, target currency, and the rate. For example, setting USD/EUR to 0.92 means 1 USD = 0.92 EUR.

### Syncing from a provider

Click **Sync from Provider** to automatically populate manual rates from your connected provider's latest rates. This creates manual rates for all supported currencies, giving you a starting point to fine-tune.

Locked rates are skipped during sync, so any rates you have manually adjusted will not be overwritten.

### Locking rates

Click the lock icon on any rate to prevent it from being overwritten during provider sync. This is useful when you have negotiated a specific rate or want to maintain a fixed rate regardless of market movements.

- **Locked** rates show a lock badge and are excluded from auto-sync.
- **Unlocked** rates can be updated when you click Sync from Provider.

### Provider comparison

Each manual rate displays the current provider rate alongside it, with a percentage difference. This helps you see at a glance how your manual rates compare to market rates:

- A **green** percentage means your rate is higher than the provider rate.
- A **red** percentage means your rate is lower than the provider rate.

## Exchange rate markup

You can add a percentage markup to exchange rates to cover currency conversion fees and protect against rate fluctuations between when a customer places an order and when you receive the payment.

For example, a 2% markup on a 1.18 USD/EUR rate would adjust it to approximately 1.20 USD/EUR. This small buffer helps ensure you don't lose money on currency conversions.

## Rate selection strategy

When you have multiple exchange rate providers connected, you can choose how rates are selected:

- **Primary Provider** - Always uses rates from your designated primary provider. This ensures consistent pricing across your store. If the primary provider has no data for a currency pair, it falls back to the latest available rate from any provider.
- **Latest Available** - Uses the most recently synced rate from any active provider. This gives you the freshest data but rates may vary slightly between providers.

For most stores, **Primary Provider** is the recommended choice as it provides the most predictable pricing.

## Supported currencies

Use the drag-and-drop currency manager to choose which currencies your store supports:

1. **Available Currencies** (left column) shows all currencies you can enable.
2. **Active Currencies** (right column) shows the currencies currently enabled on your store.
3. Drag currencies between columns to enable or disable them.
4. Drag within the Active column to reorder how currencies appear in the switcher.
5. Click **Save Currency Configuration** to apply your changes.

Your base currency is always active and cannot be removed.

## How exchange rates are resolved

When a price needs to be converted, the system checks rates in this order:

1. **Manual exchange rate** - If an active manual rate exists for the currency pair, it is always used first.
2. **Provider rate** - If no manual rate exists, the latest rate from your connected provider is used.

This means you can use providers for most currencies and override specific pairs with manual rates where you need precise control.

## Important: This setting is permanent

Once multi-currency is enabled and customers place orders in foreign currencies, this setting **cannot be disabled**. This is because:

- Orders permanently store the customer's chosen currency and the exchange rate used at the time of purchase.
- Financial reports and refund calculations depend on this historical currency data.
- Disabling multi-currency would leave existing multi-currency orders in an inconsistent state.

If no orders have been placed in foreign currencies, you can still disable multi-currency.

## Tips

- **Test with a small order first** - Place a test order in a foreign currency to verify the checkout flow and ensure exchange rates are applied correctly.
- **Monitor exchange rates regularly** - Check the Exchange Rates Dashboard periodically to ensure your provider is syncing rates and they look reasonable.
- **Consider markup for volatile currencies** - If you support currencies with high volatility, a slightly higher markup (2-3%) can protect your margins.
- **Start with major currencies** - Begin with widely-used currencies (EUR, GBP, JPY, CAD, AUD) and expand based on customer demand.
- **Review payment provider compatibility** - Not all payment providers support all currencies. Check your payment provider's documentation to confirm which currencies they process.
- **Use Display Only mode if unsure** - If you're not sure whether your payment provider handles multi-currency checkout, start with Display Only mode. You can switch to Full Multi-Currency later.
- **Lock rates before promotional periods** - If you're running a sale, lock your exchange rates beforehand to ensure consistent pricing throughout the promotion.
