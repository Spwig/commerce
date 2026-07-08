---
template_type: hosted_subscription_confirmation
category: License
---

# Email Template: hosted_subscription_confirmation

## Subject
订阅确认 - {{ store_name }}

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
    <mj-section background-color="#16a34a" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          订阅确认！
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          欢迎来到 Spwig
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
          感谢您的订阅！您的 <strong>{{ plan_name }}</strong> 计划用于 <strong>{{ store_name }}</strong> 已确认。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Plan Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          计划详情
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          计划: {{ plan_name }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          计费周期: {{ billing_interval }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          金额: {{ currency }}{{ amount }}{% if intro_period %} (试用期价格){% endif %}
        </mj-text>
        {% if intro_period %}
        <mj-text font-size="13px" color="{{ theme.color.text_muted|default:'#6b7280' }}" padding-top="5px" font-style="italic">
          您的试用期价格适用于 {{ intro_period }}。之后，您的计划将按 {{ currency }}{{ full_amount }}/{{ billing_interval }} 续订。
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Next Steps -->
    <mj-section>
      <mj-column>
        <mj-text>
          您的商店正在设置中，设置完成后您将收到另一封电子邮件。
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" padding-top="10px">
          下次计费日期: {{ next_billing_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
订阅确认！

你好 {{ name|default:'there' }},

感谢您的订阅！您的 {{ plan_name }} 计划用于 {{ store_name }} 已确认。

计划详情：
- 计划: {{ plan_name }}
- 计费周期: {{ billing_interval }}
- 金额: {{ currency }}{{ amount }}{% if intro_period %} (试用期价格){% endif %}
{% if intro_period %}
这是您的试用期价格，适用于 {{ intro_period }}。之后，您的计划将按 {{ currency }}{{ full_amount }}/{{ billing_interval }} 续订。
{% endif %}
您的商店正在设置中，设置完成后您将收到另一封电子邮件。

下次计费日期: {{ next_billing_date }}

需要帮助？请联系 {{ support_email }}