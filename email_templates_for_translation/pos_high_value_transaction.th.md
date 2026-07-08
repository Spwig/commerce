---
template_type: pos_high_value_transaction
category: POS
---

# Email Template: pos_high_value_transaction

## Subject
💰 การทำธุรกรรมมูลค่าสูง: {{ transaction_amount }} ที่ {{ terminal_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          💰 การทำธุรกรรมมูลค่าสูง
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          การทำธุรกรรมขนาดใหญ่ได้รับการประมวลผล
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          การทำธุรกรรมจำนวน {{ transaction_amount }} ได้รับการประมวลผลที่ {{ terminal_name }}.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              รายละเอียดการทำธุรกรรม:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Amount:</strong> <span style="font-size: 18px; font-weight: bold; color: #059669;">{{ transaction_amount }}</span><br/>
              <strong>Terminal:</strong> {{ terminal_name }}<br/>
              <strong>Cashier:</strong> {{ cashier_name }}<br/>
              <strong>Timestamp:</strong> {{ transaction_time }}<br/>
              <strong>Transaction ID:</strong> {{ transaction_id }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Payment Information:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            {% for payment in payment_methods %}
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>{{ payment.method }}</strong>: {{ payment.amount }}
            </mj-text>
            {% endfor %}
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Items Summary:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Total Items:</strong> {{ item_count }}<br/>
              <strong>Subtotal:</strong> {{ subtotal }}<br/>
              <strong>Tax:</strong> {{ tax_amount }}<br/>
              <strong>Total:</strong> {{ transaction_amount }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if customer_info %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Customer Information:
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
              การแจ้งเตือนนี้ถูกส่งสำหรับการทำธุรกรรมทั้งหมดที่สูงกว่า {{ threshold_amount }} เพื่อป้องกันและตรวจสอบการฉ้อโกง
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ transaction_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          View Transaction
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ receipt_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          View Receipt
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
💰 การทำธุรกรรมมูลค่าสูง

การทำธุรกรรมขนาดใหญ่ได้รับการประมวลผล

การทำธุรกรรมจำนวน {{ transaction_amount }} ได้รับการประมวลผลที่ {{ terminal_name }}.

รายละเอียดการทำธุรกรรม:
- Amount: {{ transaction_amount }}
- Terminal: {{ terminal_name }}
- Cashier: {{ cashier_name }}
- Timestamp: {{ transaction_time }}
- Transaction ID: {{ transaction_id }}

PAYMENT INFORMATION:
{% for payment in payment_methods %}
{{ payment.method }}: {{ payment.amount }}
{% endfor %}

ITEMS SUMMARY:
- Total Items: {{ item_count }}
- Subtotal: {{ subtotal }}
- Tax: {{ tax_amount }}
- Total: {{ transaction_amount }}

{% if customer_info %}
CUSTOMER INFORMATION:
{{ customer_info }}
{% endif %}

การแจ้งเตือนนี้ถูกส่งสำหรับการทำธุรกรรมทั้งหมดที่สูงกว่า {{ threshold_amount }} เพื่อป้องกันและตรวจสอบการฉ้อโกง

View transaction: {{ transaction_url }}
View receipt: {{ receipt_url }}