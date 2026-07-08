---
template_type: subscription_addon_removed
category: Subscriptions
---

# Email Template: subscription_addon_removed

## Subject
已從您的訂閱中移除 {{ addon_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          套件移除
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          套件移除
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ addon_name }} 已從您的 {{ plan_name }} 訂閱中移除。
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              移除細節：
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>套件：</strong> {{ addon_name }}<br/>
              <strong>訂閱：</strong> {{ plan_name }}<br/>
              <strong>移除日期：</strong> {{ removed_date }}<br/>
              <strong>生效日期：</strong> {{ effective_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if access_until %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              使用權至 {{ access_until }}
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              您將會持續擁有 {{ addon_name }} 的使用權，直到目前的計費週期結束。
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
              <strong>先前總金額：</strong> {{ old_total }} / {{ billing_period }}<br/>
              <strong>套件價格：</strong> -{{ addon_price }} / {{ billing_period }}<br/>
              <strong>新總金額：</strong> {{ new_total }} / {{ billing_period }}<br/>
              <strong>生效日期：</strong> {{ effective_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if credit_applied %}
        <mj-spacer height="20px" />
        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              💰 您的帳戶已應用 {{ credit_amount }} 的信用額度，用於此套件未使用的部分。
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        {% if data_retention_info %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          重要資訊：
        </mj-text>
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ data_retention_info }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          需要恢復？
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          您可以隨時將 {{ addon_name }} 再次加入您的訂閱。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-button href="{{ addons_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          瀏覽套件
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
套件移除

套件移除

Hi {{ customer_name }},

{{ addon_name }} 已從您的 {{ plan_name }} 訂閱中移除。

移除細節：
- 套件：{{ addon_name }}
- 訂閱：{{ plan_name }}
- 移除日期：{{ removed_date }}
- 生效日期：{{ effective_date }}

{% if access_until %}
使用權至 {{ access_until }}：
您將會持續擁有 {{ addon_name }} 的使用權，直到目前的計費週期結束。
{% endif %}

計費資訊：
- 先前總金額：{{ old_total }} / {{ billing_period }}
- 套件價格：-{{ addon_price }} / {{ billing_period }}
- 新總金額：{{ new_total }} / {{ billing_period }}
- 生效日期：{{ effective_date }}

{% if credit_applied %}
💰 您的帳戶已應用 {{ credit_amount }} 的信用額度，用於此套件未使用的部分。
{% endif %}

{% if data_retention_info %}
重要資訊：
{{ data_retention_info }}
{% endif %}

需要恢復？
您可以隨時將 {{ addon_name }} 再次加入您的訂閱。

瀏覽套件：{{ addons_url }}
查看我的訂閱：{{ account_url }}