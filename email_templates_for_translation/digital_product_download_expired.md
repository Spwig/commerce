---
template_type: digital_product_download_expired
category: Digital Products
---

# Email Template: digital_product_download_expired

## Subject
Download Link Expired - Order #{{ order_number }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.error|default:'#ef4444' }}" padding="20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          Download Link Expired
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Main Content -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Hi {{ customer_name }},
        </mj-text>
        <mj-text>
          Your download link for <strong>{{ product_name }}</strong> from order #{{ order_number }} has expired.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Expired Information -->
    <mj-section background-color="#fef2f2" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="14px" color="#991b1b">
          Download links expire {{ expiration_days }} days after purchase for security reasons.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Request New Link -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold">
          Need a new download link?
        </mj-text>
        <mj-text>
          You can request a new download link by logging into your account or contacting our support team.
        </mj-text>
        <mj-button href="{{ account_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" padding="15px 30px" border-radius="6px">
          Go to My Account
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Support -->
    <mj-section>
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          Questions? Contact {{ support_email }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Download Link Expired

Hi {{ customer_name }},

Your download link for {{ product_name }} from order #{{ order_number }} has expired.

Download links expire {{ expiration_days }} days after purchase for security reasons.

Need a new download link?
You can request a new download link by logging into your account or contacting our support team.

Go to My Account: {{ account_url }}

Questions? Contact {{ support_email }}
