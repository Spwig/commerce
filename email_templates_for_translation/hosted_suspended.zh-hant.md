---
template_type: hosted_suspended
category: License
---

# Email Template: hosted_suspended

## Subject
商店已停用 - {{ store_name }}

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
          帳號已停用
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
          您的商店 <strong>{{ store_name }}</strong> 因未支付費用已被停用。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What This Means -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          這代表什麼意思
        </mj-text>
        <mj-text font-size="14px">
          您的商店現在處於只讀模式 — 顧客可以瀏覽，但無法下單。您的資料是安全的，將會保留 30 天。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Reactivate -->
    <mj-section>
      <mj-column>
        <mj-text>
          要恢復完整存取權，請更新您的付款方式並結清未償還的餘額。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="重新啟用您的商店" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
帳號已停用 - {{ store_name }}

Hi {{ name|default:'there' }},

您的商店 {{ store_name }} 因未支付費用已被停用。

這代表什麼意思：
您的商店現在處於只讀模式 — 顧客可以瀏覽，但無法下單。您的資料是安全的，將會保留 30 天。

要恢復完整存取權，請更新您的付款方式並結清未償還的餘額。

重新啟用您的商店：https://spwig.com/account

需要幫助嗎？請聯繫 {{ support_email }}