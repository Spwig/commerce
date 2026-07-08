---
template_type: license_maintenance_renewal
category: License
---

# Email Template: license_maintenance_renewal

## Subject
維護服務續約 - 訂單 #{{ order_number }}

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
    <mj-section background-color="{{ theme.color.success|default:'#10b981' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          維護服務續約！
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
          您的 Spwig 維護服務已成功續約。您將繼續收到平台更新、安全補丁和新功能。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Renewal Summary -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          續約摘要
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          授權碼：{{ license_key }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          維護服務有效至：{{ renewal_expires_at }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          訂單號碼：{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What's Included -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          所含內容
        </mj-text>
        <mj-text font-size="14px">
          您的維護服務可讓您使用以下內容：
        </mj-text>
        <mj-text font-size="14px" padding-top="5px">
          - 平台功能更新與改進
        </mj-text>
        <mj-text font-size="14px">
          - 安全補丁與錯誤修復
        </mj-text>
        <mj-text font-size="14px">
          - 透過升級伺服器發布的新組件
        </mj-text>
        <mj-text font-size="14px">
          - 技術支援
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Next Steps -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          您無需採取任何行動。更新將繼續透過您管理面板的組件更新系統提供。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
維護服務續約！

訂單 #{{ order_number }}

您好 {{ customer_name }}，

您的 Spwig 維護服務已成功續約。您將繼續收到平台更新、安全補丁和新功能。

續約摘要：
- 授權碼：{{ license_key }}
- 維護服務有效至：{{ renewal_expires_at }}
- 訂單號碼：{{ order_number }}

所含內容：
- 平台功能更新與改進
- 安全補丁與錯誤修復
- 透過升級伺服器發布的新組件
- 技術支援

您無需採取任何行動。更新將繼續透過您管理面板的組件更新系統提供。

需要幫助嗎？請聯繫 {{ support_email }}