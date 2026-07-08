---
template_type: hosted_payment_recovered
category: License
---

# Email Template: hosted_payment_recovered

## Subject
支払いが成功しました - {{ store_name }}

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
    <mj-section background-color="#16a34a" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          支払いが成功しました
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
          こんにちは {{ name|default:'there' }}、
        </mj-text>
        <mj-text>
          良いニュースです！{{ plan_name }} に対する {{ currency }}{{ amount }} の支払いが正常に処理されました。あなたのサブスクリプションは中断することなく続きます。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Go to Your Store" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
支払いが成功しました - {{ store_name }}

こんにちは {{ name|default:'there' }},

良いニュースです！{{ plan_name }} に対する {{ currency }}{{ amount }} の支払いが正常に処理されました。あなたのサブスクリプションは中断することなく続きます。

Go to Your Store: {{ admin_url }}

Need help? Contact {{ support_email }}