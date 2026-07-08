---
slug: shipping-provider-accounts
title_i18n_key: Shipping Provider Accounts
category: orders-shipping
component: shipping
keywords:
  - shipping providers
  - carrier integration
  - FedEx API
  - UPS API
  - DHL API
  - carrier accounts
  - real-time rates
  - API credentials
  - shipping API
  - carrier connection
  - label purchase
  - tracking integration
  - provider setup
url_patterns:
  - /admin/shipping/provideraccount/
  - /admin/shipping/provideraccount/add/
  - /admin/shipping/provideraccount/\d+/change/
related:
  - shipping-methods
  - carrier-presets
  - shipping-packages
published: true
---

Shipping provider accounts connect your store to carrier APIs (FedEx, UPS, DHL) for real-time rate calculation and automated label purchase. Each account stores encrypted API credentials, monitors connection health, and links to real-time shipping methods. Providers fetch live rates at checkout based on package dimensions, weight, origin, and destination—eliminating manual rate table maintenance and ensuring accurate carrier pricing.

Use provider accounts when you need carrier-calculated shipping rates or automated label generation instead of manual shipment creation.

## Supported Shipping Providers

Spwig supports major carriers through installable provider components:

### FedEx

**Services**: Ground, Express, International
**API**: FedEx Web Services
**Features**: Real-time rates, label purchase, tracking, international customs

### UPS

**Services**: Ground, Air, Worldwide
**API**: UPS Developer API
**Features**: Real-time rates, label generation, tracking, address validation

### DHL

**Services**: Express, eCommerce, International
**API**: DHL Express API
**Features**: International rates, customs documents, tracking

### Additional Providers

Install from component marketplace as needed (USPS, Canada Post, Australia Post, etc.)

---

## Provider Account Configuration

Each provider account requires:

### Basic Information

- **Display Name**: How account appears in admin (e.g., "FedEx Production Account")
- **Provider**: Select installed provider component from dropdown
- **Active**: Toggle to enable/disable without deleting credentials
- **Is Default**: Set as default account for this provider (only one default per provider)

### API Credentials (Encrypted)

**Varies by provider**, typically includes:

**FedEx**:
- Account Number
- Meter Number
- API Key
- API Secret

**UPS**:
- Access License Number
- User ID
- Password
- Account Number

**DHL**:
- Site ID
- Password
- Account Number

**All credentials are encrypted at rest** and only decrypted when making API calls.

### Origin Address

- **Default Ship From**: Warehouse/origin address for rate calculation
- Some providers require specific origin setup in their dashboard

### Settings

Provider-specific options (varies by carrier):

- **Test Mode**: Use carrier's sandbox/test API endpoints
- **Negotiated Rates**: Use your negotiated carrier rates (if available)
- **Include Insurance**: Auto-quote insurance in rates
- **Residential Surcharge**: Apply residential delivery fees
- **Signature Required**: Default signature requirements

---

## Creating a Provider Account

**6-Step Setup Process**:

**Step 1: Obtain Carrier API Access**
1. Create account with carrier (FedEx.com, UPS.com, DHL.com)
2. Apply for API/Developer access
3. Complete carrier's API onboarding (may take 1-3 business days)
4. Receive API credentials via email or developer portal

**Step 2: Install Provider Component** (if not pre-installed)
1. Go to Settings > Components > Marketplace
2. Search for carrier name (e.g., "FedEx")
3. Install shipping provider component
4. Wait for installation to complete

**Step 3: Create Provider Account in Spwig**
1. Navigate to Settings > Shipping > Provider Accounts
2. Click "Add Provider Account"
3. Select provider from dropdown
4. Enter display name

**Step 4: Enter API Credentials**
1. Fill credential fields (varies by provider)
2. Credentials are auto-encrypted on save
3. Optional: Enable test mode for initial testing

**Step 5: Test Connection**
1. Click "Test Connection" button
2. System attempts API call to carrier
3. Verify "Connected" status appears
4. Check last_tested_at timestamp

**Step 6: Link to Shipping Method**
1. Create or edit shipping method (Settings > Cart > Shipping Methods)
2. Set method_type = "Real-Time"
3. Select provider account from dropdown
4. Save method

---

## Connection Status Monitoring

Provider accounts track connection health:

### Status Values

**Unknown** (gray): Never tested or not yet connected

