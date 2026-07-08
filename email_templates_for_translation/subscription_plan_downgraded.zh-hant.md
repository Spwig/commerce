---
template_type: subscription_plan_downgraded
category: Subscriptions
---

# Email Template: subscription_plan_downgraded

## Subject
您的訂閱方案已更改為 {{ new_plan_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          訂閱方案變更
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          訂閱方案已更新
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          您的訂閱方案已更改為 {{ new_plan_name }}。
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              訂閱方案變更細節：
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Previous Plan:</strong> {{ old_plan_name }}<br/>
              <strong>New Plan:</strong> {{ new_plan_name }}<br/>
              <strong>Changed On:</strong> {{ downgrade_date }}<br/>
              <strong>Effective:</strong> {{ effective_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          什麼變更：
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
          計費資訊：
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>New Price:</strong> {{ new_price }} / {{ billing_period }}<br/>
              <strong>Effective Date:</strong> {{ effective_date }}<br/>
              <strong>Next Billing Date:</strong> {{ next_billing_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if credit_applied %}
        <mj-spacer height="20px" />
        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              💰 您的帳戶已應用 {{ credit_amount }} 的信用額度，用於您之前方案未使用的部分。
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          改變主意了嗎？
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color_secondary|default:'#6b7280' }}" align="center">
          您可以隨時升級回 {{ old_plan_name }}。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-button href="{{ upgrade_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          升級方案
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ account_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          查看我的訂閱
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
訂閱方案變更

訂閱方案已更新

Hi {{ customer_name }},

您的訂閱方案已更改為 {{ new_plan_name }}。

訂閱方案變更細節：
- 原方案：{{ old_plan_name }}
- 新方案：{{ new_plan_name }}
- 更改日期：{{ downgrade_date }}
- 生效日期：{{ effective_date }}

什麼變更：
{{ plan_changes }}

{% if features_lost %}
不再可用的功能：
{{ features_lost }}
{% endif %}

計費資訊：
- 新價格：{{ new_price }} / {{ billing_period }}
- 生效日期：{{ effective_date }}
- 下次計費日期：{{ next_billing_date }}

{% if credit_applied %}
💰 您的帳戶已應用 {{ credit_amount }} 的信用額度，用於您之前方案未使用的部分。
{% endif %}

改變主意了嗎？
您可以隨時升級回 {{ old_plan_name }}。

升級方案：{{ upgrade_url }}
查看我的訂閱：{{ account_url }}