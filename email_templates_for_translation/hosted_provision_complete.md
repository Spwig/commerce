---
template_type: hosted_provision_complete
category: License
---

# Email Template: hosted_provision_complete

## Subject
Your Store is Ready - {{ store_name }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.primary|default:'#2563eb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Your Store is Live!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }} is ready for you
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Hi {{ name|default:'there' }},
        </mj-text>
        <mj-text>
          Great news! Your Spwig store <strong>{{ store_name }}</strong> has been provisioned and is now live. You can start setting up your products, branding, and payment methods right away.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Store Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Your Store Details
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Store URL: {{ store_url }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Admin Panel: {{ admin_url }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Region: {{ region }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Getting Started -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Quick Start
        </mj-text>
        <mj-text font-size="14px">
          1. Log in to your admin panel using the email and password you set during checkout
        </mj-text>
        <mj-text font-size="14px">
          2. Add your store logo and branding under Design > Theme Settings
        </mj-text>
        <mj-text font-size="14px">
          3. Add your first products under Catalog > Products
        </mj-text>
        <mj-text font-size="14px">
          4. Set up a payment provider under Settings > Payment Providers
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Go to Admin Panel" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Your Store is Live!

{{ store_name }} is ready for you.

Hi {{ name|default:'there' }},

Great news! Your Spwig store {{ store_name }} has been provisioned and is now live. You can start setting up your products, branding, and payment methods right away.

Your Store Details:
- Store URL: {{ store_url }}
- Admin Panel: {{ admin_url }}
- Region: {{ region }}

Quick Start:
1. Log in to your admin panel using the email and password you set during checkout
2. Add your store logo and branding under Design > Theme Settings
3. Add your first products under Catalog > Products
4. Set up a payment provider under Settings > Payment Providers

Go to Admin Panel: {{ admin_url }}

Need help? Contact {{ support_email }}
