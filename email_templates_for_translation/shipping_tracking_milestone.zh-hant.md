---
template_type: shipping_tracking_milestone
category: Shipping
---

# Email Template: shipping_tracking_milestone

## Subject
您的訂單 #{{ order_number }} 當前狀態為 {{ milestone_status }} - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          配送狀態更新：{{ milestone_status }}
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          好消息！您的訂單在運送到您的過程中達到了一個重要的里程碑。
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
              📦 {{ milestone_status }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
              {{ milestone_description }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              訂單詳情：
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>訂單編號：</strong> {{ order_number }}<br/>
              <strong>追蹤編號：</strong> {{ tracking_number }}<br/>
              <strong>運送商：</strong> {{ carrier_name }}<br/>
              <strong>目前位置：</strong> {{ current_location }}<br/>
              <strong>預計送達：</strong> {{ estimated_delivery }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          跟蹤您的包裹
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          有關您的配送有任何問題？<a href="{{ support_url }.ogg">聯繫支援</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
配送狀態更新：{{ milestone_status }}

Hi {{ customer_name }},

好消息！您的訂單在運送到您的過程中達到了一個重要的里程碑。

📦 {{ milestone_status }}
{{ milestone_description }}

ORDER DETAILS:
- 訂單編號：{{ order_number }}
- 追蹤編號：{{ tracking_number }}
- 運送商：{{ carrier_name }}
- 目前位置：{{ current_location }}
- 預計送達：{{ estimated_delivery }}

跟蹤您的包裹：{{ tracking_url }}

有關您的配送有任何問題？聯繫支援：{{ support_url }}