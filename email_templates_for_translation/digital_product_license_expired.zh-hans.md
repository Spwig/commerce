---
template_type: digital_product_license_expired
category: Digital Products
---

# Email Template: digital_product_license_expired

## Subject
许可证即将到期 - {{ product_name }}

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
    <mj-section background-color="{{ theme.color.warning|default:'#f59e0b' }}" padding="20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          许可证即将到期
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Main Content -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          你好 {{ customer_name }}，
        </mj-text>
        <mj-text>
          你的 {{ product_name }} 许可证即将到期。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- License Details -->
    <mj-section background-color="#fffbeb" padding="20px" border="2px solid {{ theme.color.warning|default:'#f59e0b' }}" border-radius="8px">
      <mj-column>
        <mj-text font-size="14px" color="#92400e">
          <strong>许可证密钥：</strong> {{ license_key }}
        </mj-text>
        <mj-text font-size="14px" color="#92400e">
          <strong>到期时间：</strong> {{ expiration_date }}
        </mj-text>
        <mj-text font-size="14px" color="#92400e">
          <strong>剩余天数：</strong> {{ days_remaining }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Renewal -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold">
          续订你的许可证
        </mj-text>
        <mj-text>
          今天续订你的许可证，继续享受 {{ product_name }}。
        </mj-text>
        <mj-button href="{{ renewal_url }}" background-color="{{ theme.color.warning|default:'#f59e0b' }}" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" padding="15px 30px" border-radius="6px">
          立即续订
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Support -->
    <mj-section>
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          关于续订有疑问？请联系 {{ support_email }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
许可证即将到期

你好 {{ customer_name }}，

你的 {{ product_name }} 许可证即将到期。

许可证详情：
• 许可证密钥：{{ license_key }}
• 到期时间：{{ expiration_date }}
• 剩余天数：{{ days_remaining }}

续订你的许可证：
今天续订你的许可证，继续享受 {{ product_name }}。

立即续订：{{ renewal_url }}

关于续订有疑问？请联系 {{ support_email }}