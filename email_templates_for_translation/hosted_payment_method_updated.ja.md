---
template_type: hosted_payment_method_updated
category: License
---

# Email Template: hosted_payment_method_updated

## Subject
支払い方法が更新されました - {{ store_name }}

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
          支払い方法が更新されました
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
          こんにちは、
        </mj-text>
        <mj-text>
          {{ store_name }} の <strong>{{ plan_name }}</strong> プランの支払い方法が正常に更新されました。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Security Notice -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          この変更はご自身が行いませんでしたか？
        </mj-text>
        <mj-text font-size="14px">
          支払い方法の更新を行っていなかった場合は、アカウントをセキュアにするために、すぐにサポートチームにお問い合わせください。
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
支払い方法が更新されました - {{ store_name }}

こんにちは、

{{ store_name }} の {{ plan_name }} プランの支払い方法が正常に更新されました。

この変更はご自身が行いませんでしたか？
支払い方法の更新を行っていなかった場合は、アカウントをセキュアにするために、すぐにサポートチームにお問い合わせください。

Go to Your Store: {{ admin_url }}

Need help? Contact {{ support_email }}