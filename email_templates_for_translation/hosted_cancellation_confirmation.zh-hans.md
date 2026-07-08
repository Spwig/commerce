---
template_type: hosted_cancellation_confirmation
category: License
---

# Email Template: hosted_cancellation_confirmation

## Subject
取消确认 - {{ store_name }}

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
          取消确认
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
          你好 {{ name|default:'there' }},
        </mj-text>
        <mj-text>
          你的 <strong>{{ plan_name }}</strong> 订阅已取消。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          接下来会发生什么
        </mj-text>
        <mj-text font-size="14px">
          在 <strong>{{ access_until_date }}</strong> 之前，你将继续拥有完整访问权限。
        </mj-text>
        <mj-text font-size="14px">
          之后，你的商店数据将在 30 天内保留，直到 <strong>{{ termination_date }}</strong>。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Additional Info -->
    <mj-section>
      <mj-column>
        <mj-text>
          如果你希望在访问权限结束前导出数据，可以从你的管理面板进行操作。改变主意了？你随时可以重新激活你的订阅。
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
取消确认 - {{ store_name }}

你好 {{ name|default:'there' }},

你的 {{ plan_name }} 订阅已取消。

接下来会发生什么：
- 在 {{ access_until_date }} 之前，你将继续拥有完整访问权限。
- 之后，你的商店数据将在 30 天内保留，直到 {{ termination_date }}。

如果你想在访问权限结束前导出数据，可以从你的管理面板进行操作。改变主意了？你随时可以重新激活你的订阅。

重新激活订阅：https://spwig.com/account

需要帮助？请联系 {{ support_email }}