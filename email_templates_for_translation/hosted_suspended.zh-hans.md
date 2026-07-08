---
template_type: hosted_suspended
category: License
---

# Email Template: hosted_suspended

## Subject
店铺暂停 - {{ store_name }}

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
          账户暂停
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
          你好 {{ name|default:'there' }},
        </mj-text>
        <mj-text>
          由于未支付账单，您的店铺 <strong>{{ store_name }}</strong> 已被暂停。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What This Means -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          这意味着什么
        </mj-text>
        <mj-text font-size="14px">
          您的店铺现在处于只读模式 —— 顾客可以浏览，但无法下单。您的数据是安全的，并将在30天内保留。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Reactivate -->
    <mj-section>
      <mj-column>
        <mj-text>
          要恢复完整访问权限，请更新您的支付方式并结清未付款项。
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
账户暂停 - {{ store_name }}

你好 {{ name|default:'there' }},

由于未支付账单，您的店铺 {{ store_name }} 已被暂停。

这意味着什么：
您的店铺现在处于只读模式 —— 顾客可以浏览，但无法下单。您的数据是安全的，并将在30天内保留。

要恢复完整访问权限，请更新您的支付方式并结清未付款项。

重新激活店铺：https://spwig.com/account

需要帮助？请联系 {{ support_email }} }}