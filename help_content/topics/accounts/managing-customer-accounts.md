---
slug: managing-customer-accounts
title_i18n_key: Managing Customer Accounts
category: customers
component: accounts
keywords:
  - customer account
  - create customer
  - edit customer
  - guest conversion
  - customer management
  - add customer
  - deactivate account
  - customer profile
  - customer details
  - customer notes
url_patterns:
  - /admin/accounts/customerprofile/
related:
  - customer-analytics
  - accounts-vs-customers
published: true
---

Customer accounts let merchants track customer information, order history, and preferences. Navigate to **Customers > All Customers** in the admin sidebar to manage customer accounts.

![Add Customer](/static/core/admin/img/help/managing-customer-accounts/add-customer.webp)

## Understanding Customer Accounts vs Customer Profiles

**Customer Accounts** are the login credentials (email/password) stored in the User model. **Customer Profiles** store additional customer information like phone number, date of birth, preferences, and analytics. Every customer account has a corresponding profile that stores this extended data.

When you manage customers in the admin, you're working with Customer Profiles that link to User accounts behind the scenes.

## Viewing All Customers

The customer list shows all registered customers with key metrics:

| Column | Description |
|--------|-------------|
| **User** | Customer name and email address |
| **Affiliate Status** | Whether the customer is also an affiliate partner |
| **Customer Value** | Total amount the customer has spent (color-coded) |
| **Customer Segment** | RFM segment (Champion, Loyal, At Risk, etc.) |
| **Total Orders** | Number of completed orders |
| **Days Since Last Order** | Recency of last purchase |
| **VIP Customer** | Badge if customer is marked as VIP |

### Filtering Customers

Use the filter sidebar to narrow down the list:

- **Account Type** — Guest or Registered
- **Affiliate Status** — Is Affiliate, Not Affiliate, Affiliate Pending, Active, Suspended, Rejected
- **Dashboard Layout** — Customer's preferred dashboard layout
- **Created At** — Filter by registration date

### Searching Customers

Use the search bar to find customers by:
- Username
- Email address
- First name
- Last name
- Phone number

### Bulk Actions

Select one or more customers and use the **Action** dropdown to apply bulk operations:

- **Refresh customer metrics** — Recalculates analytics, LTV, and RFM scores for the selected customers
- **Export customer data** — Downloads a CSV file with profile, order, and analytics data
- **Convert to Affiliate** — Creates an affiliate profile for the selected customers (pending review)
- **Send activation invitation email** — Sends a guest-to-registered conversion email to selected guest accounts

## Viewing Customer Details

Click on a customer's name to view their full profile. The customer detail page shows:

![Customer Detail](/static/core/admin/img/help/managing-customer-accounts/customer-detail.webp)

### Customer Information Section

Basic contact details and account status:
- **User** — Link to the underlying User account
- **Phone** — Customer's phone number
- **Date of Birth** — For age verification and birthday promotions

### B2B / Company Information

For business customers, you can record:
- **Company Name** — Business or company name
- **Tax ID / VAT Number** — Business tax or VAT registration number
- **Business Customer** — Check this to classify the account as B2B

These fields help you manage wholesale and trade customers separately from retail customers.

### Dashboard Preferences

How the customer has customized their account dashboard:
- **Dashboard Layout** — Grid, list, or compact view
- **Show Order History** — Whether order history appears on dashboard
- **Show Wishlist** — Whether wishlist appears on dashboard
- **Show Recent Products** — Whether recently viewed products appear
- **Show Recommendations** — Whether product recommendations appear

### Communication Preferences

Customer's opt-in status for various communications:
- **Newsletter Subscribed** — Opted into general newsletters
- **Marketing Emails** — Opted into promotional emails
- **Order Notifications** — Opted into order status updates

### Customer Analytics

Read-only summaries of customer behavior and value:
- **Customer Analytics Summary** — RFM scores, segment, lifetime value
- **Purchase Behavior Summary** — Order frequency, average order value, preferred categories
- **Engagement Summary** — Last login, email open rates, site activity

These analytics fields are computed automatically and cannot be edited manually. See [Understanding Customer Analytics](customer-analytics.md) for details.

## Creating a Customer Account

Merchants can manually create customer accounts for phone orders, in-store pickups, or to pre-register wholesale customers.

1. Click **+ Add Customer Profile** in the top right
2. Fill in the required and optional fields:

| Field | Required | Description |
|-------|----------|-------------|
| **User** | Yes | Select an existing User account or create a new one |
| **Phone** | No | Customer's phone number |
| **Date of Birth** | No | For age verification and birthday campaigns |
| **Company Name** | No | Business name for B2B customers |
| **Tax ID / VAT Number** | No | Business tax identification number |
| **Business Customer** | No | Check to mark as a B2B account |

### Creating a New User While Adding a Profile

If the customer doesn't have a User account yet:
1. Click the **+** icon next to the User field
2. Enter the customer's **email address** (this becomes their username)
3. Optionally enter **first name** and **last name**
4. Optionally set a **password**
5. Check **Send password reset email** if you didn't set a password
6. Save the User account
7. Complete the Customer Profile fields
8. Click **Save**

### Welcome Emails

After creating a customer account:
- If you set a password, the customer can log in immediately with that password
- If you didn't set a password, the system sends a password reset email so the customer can set their own password
- You can manually trigger a welcome email through the email system at **Marketing > Email Campaigns**

