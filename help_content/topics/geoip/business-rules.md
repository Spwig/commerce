---
slug: business-rules
title_i18n_key: Location-Based Business Rules
category: customers
component: geoip
keywords:
  - business rules
  - geo rules
  - location rules
  - country rules
  - geo-based pricing
  - currency by country
  - redirect by country
  - geo-based access
  - regional rules
  - visitor conditions
  - IP-based rules
  - geographic restrictions
url_patterns:
  - /admin/geoip/businessrule/
related:
  - geoip-setup
  - visitor-analytics
  - customer-analytics
published: true
---

Location-based business rules let you automatically take actions when a visitor arrives from a specific country, region, or device type. You can use rules to set a currency for customers from a particular region, redirect visitors to a localized page, show a promotional banner, or restrict access to certain content.

Rules are evaluated in priority order every time a visitor session is established. When a rule matches, its configured actions are executed immediately.

## How business rules work

Each rule is made up of two parts:

- **Conditions** — the criteria that must be met for the rule to trigger (e.g., "visitor is from Germany")
- **Actions** — what happens when all conditions match (e.g., "set currency to EUR")

Conditions and actions are stored as JSON objects in the rule form. Spwig evaluates all active rules in priority order (lowest number first) and applies any that match.

## Navigating to business rules

Navigate to **Customers > Business Rules** to see all your configured rules. The list shows each rule's name, status, priority, how many times it has been triggered, and when it last fired.

Click any rule to view or edit it, or click **+ Add Business Rule** to create a new one.

## Creating a business rule

### Step 1: basic information

Fill in the rule's identification details:

- **Name** — a clear, descriptive name (e.g., `Set EUR for Eurozone`)
- **Description** — optional notes explaining the rule's purpose
- **Is Active** — check this to enable the rule; uncheck to pause it without deleting it
- **Priority** — lower numbers run first; use `10`, `20`, `30` to leave room for future rules

### Step 2: define conditions

In the **Conditions** field, enter a JSON object that describes when the rule should fire. All conditions in the object must be true for the rule to match.

#### Available condition keys

| Condition | Format | Example |
|-----------|--------|---------|
| `country_in` | Array of ISO country codes | `["DE", "FR", "IT"]` |
| `country_not_in` | Array of ISO country codes | `["US", "CA"]` |
| `region_in` | Array of region names | `["Bavaria", "Catalonia"]` |
| `region_not_in` | Array of region names | `["Quebec"]` |
| `is_mobile` | Boolean | `true` |
| `is_vpn` | Boolean | `false` |

#### Example conditions

Visitors from Germany, France, or Italy:
```json
{
  "country_in": ["DE", "FR", "IT"]
}
```

Visitors from the United States who are on a mobile device:
```json
{
  "country_in": ["US"],
  "is_mobile": true
}
```

Visitors from outside the European Union:
```json
{
  "country_not_in": ["AT","BE","BG","CY","CZ","DE","DK","EE","ES","FI","FR","GR","HR","HU","IE","IT","LT","LU","LV","MT","NL","PL","PT","RO","SE","SI","SK"]
}
```

### Step 3: define actions

In the **Actions** field, enter a JSON object describing what should happen when the rule triggers.

#### Available action keys

| Action | Format | Description |
|--------|--------|-------------|
| `set_currency` | Currency code string | Pre-select a currency for the visitor |
| `set_language` | Language code string | Set the display language |
| `show_banner` | Boolean | Trigger a promotional banner |
| `redirect_to` | URL path string | Redirect the visitor to a different URL |

#### Example actions

Set currency to Euro:
```json
{
  "set_currency": "EUR"
}
```

Redirect to a localized landing page:
```json
{
  "redirect_to": "/de/"
}
```

Set both currency and language together:
```json
{
  "set_currency": "GBP",
  "set_language": "en"
}
```

## Practical examples

### Example: Eurozone currency rule

**Scenario:** Automatically show Euro pricing to visitors from Eurozone countries.

| Field | Value |
|-------|-------|
| Name | `Eurozone — Set EUR` |
| Priority | `10` |
| Is Active | Checked |
| Conditions | `{"country_in": ["AT","BE","DE","ES","FI","FR","GR","IE","IT","LU","NL","PT"]}` |
| Actions | `{"set_currency": "EUR"}` |

### Example: UK pricing rule

**Scenario:** Show GBP pricing to visitors from the United Kingdom.

| Field | Value |
|-------|-------|
| Name | `UK — Set GBP` |
| Priority | `20` |
| Is Active | Checked |
| Conditions | `{"country_in": ["GB"]}` |
| Actions | `{"set_currency": "GBP"}` |

### Example: redirect to a localized store section

**Scenario:** Send visitors from Australia to a dedicated Australian page.

| Field | Value |
|-------|-------|
| Name | `Australia — Redirect` |
| Priority | `30` |
| Is Active | Checked |
| Conditions | `{"country_in": ["AU"]}` |
| Actions | `{"redirect_to": "/au/"}` |

## Testing rules

You can verify that a rule matches the expected visitor profile without waiting for real traffic:

1. In the Business Rules list, select the rule using its checkbox
2. Open the **Action** dropdown and choose **Test selected rules**
3. Click **Go**

Spwig will evaluate the rule against a sample US-based visitor profile and report whether it matched and which actions would have been triggered.

## Monitoring rule activity

The **Triggered** column in the rules list shows how many times each rule has fired. Click a rule to see the **Last Triggered** timestamp in the Statistics section.

Use the **Reset statistics** action to zero out trigger counts if you want to start measuring from a specific date after making changes to a rule.

## Tips

- Set priorities with gaps (10, 20, 30) rather than sequential numbers (1, 2, 3) so you can insert new rules later without renumbering everything
- Rules fire in priority order and all matching rules are applied — if two rules both set the currency, the lower-priority (higher-number) rule's action will be applied last
- Use the **Is Active** toggle to temporarily pause a rule during promotions without deleting the configuration
- Always test a new rule before activating it in a live environment to make sure the conditions are correct
- VPN detection (`"is_vpn": true`) is available if you want to apply different treatment to visitors masking their location, but keep in mind that some legitimate customers use VPNs for privacy
