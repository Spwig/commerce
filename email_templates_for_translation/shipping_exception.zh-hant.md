---
template_type: shipping_exception
category: Shipping
---

# Email Template: shipping_exception

## Subject
運輸異常 - 訂單 #{{ order_number }} 需要處理

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ 運輸異常
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          我們寫這封信是為了通知您有關運輸的異常情況。我們正在努力盡快解決這個問題。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fef3c7" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#92400e">
              異常詳情：
            </mj-text>
            <mj-text color="#92400e">
              <strong>異常類型：</strong> {{ exception_type }}<br/>
              <strong>描述：</strong> {{ exception_description }}<br/>
              <strong>發生時間：</strong> {{ exception_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              訂單資訊：
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>訂單編號：</strong> {{ order_number }}<br/>
              <strong>追蹤編號：</strong> {{ tracking_number }}<br/>
              <strong>運送商：</strong> {{ carrier_name }}<br/>
              <strong>目前位置：</strong> {{ current_location }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          接下來會發生什麼？
        </mj-text>

        <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
          {{ resolution_steps }}
        </mj-text>

        <mj-spacer height="20px" />

        {% if action_required %}
        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              ⚠️ 需要操作：
            </mj-text>
            <mj-text color="#7f1d1d">
              {{ action_required_description }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="20px" />
        {% endif %}

        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          追蹤您的訂單
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          聯絡支援
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ 運輸異常

Hi {{ customer_name }},

我們寫這封信是為了通知您有關運輸的異常情況。我們正在努力盡快解決這個問題。

異常詳情：
- 異常類型：{{ exception_type }}
- 描述：{{ exception_description }}
- 發生時間：{{ exception_date }}

訂單資訊：
- 訂單編號：{{ order_number }}
- 追蹤編號：{{ tracking_number }}
- 運送商：{{ carrier_name }}
- 目前位置：{{ current_location }}

接下來會發生什麼？
{{ resolution_steps }}

{% if action_required %}
⚠️ 需要操作：
{{ action_required_description }}
{% endif %}

追蹤您的訂單：{{ tracking_url }}
聯絡支援：{{ support_url }}