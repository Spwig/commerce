---
template_type: account_invitation
category: Core E-commerce
---

# Email Template: account_invitation

## Subject
Create Your Account at {{ site_name }}

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
          You're Invited!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Create your account at {{ site_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Hi {{ customer_name }},
        </mj-text>
        <mj-text>
          We noticed you've been shopping with us as a guest. Create a full account to unlock benefits like order tracking, faster checkout, and exclusive offers.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Order History Summary -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Your Shopping History
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Total Orders: {{ total_orders }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Total Spent: {{ total_spent }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Benefits -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Why Create an Account?
        </mj-text>
        <mj-text font-size="14px">
          - Track your orders and view order history
        </mj-text>
        <mj-text font-size="14px">
          - Faster checkout with saved details
        </mj-text>
        <mj-text font-size="14px">
          - Manage your addresses and preferences
        </mj-text>
        <mj-text font-size="14px">
          - Access exclusive offers and promotions
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Button -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=activation_url text="Create Your Account" %}

    <!-- Note -->
    <mj-section>
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          This link will allow you to set a password for your account. Your existing order history will be preserved.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
You're Invited to Create Your Account!

Hi {{ customer_name }},

We noticed you've been shopping with us as a guest. Create a full account to unlock benefits like order tracking, faster checkout, and exclusive offers.

Your Shopping History:
- Total Orders: {{ total_orders }}
- Total Spent: {{ total_spent }}

Why Create an Account?
- Track your orders and view order history
- Faster checkout with saved details
- Manage your addresses and preferences
- Access exclusive offers and promotions

Create Your Account: {{ activation_url }}

This link will allow you to set a password for your account. Your existing order history will be preserved.

Need help? Contact {{ support_email }}
