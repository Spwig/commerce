---
template_type: hosted_cancellation_confirmation
category: License
---

# Email Template: hosted_cancellation_confirmation

## Subject
Cancellation Confirmed - {{ store_name }}

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
    <mj-section background-color="#6b7280" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Cancellation Confirmed
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
          Your <strong>{{ plan_name }}</strong> subscription has been cancelled.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          What Happens Next
        </mj-text>
        <mj-text font-size="14px">
          You'll continue to have full access until <strong>{{ access_until_date }}</strong>.
        </mj-text>
        <mj-text font-size="14px">
          After that, your store data will be preserved for 30 days until <strong>{{ termination_date }}</strong>.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Additional Info -->
    <mj-section>
      <mj-column>
        <mj-text>
          If you'd like to export your data before access ends, you can do so from your admin panel. Changed your mind? You can reactivate your subscription at any time.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="Reactivate Subscription" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Cancellation Confirmed - {{ store_name }}

Hi {{ name|default:'there' }},

Your {{ plan_name }} subscription has been cancelled.

What Happens Next:
- You'll continue to have full access until {{ access_until_date }}.
- After that, your store data will be preserved for 30 days until {{ termination_date }}.

If you'd like to export your data before access ends, you can do so from your admin panel. Changed your mind? You can reactivate your subscription at any time.

Reactivate Subscription: https://spwig.com/account

Need help? Contact {{ support_email }}
