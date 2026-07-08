---
slug: managing-affiliate-applications
title_i18n_key: Managing Affiliate Applications
category: affiliates
component: affiliate
keywords:
  - affiliate application
  - approve affiliate
  - reject affiliate
  - affiliate approval
  - manage affiliates
  - affiliate review
  - pending applications
  - affiliate membership
  - review affiliate
  - affiliate onboarding
url_patterns:
  - /en/affiliate/merchant/applications/
  - /en/admin/affiliate/affiliateprogrammembership/
related:
  - creating-affiliate-programs
  - affiliate-program-overview
  - commission-management
published: true
---

When potential partners apply to join your affiliate program, they appear in your applications queue awaiting review. This guide shows you how to evaluate, approve, and reject affiliate applications to build a network of quality partners who align with your brand.

Managing applications carefully ensures you work with trustworthy affiliates who will represent your store professionally and drive genuine sales.

![Applications List View](/static/core/admin/img/help/managing-affiliate-applications/applications-list.webp)

## Application Sources

Affiliate applications reach your queue through several channels:

### Public Portal Applications
Most applications come from the public affiliate portal at `/affiliate/` on your store. When potential affiliates click **Become an Affiliate**, they complete a registration form that creates an application record.

### Guest vs Registered Users
If you've enabled **Allow Guest Registration** in affiliate settings, non-customers can apply directly. Otherwise, users must first create a customer account on your store before they can apply to become affiliates.

### Manual Review Requirement
When **Require Approval** is enabled in your affiliate settings (recommended), all applications land in a **Pending** state waiting for your review. If disabled, applications are auto-approved and affiliates gain immediate access to their dashboard.

## Viewing Applications

Navigate to **Affiliate Program > Applications** (or **Marketing > Affiliate Memberships** in the admin) to see all program applications.

The list view shows:

| Column | Description |
|--------|-------------|
| **Affiliate** | The applicant's name and email |
| **Program** | Which affiliate program they're applying to |
| **Status** | Pending, approved, or rejected |
| **Applied Date** | When they submitted the application |
| **Payment Method** | Their preferred payout method (PayPal or bank transfer) |

### Filtering Applications
Use the admin filters to narrow down applications:

- **Status**: View only pending applications awaiting review
- **Program**: Filter by specific program if you run multiple affiliate programs
- **Date Range**: Find applications from a specific time period

### Pending Applications Badge
The admin sidebar shows a badge count next to **Affiliates** when you have pending applications requiring action.

## Reviewing an Application

Click any application to view the full applicant profile. This detail view shows all information you need to make an informed approval decision.

![Application Detail Card](/static/core/admin/img/help/managing-affiliate-applications/application-detail-card.webp)

### Affiliate Profile Information
Review these key details about the applicant:

**Basic Information**
- **Email Address**: Used for login and communication
- **Company/Business Name**: Their organization (if applicable)
- **Website URL**: Their primary promotional platform
- **Phone Number**: Contact information

**Payment Information**
- **Payment Method**: PayPal or bank transfer
- **PayPal Email**: Required if they selected PayPal payouts
- **Bank Details**: Required if they selected bank transfer (account number, routing number, SWIFT code)

**Promotional Channels**
Many applications include notes about where the affiliate plans to promote your products — social media accounts, YouTube channels, email lists, or blogs.

### Program Details
Check which program they applied to and review its commission rate, cookie lifetime, and minimum payout threshold. Make sure the applicant is a good fit for the program's target audience.

### Application History
If an applicant has been rejected previously or has applied to multiple programs, this history appears in the detail view.

## Approval Criteria

Use this checklist to evaluate each application consistently:

### Business Legitimacy
- [ ] **Active Website or Social Media**: Does the applicant have a live platform with real content?
- [ ] **Relevant Audience**: Does their audience match your target customer demographic?
- [ ] **Quality Content**: Is their content professional, well-written, and aligned with your brand values?
- [ ] **Established Platform**: Do they have an engaged following or meaningful traffic?

### Payment Information
- [ ] **Valid Payment Details**: Have they provided a working PayPal email or complete bank account information?
- [ ] **Matching Identity**: Do the payment details align with their business name or personal information?

### Brand Alignment
- [ ] **Appropriate Fit**: Does their content, tone, and style match your brand image?
- [ ] **No Conflicts**: Are they already promoting direct competitors?
- [ ] **Professional Standards**: Do they maintain quality standards you're comfortable associating with?

### Fraud Prevention
- [ ] **No Red Flags**: Check for signs like generic email addresses, incomplete profiles, or suspicious website patterns
- [ ] **No Previous Violations**: Have they been rejected before for fraud or terms violations?
- [ ] **Reasonable Expectations**: Are their stated promotional plans realistic and achievable?

