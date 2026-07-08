---
template_type: hosted_provision_failed
category: License
---

# Email Template: hosted_provision_failed

## Subject
조치 필요 - {{ store_name }}의 매장 설정 문제

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
    <mj-section background-color="{{ theme.color.error|default:'#dc2626' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Store Setup Issue
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
          We encountered an issue while setting up your store <strong>{{ store_name }}</strong>. Our team has been notified and is looking into it.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Error Details -->
    <mj-section background-color="#fef2f2" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="14px" font-weight="bold" color="#991b1b" padding-bottom="10px">
          What happened
        </mj-text>
        <mj-text font-size="14px" color="#7f1d1d">
          {{ provision_error }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What's Next -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          What happens next?
        </mj-text>
        <mj-text font-size="14px">
          Our support team has been automatically notified about this issue. You don't need to take any action - we will reach out to you once the issue is resolved.
        </mj-text>
        <mj-text font-size="14px" padding-top="10px">
          If you have any questions in the meantime, please don't hesitate to reach out to us.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Store Setup Issue - {{ store_name }}

Hi {{ name|default:'there' }},

We encountered an issue while setting up your store {{ store_name }}. Our team has been notified and is looking into it.

What happened:
{{ provision_error }}

What happens next?
Our support team has been automatically notified about this issue. You don't need to take any action - we will reach out to you once the issue is resolved.

If you have any questions in the meantime, please don't hesitate to reach out to us.

Need help? Contact {{ support_email }}