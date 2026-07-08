---
template_type: hosted_payment_method_updated
category: License
---

# Email Template: hosted_payment_method_updated

## Subject
支付方式已更新 - {{ store_name }}

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
          支付方式已更新
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
          你好，
        </mj-text>
        <mj-text>
          您在 <strong>{{ store_name }}</strong> 上的 <strong>{{ plan_name }}</strong> 计划的支付方式已成功更新。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Security Notice -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          没有进行此更改？
        </mj-text>
        <mj-text font-size="14px">
          如果您没有更新支付方式，请立即联系我们的支持团队，以便我们保护您的账户。
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
支付方式已更新 - {{ store_name }}

你好，

您在 {{ store_name }} 上的 {{ plan_name }} 计划的支付方式已成功更新。

没有进行此更改？
如果未更新支付方式，请立即联系我们的支持团队，以便我们保护您的账户。

前往您的商店：{{ admin_url }}

需要帮助？请联系 {{ support_email }}