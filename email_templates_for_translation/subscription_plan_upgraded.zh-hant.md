---
template_type: subscription_plan_upgraded
category: Subscriptions
---

# Email Template: subscription_plan_upgraded

## Subject
✓ 您的訂閱方案已升級！

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          ✓ 訂閱方案已升級！
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          歡迎加入 {{ new_plan_name }}
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          您的訂閱方案已成功升級。您現在可以享受 {{ new_plan_name }} 的所有優惠！
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              訂閱變更詳情：
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Previous Plan:</strong> {{ old_plan_name }}<br/>
              <strong>New Plan:</strong> {{ new_plan_name }}<br/>
              <strong>Upgraded On:</strong> {{ upgrade_date }}<br/>
              <strong>Effective Immediately</strong>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          最新功能：
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ new_features }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          計費資訊：
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>New Price:</strong> {{ new_price }} / {{ billing_period }}<br/>
              <strong>Next Billing Date:</strong> {{ next_billing_date }}<br/>
              {% if prorated_charge %}<strong>Prorated Charge Today:</strong> {{ prorated_charge }}{% endif %}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if prorated_charge %}
        <mj-spacer height="20px" />
        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              💡 您今天已為當前計費週期的剩餘部分收取 {{ prorated_charge }}。
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ account_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          查看我的訂閱
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          有問題？<a href="{{ support_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">聯繫支援</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ 訂閱方案已升級！

歡迎加入 {{ new_plan_name }}

Hi {{ customer_name }},

您的訂閱方案已成功升級。您現在可以享受 {{ new_plan_name }} 的所有優惠！

訂閱變更詳情：
- 原方案：{{ old_plan_name }}
- 新方案：{{ new_plan_name }}
- 升級日期：{{ upgrade_date }}
- 立即生效

最新功能：
{{ new_features }}

計費資訊：
- 新價格：{{ new_price }} / {{ billing_period }}
- 下次計費日期：{{ next_billing_date }}
{% if prorated_charge %}- 今日按比例收費：{{ prorated_charge }}{% endif %}

{% if prorated_charge %}
💡 您今天已為當前計費週期的剩餘部分收取 {{ prorated_charge }}。
{% endif %}

查看我的訂閱：{{ account_url }}
有問題？聯繫支援：{{ support_url }}