If an application meets all criteria, approve it. If it fails any critical check (fraud risk, brand misalignment, invalid payment info), reject it with a clear reason.

## Approving Applications

Follow these steps to approve one or more applications:

### Single Application Approval
1. Open the application detail page
2. Review all profile information carefully
3. Verify payment details are complete and valid
4. Click the **Save and Continue Editing** button if you need to make notes
5. Select **Approve** from the status dropdown
6. Click **Save**

### Bulk Approval
For multiple qualified applications:

1. Navigate to the applications list at **Affiliate Program > Applications**
2. Check the boxes next to applications you want to approve
3. Select **Approve selected applications** from the **Actions** dropdown
4. Click **Go**
5. Confirm the bulk action when prompted

### What Happens After Approval
When you approve an application:

- The affiliate's status changes to **Approved**
- They receive an email notification (if email templates are configured)
- They gain access to the affiliate dashboard to generate tracking links
- They can start promoting your products and earning commissions

Approved affiliates appear in the affiliates list with an **Active** status and can immediately begin promoting your program.

## Rejecting Applications

Reject applications that don't meet your criteria to protect your brand and prevent fraud.

### When to Reject
Common reasons for rejection:

- **No Active Platform**: Applicant has no website, blog, or social media presence
- **Competitor Conflicts**: They primarily promote direct competitors
- **Brand Misalignment**: Their content style, language, or values clash with your brand
- **Invalid Payment Info**: Missing or clearly fake payment details
- **Suspicious Activity**: Generic email, incomplete profile, or fraud indicators
- **Terms Violations**: Previous affiliate who violated program terms

### How to Reject
1. Open the application detail page
2. Review the applicant's information to confirm rejection is appropriate
3. Add a note in the **Notes** field explaining the reason (internal reference only)
4. Change the **Status** dropdown to **Rejected**
5. Click **Save**

### After Rejection
When you reject an application:

- The affiliate's status changes to **Rejected**
- They lose access to the affiliate dashboard (if they had any)
- They cannot create tracking links or earn commissions
- No automatic notification is sent (you can customize this in email templates)

Rejected affiliates remain in your database for record-keeping. You can later change their status to **Approved** if circumstances change.

## Auto-Approve Settings

Control whether applications require manual review in your affiliate program configuration:

### Manual Review (Recommended)
Navigate to your program at **Marketing > Affiliate Programs** and ensure **Auto-Approve** is **unchecked**. This setting means:

- All applications start as **Pending**
- You review each applicant before they gain access
- Better quality control and fraud prevention
- More work for you, but safer for your brand

Use manual review when you want to vet partners carefully, work with select influencers, or maintain strict brand standards.

### Auto-Approve Mode
Check **Auto-Approve** in your program settings to automatically accept all applications. This means:

- Applications skip the pending state and go straight to **Approved**
- Affiliates gain immediate access to their dashboard
- Less work for you, but higher fraud risk
- Best for open referral programs with many partners

Use auto-approve for general referral programs where you want to maximize participation and accept some quality variance.

## Bulk Actions

Process multiple applications efficiently using admin interface's bulk actions:

### Approve Multiple Applications
1. Navigate to **Affiliate Program > Applications**
2. Use filters to show only **Pending** applications
3. Check the boxes for all applications you want to approve
4. Select **Approve selected applications** from the Actions dropdown
5. Click **Go** and confirm

### Filter for Efficiency
Combine filters to process applications in batches:

- **Program + Status**: Approve all pending applications for your influencer program
- **Date + Status**: Review applications from the past week
- **Payment Method + Status**: Process all PayPal applicants together

This batching approach helps you review similar applications together, making it easier to apply consistent standards.

## Tips

- **Review within 24-48 hours** — Fast response times create a positive first impression and prevent applicants from losing interest or applying to competitors
- **Verify payment details early** — Catching invalid PayPal emails or incomplete bank details at the application stage prevents payout headaches later
- **Check their content first** — Visit the applicant's website or social media profiles before approving to verify they have real content and an engaged audience
- **Document rejection reasons** — Use the notes field to record why you rejected an application. This helps maintain consistency and protects you if the applicant reapplies later
- **Set clear program requirements** — Update your affiliate portal landing page to clearly state what you're looking for in partners (minimum audience size, content type, etc.) to reduce unqualified applications
- **Watch for repeat applicants** — Some rejected affiliates reapply with different email addresses. Check the website URL, company name, and payment details to catch duplicates
- **Start strict** — It's easier to approve more liberally over time than to remove problematic affiliates later. Begin with strict approval criteria and loosen them if you need more partners
