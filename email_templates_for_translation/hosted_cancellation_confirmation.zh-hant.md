---
template_type: hosted_cancellation_confirmation
category: License
---

# Email Template: hosted_cancellation_confirmation

## Subject
取消確認 - {{ store_name }}

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
    <mj-section background-color="#6b7280" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          取消確認
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
          您的 <strong>{{ plan_name }}</strong> 訂閱已取消。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          接下來會發生什麼
        </mj-text>
        <mj-text font-size="14px">
          您將繼續擁有完整存取權直到 <strong>{{ access_until_date }}</strong>。
        </mj-text>
        <mj-text font-size="14px">
          之後，您的商店資料將保留 30 天，直到 <strong>{{ termination_date }}</strong>。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Additional Info -->
    <mj-section>
      <mj-column>
        <mj-text>
          如果您想在存取權結束前匯出資料，可以從您的管理面板進行操作。改變主意了嗎？您可以隨時重新啟用訂閱。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="重新啟用訂閱" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
取消確認 - {{ store_name }}

Hi {{ name|default:'there' }},

您的 {{ plan_name }} 訂閱已取消。

接下來會發生什麼：
- 您將繼續擁有完整存取權直到 {{ access_until_date }}。
- 之後，您的商店資料將保留 30 天直到 {{ termination_date }}。

如果您想在存取權結束前匯出資料，可以從您的管理面板進行操作。改變主意了嗎？您可以隨時重新啟用訂閱。

重新啟用訂閱：https://spwig.com/account

需要幫助嗎？請聯繫 {{ support_email }}