---
slug: staff-roles
title_i18n_key: Staff Roles & Permissions
category: store-config
component: staff_roles
keywords:
  - staff
  - role
  - permission
  - access control
  - admin access
  - POS permission
  - staff member
  - store owner
  - store manager
  - cashier
  - clone role
url_patterns:
  - /admin/staff_roles/staffrole/
  - /admin/accounts/staffmember/
related:
  - store-settings
published: true
---

Staff roles let you control exactly what each team member can see and do — in both the admin panel and the POS terminal. Define roles with specific permissions, then assign them to staff members. A user can hold multiple roles, and their effective permissions are the combination of all assigned roles.

![Staff roles](/static/core/admin/img/help/staff-roles/role-list.webp)

## How It Works

1. You create **roles** that define a set of permissions (e.g., "Order Manager", "Cashier")
2. Each role controls two types of access: **admin panel permissions** and **POS permissions**
3. You **assign roles** to staff members from their profile page
4. A staff member's effective permissions are the **union** of all their roles — if any role grants access, the user has it
5. Permissions are **cached** for performance and automatically refreshed when roles change

## Predefined Roles

Spwig includes 7 built-in roles that cover the most common team structures. These cannot be deleted, but you can create custom roles for more specific needs.

| Role | Access | Description |
|------|--------|-------------|
| **Store Owner** | Admin + POS | Full access to everything. For the primary store administrator. |
| **Store Manager** | Admin + POS | Day-to-day operations — full access to products, orders, customers, marketing, and search. View-only for design, email, payments, and settings. |
| **Content Editor** | Admin | Manages pages, blog posts, design, and media. View-only for products. |
| **Order Manager** | Admin | Handles orders, shipping, returns, and customer service. View-only for products. |
| **Marketing Manager** | Admin | Manages promotions, vouchers, affiliate, loyalty, and referral programs. View-only for products, customers, and media. |
| **Cashier** | POS only | Frontline POS staff. Can process sales and check gift card balances. No discounts, refunds, or cash management. |
| **Senior Cashier** | POS only | Experienced POS staff. Can process refunds, apply discounts (up to 25%), manage cash, and close shifts. |

## Creating a Custom Role

Navigate to **Settings > Staff Roles** and click **Add Role**.

### General Settings

| Setting | Description |
|---------|-------------|
| **Display Name** | The role name shown in the admin (e.g., "Warehouse Staff") |
| **Description** | A brief explanation of what this role is for |
| **Sort Order** | Controls the display order in the role list |
| **Icon** | Choose from 20 icons to visually identify the role |
| **Badge Color** | Color used for role badges (Blue, Green, Orange, Red, Teal, Gray) |
| **Admin Panel** | Toggle whether this role grants admin backend access |
| **POS Terminals** | Toggle whether this role grants POS terminal access |

### Admin Permission Categories

The admin permissions tab organizes all platform features into 13 categories. For each category, you set one of three access levels:

- **None** — No access to this area (menu items are hidden)
- **View** — Read-only access (can see data but not change it)
- **Full** — Complete access (can view, create, edit, and delete)

![Permission categories](/static/core/admin/img/help/staff-roles/permission-categories.webp)

| Category | What It Controls |
|----------|-----------------|
| **Product Catalog** | Products, categories, brands, attributes, stock, warehouses, digital assets |
| **Orders & Fulfillment** | Orders, refunds, returns, shipments, shipping configuration |
| **Customers** | Customer profiles, segments, analytics |
| **Content & Pages** | Pages, blog posts, announcements, forms |
| **Design & Theme** | Themes, header/footer templates, menus, design tokens, custom CSS |
| **Marketing & Promotions** | Promotions, vouchers, affiliate, loyalty, referrals, product feeds |
| **Media Library** | Images, videos, folders, tags |
| **Email System** | Email accounts, templates, delivery queue |
| **Payments & Billing** | Payment providers, transactions, webhooks, subscriptions, exchange rates |
| **Search** | Search settings, synonyms, redirects, analytics |
| **Store Settings** | Site settings, geolocation, country mappings, business rules |
| **POS Management** | POS terminals, shifts, cash movements, receipt templates |
| **Users & Roles** | Staff user accounts, roles, API tokens |

When a user has multiple roles, the **highest** access level wins. For example, if Role A grants "View" to Products and Role B grants "Full", the user gets "Full" access.

### POS Permission Flags

