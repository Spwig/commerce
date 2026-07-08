---
template_type: order_shipped
category: Core E-commerce
---

# Email Template: order_shipped

## Subject
您的订单 #{{ order_number }} 已发货！

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          📦 订单已发货！
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          正在运送中！
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          你好 {{ customer_name }}，
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          好消息！您的订单已发货，正在运往您的途中。
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              运送详情：
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>订单 #: </strong>{{ order_number }}<br/>
              <strong>追踪 #: </strong>{{ tracking_number }}<br/>
              <strong>承运商: </strong>{{ carrier_name }}<br/>
              <strong>预估送达时间: </strong>{{ estimated_delivery }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          追踪您的包裹
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📦 订单已发货！

正在运送中！

你好 {{ customer_name }}，

好消息！您的订单已发货，正在运往您的途中。

运送详情：
- 订单 #: {{ order_number }}
- 追踪 #: {{ tracking_number }}
- 承运商: {{ carrier_name }}
- 预估送达时间: {{ estimated_delivery }}

追踪您的包裹：{{ tracking_url }}