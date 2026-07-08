---
template_type: license_purchase_confirmation
category: License
---

# Email Template: license_purchase_confirmation

## Subject
您的 Spwig 授權 - 訂單 #{{ order_number }}

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
          感謝您的購買！
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          訂單 #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          您好 {{ customer_name }}，
        </mj-text>
        <mj-text>
          您對 <strong>{{ product_name }}</strong> 的購買已完成。以下為您的授權碼和設定令牌，用以開始使用。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Order Summary -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          訂單摘要
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          產品：{{ product_name }}{% if includes_pos %} (包含 POS){% endif %}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          金額：{{ price }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          訂單編號：{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- License Key Box -->
    <mj-section background-color="#eff6ff" padding="25px" border-radius="8px">
      <mj-column>
        <mj-text font-size="12px" color="#1e40af" font-weight="bold" align="center">
          您的授權碼
        </mj-text>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" align="center" font-family="'Courier New', monospace" padding="10px 0">
          {{ license_key }}
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          請保存此授權碼 - 重新安裝時會用到
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Setup Token Box -->
    <mj-section background-color="#f0fdf4" padding="25px" border-radius="8px">
      <mj-column>
        <mj-text font-size="12px" color="#065f46" font-weight="bold" align="center">
          您的設定令牌
        </mj-text>
        <mj-text font-size="14px" font-weight="bold" color="#059669" align="center" font-family="'Courier New', monospace" padding="10px 0" word-break="break-all">
          {{ setup_token }}
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          安裝時請使用此令牌以啟動您的商店
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Getting Started -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          開始使用
        </mj-text>
        <mj-text font-size="14px">
          1. 跟隨我們的設定指南，在您的伺服器上安裝 Spwig
        </mj-text>
        <mj-text font-size="14px">
          2. 安裝過程中提示時輸入您的設定令牌
        </mj-text>
        <mj-text font-size="14px">
          3. 您的商店將自動啟動
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Setup Guide CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=setup_url text="查看設定指南" %}

    {% if activation_url %}
    <!-- Guest Account Activation -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px 20px 10px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          建立您的帳號
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="5px">
          設定密碼以管理您的授權碼、存取下載內容並接收更新。
        </mj-text>
      </mj-column>
    </mj-section>
    {% include 'email_system/mjml_components/cta_button.mjml' with url=activation_url text="建立您的帳號" %}
    {% endif %}

    <!-- Important Notice -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.warning|default:'#d97706' }}" font-weight="bold">
          重要：
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          請妥善保管這封郵件 - 其中包含您的授權碼和設定令牌，供未來參考。請勿與他人分享這些憑證。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
感謝您的購買！

訂單 #{{ order_number }}

您好 {{ customer_name }}，

您對 {{ product_name }} 的購買已完成。以下為您的授權碼和設定令牌，用以開始使用。

訂單摘要：
- 產品：{{ product_name }}{% if includes_pos %} (包含 POS){% endif %}
- 金額：{{ price }}
- 訂單編號：{{ order_number }}

您的授權碼：
{{ license_key }}
請保存此授權碼 - 重新安裝時會用到。

您的設定令牌：
{{ setup_token }}
安裝時請使用此令牌以啟動您的商店。

開始使用：
1. 跟隨我們的設定指南，在您的伺服器上安裝 Spwig
2. 安裝過程中提示時輸入您的設定令牌
3. 您的商店將自動啟動

查看設定指南：{{ setup_url }}
{% if activation_url %}
建立您的帳號：
設定密碼以管理您的授權碼、存取下載內容並接收更新。
{{ activation_url }}
{% endif %}
重要：
請妥善保管這封郵件 - 其中包含您的授權碼和設定令牌，供未來參考。請勿與他人分享這些憑證。

需要幫助？請聯繫 {{ support_email }}