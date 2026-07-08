---
template_type: return_request_approved
category: Returns
---

# Email Template: return_request_approved

## Subject
您的退货已获批准 - 订单 #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f0fdf4' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#166534' }}">
          退货已获批准
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#166534' }}">
          订单 #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          你好 {{ customer_name }}，
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          您的订单 <strong>#{{ order_number }}</strong> 的退货请求已获批准。
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>下一步：</strong>
        </mj-text>

        <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
          1. 下载并打印下方的退货标签<br/>
          2. 如果可能，请将商品安全地装回原包装中<br/>
          3. 将退货标签贴在包裹的外侧<br/>
          4. 送到您最近的快递点
        </mj-text>

        {% if return_label_url %}
        <mj-spacer height="20px" />
        <mj-button href="{{ return_label_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          下载退货标签
        </mj-button>
        {% endif %}

        {% if return_tracking_number %}
        <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>退货追踪编号：</strong> {{ return_tracking_number }}
        </mj-text>
        {% endif %}

        <mj-section background-color="{{ theme.color.surface|default:'#fffbeb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#92400e' }}">
              <strong>重要：</strong> 请在7天内寄回退货，以确保您的退款能及时处理。
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          一旦我们收到并检查您的退货，我们将把退款处理到原始的支付方式。
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
退货已获批准 - 订单 #{{ order_number }}

你好 {{ customer_name }}，

您的订单 #{{ order_number }} 的退货请求已获批准。

下一步：
1. 下载并打印退货标签
2. 如果可能，请将商品安全地装回原包装中
3. 将退货标签贴在包裹的外侧
4. 送到您最近的快递点

{% if return_label_url %}下载退货标签： {{ return_label_url }}{% endif %}
{% if return_tracking_number %}退货追踪编号： {{ return_tracking_number }}{% endif %}

重要：请在7天内寄回退货，以确保您的退款能及时处理。

一旦我们收到并检查您的退货，我们将把退款处理到原始的支付方式。