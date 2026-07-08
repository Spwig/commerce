---
template_type: hosted_termination_warning
category: License
---

# Email Template: hosted_termination_warning

## Subject
重要：7天内将删除数据 - {{ store_name }}

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
          数据删除警告
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
          您的商店 <strong>{{ store_name }}</strong> 及所有相关数据将在 <strong>{{ termination_date }}</strong> 被永久删除。此操作无法撤销。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What You Can Do -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          您可以采取的措施
        </mj-text>
        <mj-text font-size="14px">
          如果您希望保留数据，请在此日期之前导出数据或重新激活订阅以防止删除。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="Reactivate Subscription" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
数据删除警告 - {{ store_name }}

Hi {{ name|default:'there' }},

您的商店 {{ store_name }} 及所有相关数据将在 {{ termination_date }} 被永久删除。此操作无法撤销。

您可以采取的措施：
如果希望保留数据，请在此日期之前导出数据或重新激活订阅以防止删除。

重新激活订阅：https://spwig.com/account

需要帮助？请联系 {{ support_email }}