---
template_type: hosted_suspension_warning
category: License
---

# Email Template: hosted_suspension_warning

## Subject
कार्रवाई की आवश्यकता है - {{ store_name }}

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
    <mj-section background-color="#ea580c" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Suspension Warning
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Action required for {{ store_name }}
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
          Your payment for <strong>{{ plan_name }}</strong> is overdue. If not resolved by <strong>{{ grace_end_date }}</strong>, your store will be placed in read-only mode.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What Suspension Means -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          What Suspension Means
        </mj-text>
        <mj-text font-size="14px">
          If your store is suspended, it will remain visible to visitors but you will not be able to make changes. New orders will be paused until the outstanding balance is settled.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Resolve -->
    <mj-section>
      <mj-column>
        <mj-text>
          Please update your payment method to avoid any disruption to your store.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="Update Payment Method" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Suspension Warning - {{ store_name }}

Hi {{ name|default:'there' }},

Your payment for {{ plan_name }} is overdue. If not resolved by {{ grace_end_date }}, your store will be placed in read-only mode.

What Suspension Means:
If your store is suspended, it will remain visible to visitors but you will not be able to make changes. New orders will be paused until the outstanding balance is settled.

Please update your payment method to avoid any disruption to your store.

Update Payment Method: https://spwig.com/account

Need help? Contact {{ support_email }}