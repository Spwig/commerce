---
template_type: return_refund_processed
category: Returns
---

# Email Template: return_refund_processed

## Subject
退款已完成 - 订单 #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f0fdf4' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#166534' }}">
          退款已完成
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
          你关于订单 <strong>#{{ order_number }}</strong> 的退货已审核，退款已处理。
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f0fdf4' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#166534' }}">
              退款详情
            </mj-text>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>退款金额：</strong> {{ refund_currency }} {{ refund_amount }}
            </mj-text>
            {% if restocking_fee %}
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>退货手续费：</strong> {{ restocking_fee_currency }} {{ restocking_fee }}
            </mj-text>
            {% endif %}
          </mj-column>
        </mj-section>

        <mj-section background-color="{{ theme.color.surface|default:'#fffbeb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#92400e' }}">
              <strong>注意：</strong> 退款可能需要 5-10 个工作日才会出现在你的账户中，具体时间取决于你的支付提供商。
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          如果你对退款有任何疑问，请联系我们的支持团队。
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
退款已完成 - 订单 #{{ order_number }}

你好 {{ customer_name }}，

你关于订单 #{{ order_number }} 的退货已审核，退款已处理。

退款详情：
- 退款金额：{{ refund_currency }} {{ refund_amount }}
{% if restocking_fee %}- 退货手续费：{{ restocking_fee_currency }} {{ restocking_fee }}{% endif %}

注意：退款可能需要 5-10 个工作日才会出现在你的账户中，具体时间取决于你的支付提供商。

如果你对退款有任何疑问，请联系我们的支持团队。