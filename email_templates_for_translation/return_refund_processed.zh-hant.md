---
template_type: return_refund_processed
category: Returns
---

# Email Template: return_refund_processed

## Subject
退款已完成 - 訂單 #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f0fdf4' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#166534' }}">
          退款已完成
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#166534' }}">
          訂單 #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          您的退貨申請針對訂單 <strong>#{{ order_number }}</strong> 已經完成檢查，退款也已經處理完成。
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f0fdf4' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#166534' }}">
              退款明細
            </mj-text>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>退款金額：</strong> {{ refund_currency }} {{ refund_amount }}
            </mj-text>
            {% if restocking_fee %}
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>退貨手續費：</strong> {{ restocking_fee_currency }} {{ restocking_fee }}
            </mj-text>
            {% endif %}
          </mj-column>
        </mj-section>

        <mj-section background-color="{{ theme.color.surface|default:'#fffbeb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#92400e' }}">
              <strong>注意：</strong> 退款可能會根據您的支付提供商，需要 5-10 個工作天才會出現在您的帳戶中。
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          如果您對退款有任何疑問，請聯繫我們的客服團隊。
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
退款已完成 - 訂單 #{{ order_number }}

Hi {{ customer_name }},

您的退貨申請針對訂單 #{{ order_number }} 已經完成檢查，退款也已經處理完成。

退款明細：
- 退款金額：{{ refund_currency }} {{ refund_amount }}
{% if restocking_fee %}- 退貨手續費：{{ restocking_fee_currency }} {{ restocking_fee }}{% endif %}

注意：退款可能會根據您的支付提供商，需要 5-10 個工作天才會出現在您的帳戶中。

如果您對退款有任何疑問，請聯繫我們的客服團隊。