If the role grants POS access, the POS Permissions tab lets you fine-tune exactly what a POS operator can do. These are separate from admin permissions and are checked at the POS terminal.

![POS permissions](/static/core/admin/img/help/staff-roles/pos-permissions.webp)

| Group | Permission | Description |
|-------|-----------|-------------|
| **General** | POS Access | Can use the POS system at all |
| **Sales & Discounts** | Manual Discounts | Can apply manual line-item or cart-level discounts |
| | Maximum Discount % | The highest discount percentage allowed (0–100) |
| | Price Override | Can override product prices at the register |
| **Refunds & Voids** | Process Refunds | Can process refunds on POS orders |
| | Void Orders | Can void POS orders from the current shift |
| **Gift Cards** | Issue Gift Cards | Can issue new gift cards at the register |
| | Check Gift Card Balance | Can look up gift card balances |
| **Cash Management** | Cash Management | Can perform cash-in and cash-out operations |
| | Open Cash Drawer | Can open the cash drawer without a sale |
| | Close Shifts | Can close shifts and perform cash reconciliation |
| **Reporting** | View POS Reports | Can view shift reports and sales summaries |
| **Inventory** | Stock Adjustments | Can adjust stock levels (receive, damage, recount, return) |

For boolean permissions, if **any** of a user's roles enables it, the user has it. For the Maximum Discount %, the **highest** value across all roles applies.

## Managing Staff Members

Navigate to **Settings > Staff Management** to view and manage your team.

### Staff List

The staff list shows all users with staff access. For each member, you can see:
- **Name and email**
- **Assigned roles** (shown as colored badges)
- **Access type** — Admin only, POS only, or Both
- **2FA status** — Whether two-factor authentication is enabled
- **Active/Inactive** status

Use the filters to narrow by role, access type, or 2FA status.

### Assigning Roles to Staff

1. Click on a staff member to open their profile
2. In the **Roles** section, you'll see cards for each available role
3. Click the toggle on any role card to assign or remove it
4. Changes take effect immediately — no save button needed
5. The **Effective Permissions** summary below shows the combined result of all assigned roles

### Adding a New Staff Member

1. Navigate to **Settings > Staff Management** and click **Add Staff Member**
2. Enter the user's email, first name, and last name
3. Set a temporary password
4. Assign one or more roles
5. The user can now log in with the access their roles provide

## Cloning Roles

To create a new role based on an existing one:

1. Open the role you want to copy
2. Click **Clone Role** at the bottom of the page
3. A new role is created with all the same permissions
4. Rename it and adjust permissions as needed
5. Save the new role

This is useful when you need a role that's similar to an existing one with minor differences — for example, a "Junior Manager" based on "Store Manager" but with fewer permissions.

## How Permissions Are Applied

### Admin Panel

- **Menu visibility** — Sidebar sections are hidden for categories where the user has "None" access
- **Page access** — Attempting to visit a restricted page shows a permission error
- **Action restrictions** — With "View" access, edit and delete buttons are hidden and save actions are blocked
- **Superuser bypass** — Superuser accounts always have full access regardless of role assignments

### POS Terminal

- **Login gate** — Only users with at least one role that has "POS Terminals" enabled can log in to the POS
- **Feature toggles** — POS buttons and actions (refund, discount, void, etc.) are shown or hidden based on the user's merged POS permissions
- **Discount cap** — The Maximum Discount % enforces a hard limit on how large a discount a POS operator can apply
- **API enforcement** — All POS permissions are checked server-side at the API layer, not just in the UI

## Tips

- **Start with predefined roles** — The 7 built-in roles cover most team structures. Create custom roles only when you need more specific access controls.
- **Use the clone feature** — When you need a role similar to an existing one, clone it and adjust rather than building from scratch.
- **Assign multiple roles when needed** — A staff member who handles both orders and marketing can be assigned both "Order Manager" and "Marketing Manager" roles. Permissions combine automatically.
- **Separate admin and POS access** — Cashiers typically don't need admin access, and office staff don't need POS access. Use the access toggles to keep things clean.
- **Set discount limits for POS staff** — The Maximum Discount % prevents cashiers from applying excessive discounts. Set it to 0 for no discounts, or a reasonable cap like 10–25% for senior staff.
- **Review roles periodically** — As your team grows, audit role assignments to ensure staff have the minimum access needed for their job. Remove roles when people change positions.
- **Enable 2FA for sensitive roles** — Staff with access to payments, settings, or user management should have two-factor authentication enabled for security.
