---
template_type: subscription_plan_downgraded
category: Subscriptions
---

# Email Template: subscription_plan_downgraded

## Subject
您的订阅计划已更改为 {{ new_plan_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          计划变更
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          订阅计划已更新
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          你好 {{ customer_name }}，
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          您的订阅计划已更改为 {{ new_plan_name }}。
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              计划变更详情：
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>原计划：</strong> {{ old_plan_name }}<br/>
              <strong>新计划：</strong> {{ new_plan_name }}<br/>
              <strong>变更时间：</strong> {{ downgrade_date }}<br/>
              <strong>生效时间：</strong> {{ effective_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          变更内容：
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ plan_changes }}
        </mj-text>

        {% if features_lost %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              不再可用的功能：
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ features_lost }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          账单信息：
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>新价格：</strong> {{ new_price }} / {{ billing_period }}<br/>
              <strong>生效日期：</strong> {{ effective_date }}<br/>
              <strong>下次账单日期：</strong> {{ next_billing_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if credit_applied %}
        <mj-spacer height="20px" />
        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              💰 您的账户已应用了 {{ credit_amount }} 的信用额度，用于您之前计划的未使用部分。
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          改变主意了？
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color_secondary|default:'#6b7280' }}" align="center">
          您可以随时升级回 {{ old_plan_name }}。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-button href="{{ upgrade_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          升级计划
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ account_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          查看我的订阅
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
计划变更

订阅计划已更新

你好 {{ customer_name }}，

您的订阅计划已更改为 {{ new_plan_name }}。

计划变更详情：
- 原计划： {{ old_plan_name }}
- 新计划： {{ new_plan_name }}
- 变更时间： {{ downgrade_date }}
- 生效时间： {{ effective_date }}

变更内容：
{{ plan_changes }}

{% if features_lost %}
不再可用的功能：
{{ features_lost }}
{% endif %}

账单信息：
- 新价格： {{ new_price }} / {{ billing_period }}
- 生效日期： {{ effective_date }}
- 下次账单日期： {{ next_billing_date }}

{% if credit_applied %}
💰 您的账户已应用了 {{ credit_amount }} 的信用额度，用于您之前计划的未使用部分。
{% endif %}

改变主意了？
您可以随时升级回 {{ old_plan_name }}。

升级计划： {{ upgrade_url }}
查看我的订阅： {{ account_url }}