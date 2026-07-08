---
template_type: shipping_tracking_milestone
category: Shipping
---

# Email Template: shipping_tracking_milestone

## Subject
您的订单 #{{ order_number }} 的状态是 {{ milestone_status }} - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          配送更新：{{ milestone_status }}
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          好消息！您的订单在运送到您的过程中达到了一个重要里程碑。
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
              订单详情：
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>订单编号：</strong>{{ order_number }}<br/>
              <strong>追踪编号：</strong>{{ tracking_number }}<br/>
              <strong>承运商：</strong>{{ carrier_name }}<br/>
              <strong>当前位置：</strong>{{ current_location }}<br/>
              <strong>预计送达时间：</strong>{{ estimated_delivery }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          跟踪您的包裹
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          关于您的配送有任何问题？<a href="{{ support_url }.ogg">联系支持</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
配送更新：{{ milestone_status }}

Hi {{ customer_name }},

好消息！您的订单在运送到您的过程中达到了一个重要里程碑。

📦 {{ milestone_status }}
{{ milestone_description }}

订单详情：
- 订单编号：{{ order_number }}
- 追踪编号：{{ tracking_number }}
- 承运商：{{ carrier_name }}
- 当前位置：{{ current_location }}
- 预计送达时间：{{ estimated_delivery }}

跟踪您的包裹：{{ tracking_url }}

关于您的配送有任何问题？联系支持：{{ support_url }}