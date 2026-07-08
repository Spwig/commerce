---
template_type: pos_high_value_transaction
category: POS
---

# Email Template: pos_high_value_transaction

## Subject
💰 高價值交易：{{ transaction_amount }} 於 {{ terminal_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          💰 高價值交易
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          已處理大額交易
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          在 {{ terminal_name }} 處理了一筆 {{ transaction_amount }} 的交易。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              交易詳情：
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>金額：</strong> <span style="font-size: 18px; font-weight: bold; color: #059669;">{{ transaction_amount }}</span><br/>
              <strong>終端機：</strong> {{ terminal_name }}<br/>
              <strong>收銀員：</strong> {{ cashier_name }}<br/>
              <strong>時間戳：</strong> {{ transaction_time }}<br/>
              <strong>交易 ID：</strong> {{ transaction_id }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          支付資訊：
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            {% for payment in payment_methods %}
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>{{ payment.method }}</strong>：{{ payment.amount }}
            </mj-text>
            {% endfor %}
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          商品總覽：
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>總商品數：</strong> {{ item_count }}<br/>
              <strong>小計：</strong> {{ subtotal }}<br/>
              <strong>稅款：</strong> {{ tax_amount }}<br/>
              <strong>總計：</strong> {{ transaction_amount }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if customer_info %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          顧客資訊：
        </mj-text>
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              {{ customer_info }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              本通知會發送給所有超過 {{ threshold_amount }} 的交易，以防止欺詐和監控。
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ transaction_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          查看交易
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ receipt_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          查看收據
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
💰 高價值交易

已處理大額交易

在 {{ terminal_name }} 處理了一筆 {{ transaction_amount }} 的交易。

交易詳情：
- 金額：{{ transaction_amount }}
- 終端機：{{ terminal_name }}
- 收銀員：{{ cashier_name }}
- 時間戳：{{ transaction_time }}
- 交易 ID：{{ transaction_id }}

支付資訊：
{% for payment in payment_methods %}
{{ payment.method }}：{{ payment.amount }}
{% endfor %}

商品總覽：
- 總商品數：{{ item_count }}
- 小計：{{ subtotal }}
- 稅款：{{ tax_amount }}
- 總計：{{ transaction_amount }}

{% if customer_info %}
顧客資訊：
{{ customer_info }}
{% endif %}

本通知會發送給所有超過 {{ threshold_amount }} 的交易，以防止欺詐和監控。

查看交易：{{ transaction_url }}
查看收據：{{ receipt_url }}