## Editing Customer Information

To update customer details:
1. Navigate to **Customers > All Customers**
2. Click the customer's name
3. Modify the fields you want to update
4. Click **Save**

### What You Can Edit

**Contact Details:**
- Name (via the User account)
- Email address (via the User account)
- Phone number
- Date of birth

**B2B Information:**
- Company name
- Tax ID / VAT number
- Business customer flag

**Preferences:**
- Dashboard layout and visibility settings

### What You Cannot Edit

These fields are computed automatically based on customer behavior:
- Total spent / Customer value
- Order count
- Customer segment (Champion, Loyal, At Risk, etc.)
- RFM scores
- Lifetime value predictions
- Last order date
- Analytics summaries

If these fields appear incorrect, check the underlying order data or trigger a manual recalculation at **Customers > Analytics** → **Recalculate Metrics**.

## Customer Notes

Add internal notes about customers to track support issues, VIP requests, or follow-up tasks.

### Adding a Note

1. Open a customer's profile
2. Scroll to the **Customer Notes** section (may be a separate tab)
3. Click **+ Add Note**
4. Fill in the note details:

| Field | Description |
|-------|-------------|
| **Note Type** | General, Support Issue, Complaint, Compliment, VIP Service, Follow Up Required, Payment Issue, Shipping Issue |
| **Title** | Short summary of the note |
| **Content** | Detailed note content |
| **Requires Follow Up** | Check if this needs action |
| **Follow Up Date** | Date to follow up by |
| **Completed** | Check when the follow-up is done |

### Note Types

| Type | Use Case |
|------|----------|
| **General Note** | Any general observation about the customer |
| **Support Issue** | Record of a support ticket or issue |
| **Complaint** | Customer complaint for tracking and resolution |
| **Compliment** | Positive feedback about the customer or their feedback about you |
| **VIP Service** | Special handling requests for VIP customers |
| **Follow Up Required** | Tasks that need action by a specific date |
| **Payment Issue** | Notes about payment problems or disputes |
| **Shipping Issue** | Notes about shipping problems or special delivery requests |

### Viewing Note History

All notes appear in chronological order on the customer's profile. Each note shows:
- Created date and time
- Created by (staff member name)
- Note type badge
- Title and content
- Follow-up status if applicable

### Internal vs Customer-Visible Notes

All customer notes are **internal only** by default — customers never see these notes. They are for merchant team communication only.

If you need to communicate with the customer, use the email system at **Marketing > Email Campaigns** or add an order comment on the specific order.

## Converting Guest to Registered Customer

Guest customers are created automatically when someone completes checkout without creating an account. Their username follows the pattern `guest_10374` where the number is a unique ID.

To convert a guest to a registered customer:

1. Navigate to **Customers > All Customers**
2. Search for the guest by their order email address
3. Click on the guest customer profile
4. Click the **User** link to edit the underlying User account
5. Change the **username** from `guest_10374` to the customer's real email address
6. Change the **email** to match
7. Optionally add **first name** and **last name**
8. Check **Send password reset email** so the customer can set a password
9. Click **Save**

The customer can now log in with their email address and will see their past guest orders in their order history.

### Why Convert Guest Customers?

- Guest orders don't count toward customer analytics or segments
- Guests can't track orders or access order history
- Converting guests increases registered customer count and improves analytics accuracy
- Registered customers are more likely to make repeat purchases

## Deactivating vs Deleting Accounts

### Deactivating a Customer Account

Deactivation prevents login while preserving all data:

1. Open the customer's profile
2. Click the **User** link to edit the User account
3. **Uncheck "Active"**
4. Click **Save**

**What happens:**
- Customer cannot log in
- Order history is preserved
- Customer can be reactivated later by checking "Active" again
- Analytics and metrics remain intact

**Use deactivation for:**
- Temporarily suspending accounts due to payment disputes
- Blocking abusive customers
- Customers who requested to stop receiving access but not delete data

### Deleting a Customer Account

Deletion removes the account and can orphan order history:

1. Open the customer's profile
2. Scroll to the bottom and click **Delete**
3. Confirm the deletion

**What happens:**
- Customer account is permanently removed
- Customer Profile is deleted
- Order history may be orphaned (orders exist but aren't linked to a customer)
- Cannot be undone

**Use deletion for:**
- GDPR/CCPA data deletion requests (export data first)
- Test accounts that should never have existed
- Duplicate accounts created by mistake

### GDPR Compliance

Before deleting a customer account in response to a GDPR request:

1. Navigate to **Customers > All Customers**
2. Select the customer
3. Use the **Export Data** action to generate a complete data export
4. Send the export to the customer if they requested it
5. Then proceed with deletion

The export includes: customer profile, order history, addresses, notes, and analytics data.

## Tips

- **Use filters to identify high-value customers** — Filter by Customer Value to find your Champions and VIPs
- **Review customer notes regularly** — Check for open follow-up tasks at least weekly
- **Don't manually edit analytics** — Let the system calculate RFM scores and segments automatically
- **Convert guests proactively** — After a guest makes a second purchase, reach out and offer to create a proper account
- **Use deactivate instead of delete** — Deactivation preserves data and can be reversed if needed
- **Add notes during support calls** — Document support interactions so other team members have context
- **Set follow-up dates** — Use the follow-up task system in notes to ensure nothing falls through the cracks
- **Respect communication preferences** — Never send marketing emails to customers who've opted out
