---
slug: form-builder-fields
title_i18n_key: Form Builder Fields and Validation
category: store-config
component: form_builder
keywords:
  - form fields
  - field types
  - form validation
  - required fields
  - conditional logic
  - field configuration
  - text fields
  - file upload
  - rating fields
  - dropdown fields
  - checkbox fields
  - form rules
  - dynamic forms
  - field options
url_patterns:
  - /admin/form-builder/forms/*/builder/
related:
  - form-builder-overview
  - page-builder
published: true
---

Form fields are the building blocks of your forms—each field collects one piece of data from users. The Form Builder offers 22 field types ranging from simple text inputs to advanced rating scales and product selectors. Configure each field with labels, validation rules, help text, and conditional logic to create dynamic forms that adapt based on user responses. Fields can be required or optional, validated with regex patterns, and styled with custom CSS classes.

Use this guide to understand all available field types, when to use each one, and how to configure validation and conditional logic.

## Field Configuration Basics

Every field shares these common settings:

**Identity**:
- **Field Name** - Machine name for data storage (no spaces, use underscores: `email_address`)
- **Field Type** - Determines input behavior and rendering
- **Step Assignment** - Which step this field belongs to (multi-step forms only)

**Display**:
- **Label** - Question or prompt shown to users (e.g., "What is your email address?")
- **Placeholder** - Hint text inside input (e.g., "you@example.com")
- **Help Text** - Additional guidance below field (e.g., "We'll never share your email")
- **Default Value** - Pre-filled value (users can change it)

**Layout**:
- **Width** - Full (100%), Half (50%), or One-Third (33%) of form width
- **CSS Class** - Additional styling classes for custom design
- **Order** - Position within step (drag to reorder)

**Validation**:
- **Required** - Toggle required status (red asterisk appears on label)
- **Min/Max Length** - Character limits (text fields)
- **Min/Max Value** - Numeric limits (number fields)
- **Validation Pattern** - Custom regex for complex validation
- **Error Message** - Custom text shown when validation fails

## Text Input Fields

**Single Line Text** (`text`):
- Basic text input for short responses
- Validation: min/max length, regex pattern
- Use case: Names, addresses, product codes, short answers
- Example: "Full Name", "Street Address", "Company Name"

**Multi-line Text** (`textarea`):
- Expandable text area for longer content (3-10 rows)
- Validation: min/max length
- Use case: Comments, feedback, detailed descriptions, messages
- Example: "Tell us about your experience", "Additional notes"

**Email Address** (`email`):
- Email-specific validation (requires @ and domain)
- Mobile keyboards show @ key prominently
- Use case: Contact email, newsletter signups, account creation
- Example: "Email Address", "Work Email"

**Phone Number** (`phone`):
- Formats phone numbers automatically
- Mobile keyboards show numeric layout
- Validation: configurable pattern (international formats supported)
- Use case: Contact phone, emergency contact, appointment scheduling
- Example: "Phone Number", "Mobile", "Contact Number"

**Number** (`number`):
- Numeric input with increment/decrement controls
- Validation: min/max value, step increment
- Returns number (not string) in responses
- Use case: Quantities, ages, years of experience, budget amounts
- Example: "How many employees?", "Your age", "Years in business"

**URL** (`url`):
- URL validation (requires http:// or https://)
- Mobile keyboards show .com key
- Use case: Website, LinkedIn profile, portfolio link
- Example: "Company Website", "Portfolio URL"

## Selection Fields

**Dropdown Select** (`select`):
- Single option selection from dropdown menu
- Configuration: array of {value, label} options
- Supports default selection
- Use case: Categories, states/countries, status selection
- Example: "Select your country", "Department", "How did you hear about us?"
- Best for: 5+ options (fewer options use radio instead)

**Radio Buttons** (`radio`):
- Single choice from visible options (all options displayed)
- Configuration: array of {value, label} options
- Better UX than select for 2-4 options
- Use case: Yes/no questions, gender, preferences with few choices
- Example: "Would you recommend us?", "Preferred contact method"

**Checkbox** (`checkbox`):
- Single toggle checkbox (on/off)
- Returns true/false in responses
- Use case: Terms acceptance, agreements, single preference
- Example: "I agree to terms and conditions", "Subscribe to newsletter"

**Checkbox Group** (`checkbox_group`):
- Multiple selection from options (users can select 0, 1, or many)
- Configuration: array of {value, label} options
- Returns array of selected values
- Use case: Multi-select preferences, interests, features needed
- Example: "Which topics interest you?", "Select all that apply"

## Rating Fields

**Star Rating** (`rating_stars`):
- Visual star rating scale (typically 1-5 stars)
- Configuration:
  - `max_stars`: 3-10 stars (default: 5)
  - `allow_half`: true/false for half-star ratings
  - `icon`: fa-star (default) or fa-heart
  - `color`: hex color code (default: #FFD700 gold)
- Use case: Product ratings, service quality, satisfaction scores
- Example: "Rate your experience", "How was our service?"

**Likert Scale** (`rating_likert`):
- Statement rating scale: strongly disagree → strongly agree
- Configuration:
  - `scale_type`: 5_point (1-5) or 7_point (1-7)
  - `labels`: customize endpoint text (left: "Strongly Disagree", right: "Strongly Agree")
- Returns numeric value (1-5 or 1-7)
- Use case: Survey statements, agreement scales, sentiment measurement
- Example: "The product meets my needs", "Customer service was helpful"

**Net Promoter Score (NPS)** (`rating_nps`):
- 0-10 scale: "Not at all likely" to "Extremely likely"
- Configuration:
  - `low_label`: left endpoint text (default: "Not at all likely")
  - `high_label`: right endpoint text (default: "Extremely likely")
- Returns 0-10 value (0-6 = detractors, 7-8 = passives, 9-10 = promoters)
- Use case: NPS surveys, recommendation likelihood, loyalty measurement
- Example: "How likely are you to recommend us to a friend?"

## Advanced Fields

**File Upload** (`file`):
- Single or multiple file uploads
- Configuration:
  - `max_size_mb`: file size limit per file (default: 5MB)
  - `allowed_types`: array of extensions (e.g., ["pdf", "doc", "docx", "jpg", "png"])
  - `max_files`: maximum number of files (1 for single, 2+ for multiple)
- Returns file path(s) in responses
- Files stored in `/media/form_uploads/{form-slug}/`
- Use case: Resume uploads, document submissions, photo attachments
- Example: "Upload your resume", "Attach supporting documents"

**Product Selector** (`product_select`):
- Multi-select from your product catalog
- Configuration:
  - `category_filters`: limit to specific categories (array of category IDs)
  - `max_selections`: 1 for single product, 2+ for multiple
  - `display_mode`: "list" (default) or "grid" (with thumbnails)
- Returns product IDs/SKUs in responses
- Use case: Product recommendations, wishlists, feedback surveys, bundles
- Example: "Which products are you interested in?", "Select your favorite items"

**Date** (`date`):
- Date picker interface (calendar popup)
- Returns ISO format (YYYY-MM-DD)
- Validation: min/max date
- Use case: Birth dates, event dates, appointment scheduling, deadlines
- Example: "Date of Birth", "Preferred Appointment Date"

**Time** (`time`):
- Time picker (hours and minutes)
- Returns ISO time format (HH:MM)
- Use case: Appointment times, availability windows
- Example: "Preferred Time", "Available After"

**Date & Time** (`datetime`):
- Combined date and time picker
- Returns full ISO datetime
- Use case: Event scheduling, appointment booking
- Example: "Event Start Time", "Delivery Window"

## Layout Fields (Non-Input)

**Section Heading** (`heading`):
- Heading text to organize form sections
- Configuration: heading level (h2, h3, h4)
- No data collection
- Use case: Breaking long forms into logical sections
- Example: "Personal Information", "Contact Details", "Preferences"

**Descriptive Paragraph** (`paragraph`):
- Rich text block for instructions or information
- No data collection
- Supports basic formatting (bold, italic, links)
- Use case: Step instructions, legal disclaimers, explanations
- Example: Privacy policy notice, GDPR consent explanation

**Divider Line** (`divider`):
- Visual horizontal line separator
- No data collection
- Use case: Visual organization between sections

**Hidden Field** (`hidden`):
- Invisible field with programmatic value
- Configuration: `default_value` (required)
- No label or help text shown to users
- Use case: UTM parameters, tracking data, session IDs, referral codes
- Example: Hidden field with value from URL parameter

## Field Validation Rules

**Required Fields**:
- Toggle "Required" checkbox in field settings
- Red asterisk (*) appears next to label
- Form cannot be submitted if required fields are empty
- Custom error: "This field is required" (or custom message)

**Min/Max Length** (text fields):
- Set minimum character count: prevents too-short responses
- Set maximum character count: prevents excessive input
- Example: Message field requires min 10 characters (prevents "ok" responses)

**Min/Max Value** (number fields):
- Set minimum numeric value: prevents negative ages, quantities
- Set maximum numeric value: caps input to reasonable range
- Example: Age field requires min 18, max 120

**Validation Pattern** (regex):
- Custom regular expression for complex validation
- Common patterns:
  - ZIP code: `^\d{5}(-\d{4})?$` (US format)
  - Phone: `^\(\d{3}\) \d{3}-\d{4}$` (US format)
  - Product code: `^[A-Z]{2}\d{4}$` (2 letters, 4 digits)
- Custom error message required when using patterns

**File Validation**:
- Max file size: prevents large uploads (default 5MB)
- Allowed types: whitelist specific extensions (security)
- Example: Resume field allows ["pdf", "doc", "docx"], max 2MB

## Conditional Logic

Create dynamic forms where fields appear/disappear based on user responses:

**How Conditional Rules Work**:
1. User answers "source field" (the trigger)
2. System evaluates rule: operator + comparison value
3. If condition is true, action executes (show/hide/require field or step)
4. Multiple rules can cascade (rule A triggers rule B)

**Available Operators**:
- **Equals** (`equals`): exact match (e.g., country equals "US")
- **Not Equals** (`not_equals`): anything except value
- **Contains** (`contains`): text includes substring (case-insensitive)
- **Greater Than** (`greater_than`): numeric comparison (e.g., age > 18)
- **Less Than** (`less_than`): numeric comparison (e.g., rating < 3)
- **Is Empty** (`is_empty`): field has no value
- **Is Not Empty** (`is_not_empty`): field has any value
- **In List** (`in_list`): value is one of ["Option1", "Option2"]

**Available Actions**:
- **Show Field** - Display hidden field
- **Hide Field** - Conceal field (value cleared if hidden)
- **Require Field** - Make field mandatory
- **Unrequire Field** - Make field optional
- **Set Value** - Populate field with a value
- **Show Step** - Display hidden step (multi-step only)
- **Hide Step** - Conceal step (multi-step only)
- **Skip to Step** - Jump to specific step (multi-step only)

**Example Rules**:
- IF `contact_method` EQUALS "phone" THEN show_field `phone_number`
- IF `rating` LESS_THAN "3" THEN require_field `improvement_feedback`
- IF `country` IN_LIST ["US", "CA"] THEN show_step `shipping_details`
- IF `budget` GREATER_THAN "10000" THEN show_field `enterprise_features`

**Creating Conditional Rules**:
1. Click "Conditional Rules" tab in right panel
2. Click "Add Rule"
3. Select source field (trigger)
4. Select operator (how to compare)
5. Enter comparison value (what to compare against)
6. Select action (what to do)
7. Select target (field or step affected)
8. Optional: Set priority (higher priority rules evaluate first)
9. Save rule

**Rule Priority**:
- Higher numbers evaluate first (priority 100 before priority 10)
- Use priority when rules conflict or cascade
- Example: Rule A (priority 100) shows field, Rule B (priority 50) requires it (A executes first, then B)

## Common Field Patterns

**Contact Form**:
- Full Name (text, required)
- Email (email, required)
- Phone (phone)
- Subject (select with options: "Sales", "Support", "Partnership")
- Message (textarea, required, min 10 characters)

**Product Feedback**:
- Product (product_select, single selection)
- Overall Rating (rating_stars, 5 stars)
- Conditional: IF rating < 3 THEN require "What can we improve?" (textarea)
- Recommendation (rating_nps)

**Job Application**:
- Step 1: Personal (name, email, phone)
- Step 2: Resume (file upload, allow ["pdf", "doc"], max 2MB)
- Step 3: Availability (date for start, checkbox_group for work days)
- Conditional: IF "years_experience" > 5 THEN show_field "leadership_experience"

## Tips

- **Use appropriate field types** - Email field for emails (not text), provides validation and better mobile keyboards
- **Keep labels short** - Use help text for details, not labels
- **Group related fields** - Use headings and dividers for visual organization
- **Test validation** - Preview form and try submitting with invalid data
- **Limit file upload sizes** - 5MB max prevents server overload from large files
- **Use conditional logic sparingly** - Too many rules confuse users; keep forms simple
- **Set realistic max values** - Age max of 120, quantity max of 100 (prevents typos like 1000)
- **Provide pattern examples** - If using regex validation, show example in help text
- **Make obvious fields required** - Name and email for contact forms, always required
- **Use radio for 2-4 options** - Dropdown for 5+ options (improves UX)
- **Half-width fields for short inputs** - Phone and ZIP can be half-width, saves vertical space
- **Product selectors for wishlists** - Let customers select multiple products for recommendations
