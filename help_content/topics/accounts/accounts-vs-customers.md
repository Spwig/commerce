---
slug: accounts-vs-customers
title_i18n_key: Accounts vs Customers
category: customers
component: accounts
keywords:
  - accounts vs customers
  - user account
  - customer profile
  - staff account
  - guest user
  - what is an account
  - what is a customer
  - account vs customer difference
  - user vs customer
  - staff vs customer
url_patterns:
  - /admin/auth/user/
  - /admin/accounts/staffmember/
  - /admin/accounts/customerprofile/
related:
  - staff-roles
  - customer-analytics
published: true
---

Merchants often ask: "What is the difference between an account and a customer?" This confusion is common because every customer is an account, but not every account is a customer. This guide clarifies the distinction and explains when to use each admin interface.

![User List](/static/core/admin/img/help/accounts-vs-customers/user-list.webp)

## What is an Account?

An **account** is the core authentication object in Spwig. Anyone who can log in to your platform — staff member or customer — has an account. Accounts are managed in the Spwig authentication system and are stored in the `User` model.

All accounts have:
- **Email address** — The primary identifier and login credential
- **Username** — A unique username (auto-generated from email by default)
- **Password** — Hashed and stored securely
- **is_staff flag** — Determines if the account can access the admin backend

Accounts can also authenticate via OAuth providers (Google, Facebook, etc.) configured at **Settings > Authentication**.

## What is a Customer?

A **customer** is a special type of account with `is_staff=False`. Customers shop on your storefront, place orders, and manage their profiles. Every customer account is automatically extended with:

- **CustomerProfile** — Stores contact details, B2B information, dashboard preferences, and custom field values
- **CustomerMetrics** — Tracks lifetime value (LTV), RFM scores, order history, and segmentation data
- **OrderHistory** — Links to all orders placed by this customer

Customers can be:
- **Registered customers** — Created via storefront registration or admin
- **Guest users** — Temporary accounts created during guest checkout (username starts with `guest_`)
- **Imported customers** — Migrated from other platforms via CSV import

## The Key Difference

| Attribute | Account | Customer |
|-----------|---------|----------|
| **Purpose** | Authentication and authorization | Shopping, orders, and analytics |
| **Scope** | Staff members AND customers | Only customers |
| **is_staff flag** | True OR False | Always False |
| **Extended data** | None (core fields only) | CustomerProfile + CustomerMetrics |
| **Admin location** | Settings > Users | Customers > Customer Profiles |
| **Can log in** | Yes | Yes |
| **Can place orders** | Only if has CustomerProfile | Yes |
| **Can access admin** | Only if is_staff=True | No |
| **B2B fields** | None | Company name, Tax ID, Business Customer flag |

In short:
- An **account** is anyone who can log in
- A **customer** is an account that shops and places orders

## B2B Customer Fields

CustomerProfiles support business customers with dedicated B2B fields:

- **Company Name** — The business or company name for the account
- **Tax ID / VAT Number** — Business tax identification or VAT registration number
- **Business Customer** — Flag to classify the account as a B2B customer

These fields appear on the customer profile form and help you identify and manage wholesale or trade accounts separately from retail customers.

## Staff Members Are Also Accounts

Staff members are accounts with `is_staff=True`. They can log in to the admin backend and perform actions based on their assigned **StaffRole** permissions.

Staff members can optionally have a **CustomerProfile** if they also shop on the storefront. For example, if you (the merchant) place a test order on your own store, a CustomerProfile is created for your staff account. This does NOT affect your admin access.

Staff permissions are controlled by:
- **StaffRole** — Defines which admin sections and actions the staff member can access
- **is_superuser flag** — Grants full unrestricted access (use sparingly)

The **Settings > Users** list also shows each staff member's **2FA Status** (enabled or not enabled) and their assigned role badges, so you can quickly see who has two-factor authentication active.

Manage staff members at **Settings > Staff Management**.

## Guest Users

Guest checkout creates temporary accounts with auto-generated usernames starting with `guest_`. These accounts:
- Have `is_staff=False` (they are customers)
- Have a CustomerProfile (for order association)
- Have a random password (guest cannot log in unless they convert to registered)
- Are excluded from customer analytics by default

Guests can convert to registered customers by:
1. Creating an account on the storefront with the same email
2. Verifying their email address
3. System merges the guest order history into the new registered account

Manage guest conversion settings at **Settings > Checkout > Guest Checkout**.

## Where to Find Each

| Admin Location | What You Manage | Key Use Cases |
|----------------|-----------------|---------------|
| **Settings > Users** | All accounts (staff + customers) | Reset passwords, activate/deactivate accounts, assign staff permissions |
| **Settings > Staff Management** | Staff accounts only (is_staff=True) | Assign roles, manage team member access, configure permissions |
| **Customers > Customer Profiles** | Customer accounts only (is_staff=False) | View customer preferences, order history, LTV, RFM scores, segments |
| **Customers > Analytics** | Customer metrics and segments | Analyze customer behavior, create marketing segments, track retention |

![Customer Profile List](/static/core/admin/img/help/accounts-vs-customers/customer-profile-list.webp)

## When to Use Each Interface

Use **Settings > Users** when you need to:
- Reset a customer's password
- Deactivate a compromised account
- Manually create a customer account
- View OAuth login connections
- See all accounts (staff + customers) in one list

Use **Settings > Staff Management** when you need to:
- Add a new team member
- Assign or change a staff member's role
- Configure granular permissions
- Audit staff activity logs

Use **Customers > Customer Profiles** when you need to:
- View a customer's order history
- See customer preferences and custom field values
- Check newsletter subscription status
- Review customer LTV and RFM scores
- Manage customer segments

Use **Customers > Analytics** when you need to:
- Identify high-value customers
- Create marketing segments (e.g., "customers who haven't ordered in 90 days")
- Analyze customer lifetime value trends
- Export customer lists for campaigns

## Tips

- **Customer profiles are created automatically** — When a customer places their first order (guest or registered), Spwig creates a CustomerProfile and CustomerMetrics record for analytics.
- **Staff can also be customers** — If a staff member places an order on the storefront, they get a CustomerProfile. This is normal and does not affect their admin access.
- **Guest accounts clutter the user list** — Use the customer profile interface to focus on real, engaged customers. The user list includes all guest accounts.
- **Segment by is_staff=False** — When exporting customer lists for email campaigns, always filter for `is_staff=False` to exclude team members.
- **OAuth accounts are also accounts** — When a customer logs in via Google or Facebook, Spwig creates an account and links it to their OAuth profile. The email field is populated from the OAuth provider.
