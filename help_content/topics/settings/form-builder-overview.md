---
slug: form-builder-overview
title_i18n_key: Form Builder Overview
category: store-config
component: form_builder
keywords:
  - form builder
  - custom forms
  - contact forms
  - survey forms
  - form creation
  - drag and drop forms
  - multi-step forms
  - form responses
  - form submissions
  - visual form builder
  - online forms
  - web forms
  - data collection
  - form management
url_patterns:
  - /admin/form_builder/form/
  - /admin/form-builder/forms/*/builder/
related:
  - form-builder-fields
  - page-builder
published: true
---

The Form Builder creates custom forms for data collection—contact forms, surveys, applications, registrations, and more. Build forms visually with drag-and-drop fields, configure validation rules, enable multi-step workflows, and collect responses with detailed analytics. Forms integrate seamlessly with Page Builder elements, embedding anywhere on your site. All submissions are stored in the database with full metadata (IP address, browser, time to complete) for analysis and export.

Use the Form Builder when you need to collect structured data from customers, whether simple contact information or complex multi-page applications.

## What is the Form Builder?

The Form Builder is a visual drag-and-drop tool for creating custom forms without code:

**Form Types Supported**:
- Contact forms (name, email, message)
- Customer surveys (ratings, feedback, NPS)
- Product registrations (warranty, support)
- Job applications (resume upload, multi-step)
- Event registrations (attendee info, preferences)
- Service requests (detailed requirements)
- Newsletter signups (with checkboxes for preferences)

**Key Features**:
- **22 field types** - Text, email, phone, file upload, ratings, product selectors, and more
- **Multi-step forms** - Break long forms into logical steps with progress tracking
- **Conditional logic** - Show/hide fields based on user responses
- **Validation rules** - Required fields, min/max length, custom regex patterns
- **Spam protection** - Honeypot fields or Google reCAPTCHA v3
- **Response analytics** - Track completion time, IP address, browser, referrer
- **CSV export** - Download all responses for analysis in Excel/Google Sheets
- **Multi-language** - Translate form labels and messages to all active languages

## Creating Your First Form

Navigate to **Settings > Pages > Forms** to access the form manager:

**Step 1: Create New Form**
- Click **+ Create New Form**
- Enter form name (internal identifier, not shown to customers)
- Enter form title (displayed as heading above form)
- Optional: Add description (help text shown below title)

**Step 2: Add Fields**
- Click **Edit Form Design** to open visual builder
- Drag field types from left sidebar to canvas
- Click field to configure in right panel
- Set label, placeholder, help text
- Toggle required status
- Add validation rules

**Step 3: Configure Form Settings**
- Set submit button text (default: "Submit")
- Customize success message (shown after submission)
- Choose spam protection (honeypot recommended)
- Toggle "Require Login" if needed
- Enable "Multi-step Form" for complex forms

**Step 4: Activate Form**
- Toggle **Active** status on
- Only active forms accept submissions
- Save form

**Step 5: Use in Page Builder**
- Add **Form** element to any page
- Select your form from dropdown
- Form inherits page styling
- Submissions sent to backend automatically

## Single-Page vs Multi-Step Forms

**Single-Page Forms** (default):
- All fields displayed at once
- Scroll to see all fields
- Submit button at bottom
- Best for: Contact forms, short surveys, simple data collection

**Multi-Step Forms**:
- Fields organized into numbered steps
- Progress bar shows current step
- Back/Next navigation buttons
- Submit on final step only
- Optional: Save partial responses (draft mode)
- Best for: Job applications, registrations, complex surveys, checkout flows

**Enabling Multi-Step**:
1. Toggle "Multi-step Form" in form settings
2. Click "Steps" tab in right panel
3. Add step (e.g., "Personal Info", "Contact Details", "Preferences")
4. Assign fields to steps using step dropdown when editing field
5. Reorder steps by dragging
6. Set step properties: title, description, skippable

**Multi-Step Benefits**:
- Reduces form abandonment (psychological: "only 3 questions on this page")
- Logical grouping improves UX
- Progress indicator motivates completion
- Optional draft saving for long forms

## Form Settings Explained

**Basic Settings**:
- **Internal Name** - How you identify the form in admin (not visible to customers)
- **Slug** - URL-friendly identifier (auto-generated, used in API endpoints)
- **Form Title** - Heading displayed above form
- **Description** - Optional help text shown below title
- **Submit Button Text** - Customize button label (e.g., "Send Message", "Apply Now")

**Messages**:
- **Success Message** - Shown after successful submission (default: "Thank you for your submission!")
- **Error Message** - Shown if submission fails (default: "An error occurred. Please try again.")

**Security & Access**:
- **Active** - Only active forms accept submissions (inactive forms show "Form unavailable")
- **Require Login** - Restrict to authenticated users only (anonymous users see login prompt)

**Spam Protection**:
- **None** - No protection (not recommended, bots will spam)
- **Honeypot Field** - Invisible field catches bots (recommended for most merchants)
- **Google reCAPTCHA v3** - Requires site key and secret key from Google (strongest protection)

**Advanced Features**:
- **Multi-step Form** - Enable step-by-step workflow
- **Save Partial Responses** - Allow users to save progress and resume later (multi-step only)

## Spam Protection Options

**Honeypot Field (Recommended)**:
- Invisible field added to form
- Bots fill it (humans can't see it)
- Submissions with filled honeypot rejected
- No configuration required
- No CAPTCHA frustration for users
- Effective against 95%+ of spam bots

**Google reCAPTCHA v3**:
- Invisible background score (0.0-1.0)
- No "click the traffic lights" challenge
- Requires setup:
  1. Create account at google.com/recaptcha/admin
  2. Generate site key and secret key
  3. Enter keys in form builder settings
- More robust than honeypot
- Use when honeypot insufficient

**None**:
- No spam protection
- Only use for internal forms or testing
- Public forms will be spammed heavily

## Managing Form Responses

View all submissions at **Settings > Pages > Forms > [Form Name] > Responses**:

**Response List View**:
- Status: draft, submitted, completed
- Submitter: email (if logged in) or "Anonymous"
- IP address and location (if GeoIP enabled)
- Submitted date/time
- Time to complete (seconds)

**Response Detail**:
- All field values with labels
- Metadata: browser, referrer, language
- Progress tracking (multi-step): current step, completed steps
- Action results (if form triggers actions)

**Response Filtering**:
- Filter by form, status, date range
- Search by submitter email or IP address
- Sort by submission date, completion time

**Response Export**:
- Click **Export to CSV** button
- Downloads `{form-slug}_responses_{date}.csv`
- Header row: Submitted At, User, IP, Status, [Field Labels]
- One response per row
- Open in Excel, Google Sheets, or data analysis tools

## Using Forms in Pages

**Embedding Forms**:
1. Open page in Page Builder
2. Add **Form** element from elements panel
3. Select form from dropdown
4. Customize form container styling (background, padding, border)
5. Save and publish page

**Form Renders With**:
- Form title and description (from form settings)
- All fields in order (single-page) or current step (multi-step)
- Submit button with custom text
- Success/error messages after submission

**Styling Inheritance**:
- Forms inherit page theme styling
- Buttons use theme button styles
- Input fields use theme input styles
- Custom CSS class can be added to fields for specific styling

## Form Builder Interface

**Left Sidebar - Field Library**:
- Organized by category (Text, Selection, Rating, Advanced)
- Drag field to canvas or click to add
- Search to quickly find field types

**Main Canvas - Fields Editor**:
- Drag handle (≡) to reorder fields
- Click field to select and edit
- Delete button (×) on each field
- Visual preview of field as configured
- Empty state with drop zone instructions

**Right Sidebar - Properties Panel**:
- **Form Settings Tab** - Basic info, messages, spam protection
- **Field Settings Tab** - Configure selected field (label, validation, etc.)
- **Steps Tab** - Manage steps (multi-step forms only)
- **Conditional Rules Tab** - Add show/hide logic based on responses

**Toolbar Features**:
- **Undo/Redo** - Full edit history
- **Preview** - Test form functionality
- **Save** - Auto-saves every 3 seconds while editing
- **Translations** - Translate form text to other languages

## Common Form Examples

**Contact Form**:
- Fields: Full Name (required), Email (required), Phone, Message (required)
- Submit button: "Send Message"
- Success: "Thanks for contacting us! We'll reply within 24 hours."

**Product Feedback Survey**:
- Step 1: Star rating, Likert scale agreement
- Step 2: NPS score, improvement suggestions
- Conditional: If rating < 3, require improvement feedback

**Job Application**:
- Step 1: Personal info (name, email, phone)
- Step 2: Experience (resume upload, years experience, references)
- Step 3: Availability (start date, salary expectations)
- Partial save enabled (applicants can resume later)

**Newsletter Signup with Preferences**:
- Email (required)
- Checkbox group: Interests (Products, Sales, Blog Updates)
- reCAPTCHA enabled (prevent fake signups)

## Tips

- **Start with single-page** - Add multi-step only if form exceeds 10 fields
- **Use honeypot first** - Only upgrade to reCAPTCHA if spam persists
- **Test before publishing** - Use preview mode to verify validation and flow
- **Export regularly** - Download response CSV weekly for backup
- **Monitor completion time** - If average >5 minutes, form may be too long
- **Use conditional logic** - Hide irrelevant fields to reduce form length perception
- **Enable partial save for long forms** - Reduces abandonment on multi-step applications
- **Translate form labels** - Use built-in translation system for multi-language sites
- **Require login for sensitive data** - Prevents anonymous spam, links submissions to user accounts
- **Keep success messages specific** - "We'll reply within 24 hours" better than "Thank you"
