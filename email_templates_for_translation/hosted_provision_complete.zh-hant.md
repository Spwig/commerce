---
template_type: hosted_provision_complete
category: License
---

# Email Template: hosted_provision_complete

## Subject
您的商店已準備好 - {{ store_name }}

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
    <mj-section background-color="{{ theme.color.primary|default:'#2563eb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          您的商店已上線！
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }} 已準備好為您服務
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
          好消息！您的 Spwig 商店 <strong>{{ store_name }}</strong> 已完成配置，現在已上線。您可以立即開始設定產品、品牌和付款方式。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Store Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          您的商店詳情
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          商店網址：{{ store_url }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          管理面板：{{ admin_url }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          地區：{{ region }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Getting Started -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          快速開始
        </mj-text>
        <mj-text font-size="14px">
          1. 使用結帳時設定的電子郵件和密碼，登入管理面板
        </mj-text>
        <mj-text font-size="14px">
          2. 在「設計 > 主題設定」中新增商店標誌和品牌
        </mj-text>
        <mj-text font-size="14px">
          3. 在「目錄 > 產品」中新增第一個產品
        </mj-text>
        <mj-text font-size="14px">
          4. 在「設定 > 支付服務」中設定支付服務商
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="前往管理面板" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
您的商店已上線！

{{ store_name }} 已準備好為您服務。

Hi {{ name|default:'there' }},

好消息！您的 Spwig 商店 {{ store_name }} 已完成配置，現在已上線。您可以立即開始設定產品、品牌和付款方式。

您的商店詳情：
- 商店網址：{{ store_url }}
- 管理面板：{{ admin_url }}
- 地區：{{ region }}

快速開始：
1. 使用結帳時設定的電子郵件和密碼，登入管理面板
2. 在「設計 > 主題設定」中新增商店標誌和品牌
3. 在「目錄 > 產品」中新增第一個產品
4. 在「設定 > 支付服務」中設定支付服務商

前往管理面板：{{ admin_url }}

需要幫助嗎？請聯繫 {{ support_email }}