---
template_type: hosted_termination_warning
category: License
---

# Email Template: hosted_termination_warning

## Subject
重要：7天後將刪除資料 - {{ store_name }}

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
          資料刪除警告
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
          您的商店 <strong>{{ store_name }}</strong> 及所有相關資料將於 <strong>{{ termination_date }}</strong> 永久刪除。此操作無法撤銷。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What You Can Do -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          您可以採取的行動
        </mj-text>
        <mj-text font-size="14px">
          如果您希望保留資料，請在這日期前導出資料，或重新啟用訂閱以防止刪除。
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
資料刪除警告 - {{ store_name }}

Hi {{ name|default:'there' }},

您的商店 {{ store_name }} 及所有相關資料將於 {{ termination_date }} 永久刪除。此操作無法撤銷。

您可以採取的行動：
如果希望保留資料，請在這日期前導出資料，或重新啟用訂閱以防止刪除。

重新啟用訂閱：https://spwig.com/account

需要幫助嗎？請聯繫 {{ support_email }}