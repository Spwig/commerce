---
template_type: blog_subscription_confirmed
category: Blog
---

# Email Template: blog_subscription_confirmed

## Subject
Please confirm your subscription to {{ blog_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Confirm Your Subscription
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ subscriber_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Thank you for subscribing to {{ blog_name }}! To complete your subscription and start receiving updates, please confirm your email address.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ confirmation_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          Confirm Subscription
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              Can't click the button? Copy and paste this link into your browser:<br/>
              <span style="color: {{ theme.color.primary|default:'#2563eb' }}; font-family: 'Courier New', monospace;">{{ confirmation_url }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>Why confirm?</strong><br/>
          Email confirmation helps us ensure you want to receive updates and prevents spam. Your privacy and inbox are important to us.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Didn't subscribe? You can safely ignore this email.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
CONFIRM YOUR SUBSCRIPTION

Hi {{ subscriber_name }},

Thank you for subscribing to {{ blog_name }}! To complete your subscription and start receiving updates, please confirm your email address.

Confirm subscription: {{ confirmation_url }}

WHY CONFIRM?
Email confirmation helps us ensure you want to receive updates and prevents spam. Your privacy and inbox are important to us.

Didn't subscribe? You can safely ignore this email.

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| subscriber_name | Subscriber's name or email | Sarah |
| blog_name | Blog name | Health & Wellness Blog |
| confirmation_url | Confirmation link with token | https://shop.com/en/blog/confirm/abc123xyz |

## Notes

- Double opt-in confirmation (anti-spam)
- Transactional email - always sent
- Link expires after 24-48 hours
- Simple, focused message
- Sent immediately after subscription request