**Connected** (green): Last API call successful, credentials valid

**Error** (red): Last API call failed, credentials may be invalid

### Last Tested

- **Timestamp**: When connection was last verified
- **Auto-updates**: Every time provider used (rate fetch, label purchase)
- **Manual test**: Click "Test Connection" button anytime

### Troubleshooting Failed Connections

**Common Causes**:
- Incorrect API credentials (typo, copied with extra space)
- Carrier API key expired or revoked
- Test mode enabled but using production credentials (or vice versa)
- IP address not whitelisted with carrier
- Carrier API downtime

**Solution Steps**:
1. Verify credentials match carrier dashboard exactly
2. Check test mode setting matches credential type
3. Review carrier's API status page for outages
4. Contact carrier support for account verification

---

## Rate Lookup Workflow

How real-time rates work at checkout:

**1. Customer Enters Address**
- Shipping address entered
- Cart calculates total weight + dimensions

**2. System Prepares Rate Request**
- Fetches provider account credentials (decrypted)
- Calculates package dimensions from cart items (uses shipping packages if defined)
- Prepares API request with origin, destination, parcels

**3. Provider API Called**
- Request sent to carrier API with auth credentials
- Carrier calculates rate based on zone, weight, dimensions
- Response includes service options (Ground, Express, etc.)

**4. Rates Displayed**
- System parses carrier response
- Normalizes to standard format
- Optional markup applied (if configured)
- Rates shown to customer at checkout

**5. Customer Selects Service**
- Customer chooses preferred option
- Selected rate saved to order

**Example API Flow**:
```
Request to FedEx API:
{
  "origin": {"postal_code": "90210", "country": "US"},
  "destination": {"postal_code": "10001", "country": "US"},
  "parcels": [{
    "weight": 2500,  // grams
    "dimensions": {"length": 30, "width": 20, "height": 15}  // cm
  }]
}

FedEx Response:
[
  {"service": "FEDEX_GROUND", "rate": 12.50, "delivery_days": 5},
  {"service": "FEDEX_EXPRESS", "rate": 28.75, "delivery_days": 2}
]
```

---

## Label Purchase (Optional)

If provider supports label generation:

**Workflow**:
1. Customer completes order
2. Merchant creates shipment (Orders > Order Detail > Create Shipment)
3. Select provider account + service
4. System calls provider's label API
5. Label PDF generated and attached to shipment
6. Tracking number auto-filled
7. Label ready for printing

**Benefits**:
- No manual carrier website login
- Tracking auto-synced
- Customs forms auto-generated (international)
- Batch label generation possible

---

## Rate Markup

Add merchant markup to carrier rates:

**Configuration** (in shipping method, not provider account):
- **Markup Type**: Percentage or Fixed
- **Markup Amount**: e.g., 15% or $2.50

**Example**:
```
Carrier Rate: $12.50
Markup: 15%
Customer Pays: $14.38

OR

Carrier Rate: $12.50
Markup: $2.50 (fixed)
Customer Pays: $15.00
```

**Use Cases**:
- Cover packaging/handling costs
- Add profit margin to shipping
- Offset credit card fees on shipping

---

## Multiple Provider Accounts

You can create multiple accounts for same provider:

**Use Cases**:
1. **Test vs Production**
   - Test Account: Carrier sandbox credentials
   - Production Account: Live credentials

2. **Multiple Warehouses**
   - Warehouse A Account: Origin = Los Angeles
   - Warehouse B Account: Origin = New York

3. **Different Negotiated Rates**
   - Account A: Standard rates
   - Account B: Volume discount rates

**Each account can link to different shipping methods** for flexible configuration.

---

## Tips

- **Test in sandbox first** - Use carrier test credentials before going live
- **Monitor connection status** - Check dashboard for error statuses regularly
- **Define shipping packages** - Accurate dimensions improve rate quotes
- **Use negotiated rates** - Enable if you have volume discounts with carrier
- **Set realistic origin** - Use actual ship-from address for accurate zones
- **Keep credentials secure** - Never share API keys, rotate periodically
- **Have backup method** - Keep flat-rate method active if carrier API fails
- **Monitor carrier API limits** - Some carriers limit API calls per day
- **Update credentials promptly** - When carrier rotates keys, update immediately
- **Use descriptive names** - "FedEx LA Warehouse" better than "FedEx 1"
