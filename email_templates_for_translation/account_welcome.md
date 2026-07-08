---
template_type: account_welcome
category: Enhanced E-commerce
---

# Email Template: account_welcome

## Subject
Welcome to {{ shop_name }}!

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="32px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          Welcome! 👋
        </mj-text>
        <mj-text font-size="18px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          We're excited to have you as part of our community
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Personalized Greeting -->
    <mj-section background-color="{{ theme.color.info_light|default:'#dbeafe' }}" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          Hi {{ customer_name }},
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          Your account has been successfully created. You're all set to start shopping!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Benefits Section -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="20px" font-weight="600" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="20px">
          Member Benefits
        </mj-text>

        {% for benefit in shop_benefits %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="8px 0">
          <span style="color: {{ theme.color.success|default:'#10b981' }}; font-size: 18px;">✓</span> {{ benefit }}
        </mj-text>
        {% endfor %}
      </mj-column>
    </mj-section>

    <!-- CTA Buttons -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="10px 20px">
      <mj-column>
        <mj-button
          href="{{ browse_products_url }}"
          background-color="{{ theme.color.primary|default:'#2563eb' }}"
          color="{{ theme.color.background|default:'#ffffff' }}"
          font-size="16px"
          font-weight="600"
          border-radius="6px"
          padding="14px 32px"
        >
          Start Shopping
        </mj-button>
      </mj-column>
    </mj-section>

    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="10px 20px 30px 20px">
      <mj-column>
        <mj-button
          href="{{ account_url }}"
          background-color="{{ theme.color.text_muted|default:'#6b7280' }}"
          color="{{ theme.color.background|default:'#ffffff' }}"
          font-size="14px"
          border-radius="6px"
          padding="12px 24px"
        >
          Manage My Account
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Support Block -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Welcome! 👋

Hi {{ customer_name }},

Your account has been successfully created. You're all set to start shopping!

Member Benefits:
{% for benefit in shop_benefits %}
✓ {{ benefit }}
{% endfor %}

Start shopping: {{ browse_products_url }}
Manage your account: {{ account_url }}

Need Help?
Email: {{ support_email }}
Phone: {{ support_phone }}

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| customer_name | Customer's first name | Sarah |
| shop_name | Store name | Amazing Shop |
| shop_benefits | List of member benefits | ['Exclusive discounts', 'Early access to sales', 'Free shipping on orders over $50'] |
| browse_products_url | Product catalog URL | https://shop.com/en/products |
| account_url | Customer account page | https://shop.com/en/account |
| support_email | Support email address | support@shop.com |
| support_phone | Support phone number | 1-800-555-0123 |

## Notes

- Transactional email - sent after account creation
- Welcome new customers and set expectations
- Highlights member benefits
- Encourages first purchase
- Sets positive first impression
- Should be sent immediately after successful registration
