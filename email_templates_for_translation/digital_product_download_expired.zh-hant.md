---
template_type: digital_product_download_expired
category: Digital Products
---

# Email Template: digital_product_download_expired

## Subject
下載連結已過期 - 訂單 #{{ order_number }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.error|default:'#ef4444' }}" padding="20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          下載連結已過期
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Main Content -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Hi {{ customer_name }},
        </mj-text>
        <mj-text>
          您的訂單 #{{ order_number }} 中 {{ product_name }} 的下載連結已過期。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Expired Information -->
    <mj-section background-color="#fef2f2" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="14px" color="#991b1b">
          下載連結在購買後 {{ expiration_days }} 天過期，這是為了安全起見。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Request New Link -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold">
          需要新的下載連結嗎？
        </mj-text>
        <mj-text>
          您可以透過登入帳戶或聯繫我們的支援團隊來索取新的下載連結。
        </mj-text>
        <mj-button href="{{ account_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" padding="15px 30px" border-radius="6px">
          前往我的帳戶
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Support -->
    <mj-section>
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          有問題嗎？請聯繫 {{ support_email }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
下載連結已過期

Hi {{ customer_name }},

您的訂單 #{{ order_number }} 中 {{ product_name }} 的下載連結已過期。

下載連結在購買後 {{ expiration_days }} 天過期，這是為了安全起見。

需要新的下載連結嗎？
您可以透過登入帳戶或聯繫我們的支援團隊來索取新的下載連結。

前往我的帳戶: {{ account_url }}

有問題嗎？請聯繫 {{ support_email }}