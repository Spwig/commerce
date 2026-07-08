---
template_type: hosted_suspended
category: License
---

# Email Template: hosted_suspended

## Subject
Store Suspended - {{ store_name }}

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
    <mj-section background-color="#dc2626" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Account Suspended
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }}
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
          Your store <strong>{{ store_name }}</strong> has been suspended due to unpaid billing.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What This Means -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          What This Means
        </mj-text>
        <mj-text font-size="14px">
          Your store is now in read-only mode -- customers can browse but orders are disabled. Your data is safe and will be preserved for 30 days.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Reactivate -->
    <mj-section>
      <mj-column>
        <mj-text>
          To restore full access, please update your payment method and settle the outstanding balance.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="Reactivate Your Store" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Account Suspended - {{ store_name }}

Hi {{ name|default:'there' }},

Your store {{ store_name }} has been suspended due to unpaid billing.

What This Means:
Your store is now in read-only mode -- customers can browse but orders are disabled. Your data is safe and will be preserved for 30 days.

To restore full access, please update your payment method and settle the outstanding balance.

Reactivate Your Store: https://spwig.com/account

Need help? Contact {{ support_email }}
