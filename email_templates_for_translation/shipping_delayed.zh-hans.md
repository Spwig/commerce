---
template_type: shipping_delayed
category: Shipping
---

# Email Template: shipping_delayed

## Subject
关于您的订单 #{{ order_number }} - 配送延迟

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          关于您的订单的更新
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          你好 {{ customer_name }}，
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          我们想通知您有关订单的延迟情况。我们为由此带来的不便表示歉意，并感谢您的耐心等待。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              订单详情：
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>订单号：</strong> {{ order_number }}<br/>
              <strong>原预计送达时间：</strong> {{ original_delivery_date }}<br/>
              <strong>新预计送达时间：</strong> {{ new_delivery_date }}<br/>
              <strong>追踪号：</strong> {{ tracking_number }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          延迟原因：
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ delay_reason }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          追踪您的订单
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          我们正在努力尽快将您的订单送达。当包裹开始运输时，您将收到另一条更新信息。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          有问题吗？ <a href="{{ support_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">联系我们的客户服务团队</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
关于您的订单 #{{ order_number }}

你好 {{ customer_name }}，

我们想通知您有关订单的延迟情况。我们为由此带来的不便表示歉意，并感谢您的耐心等待。

订单详情：
- 订单号：{{ order_number }}
- 原预计送达时间：{{ original_delivery_date }}
- 新预计送达时间：{{ new_delivery_date }}
- 追踪号：{{ tracking_number }}

延迟原因：
{{ delay_reason }}

追踪您的订单：{{ tracking_url }}

我们正在努力尽快将您的订单送达。当包裹开始运输时，您将收到另一条更新信息。

有问题吗？联系我们的客户服务团队：{{ support_url }}

---
此更新是针对 {{ shop_name }} 的订单 #{{ order_number }}。