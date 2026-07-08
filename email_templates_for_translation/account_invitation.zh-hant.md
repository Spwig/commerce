---
template_type: account_invitation
category: Core E-commerce
---

# Email Template: account_invitation

## Subject
在 {{ site_name }} 創建您的帳號

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
          您受邀加入！
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          在 {{ site_name }} 創建您的帳號
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
          我們注意到您之前是以訪客身份在本網站購物。創建完整帳號可享有追蹤訂單、快速結帳和專屬優惠等好處。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Order History Summary -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          您的購物記錄
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          總訂單數：{{ total_orders }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          總消費金額：{{ total_spent }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Benefits -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          為何要創建帳號？
        </mj-text>
        <mj-text font-size="14px">
          - 追蹤您的訂單並查看訂單記錄
        </mj-text>
        <mj-text font-size="14px">
          - 使用儲存的資料快速結帳
        </mj-text>
        <mj-text font-size="14px">
          - 管理您的地址和偏好設定
        </mj-text>
        <mj-text font-size="14px">
          - 取得專屬優惠和促銷活動
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Button -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=activation_url text="Create Your Account" %}

    <!-- Note -->
    <mj-section>
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          這個連結將讓您為帳號設定密碼。您現有的訂單記錄將會保留。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
您受邀創建您的帳號！

您好 {{ customer_name }}，

我們注意到您之前是以訪客身份在本網站購物。創建完整帳號可享有追蹤訂單、快速結帳和專屬優惠等好處。

您的購物記錄：
- 總訂單數：{{ total_orders }}
- 總消費金額：{{ total_spent }}

為何要創建帳號？
- 追蹤您的訂單並查看訂單記錄
- 使用儲存的資料快速結帳
- 管理您的地址和偏好設定
- 取得專屬優惠和促銷活動

創建您的帳號：{{ activation_url }}

這個連結將讓您為帳號設定密碼。您現有的訂單記錄將會保留。

需要幫助嗎？請聯繫 {{ support_email }}