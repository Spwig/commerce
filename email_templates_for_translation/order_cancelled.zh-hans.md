---
template_type: order_cancelled
category: Core E-commerce
---

# Email Template: order_cancelled

## Subject
您的订单 #{{ order_number }} 已被取消

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          订单已取消
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          你好 {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          您的订单 <strong>#{{ order_number }}</strong> 已被取消。
        </mj-text>

        {% if cancellation_reason %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>原因：</strong> {{ cancellation_reason }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          如果已支付，将根据原始支付方式处理退款。
        </mj-text>

        <mj-spacer height="30px" />

        {% if order_url %}
        <mj-button href="{{ order_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          查看订单详情
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
订单已取消

你好 {{ customer_name }},

您的订单 #{{ order_number }} 已被取消。

{% if cancellation_reason %}原因： {{ cancellation_reason }}{% endif %}

如果已支付，将根据原始支付方式处理退款。

{% if order_url %}查看订单详情： {{ order_url }}{% endif %}

有关此取消的疑问？
电子邮件：{{ support_email }}
电话：{{ support_phone }}