---
template_type: pos_high_value_transaction
category: POS
---

# Email Template: pos_high_value_transaction

## Subject
💰 Giao dịch có giá trị cao: {{ transaction_amount }} tại {{ terminal_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          💰 Giao dịch có giá trị cao
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Giao dịch lớn đã được xử lý
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Một giao dịch trị giá {{ transaction_amount }} đã được xử lý tại {{ terminal_name }}.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Chi tiết giao dịch:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Số tiền:</strong> <span style="font-size: 18px; font-weight: bold; color: #059669;">{{ transaction_amount }}</span><br/>
              <strong>Máy POS:</strong> {{ terminal_name }}<br/>
              <strong>Thu ngân:</strong> {{ cashier_name }}<br/>
              <strong>Thời gian:</strong> {{ transaction_time }}<br/>
              <strong>Mã giao dịch:</strong> {{ transaction_id }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Thông tin thanh toán:
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
          Tổng quan mặt hàng:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Tổng số mặt hàng:</strong> {{ item_count }}<br/>
              <strong>Tổng phụ:</strong> {{ subtotal }}<br/>
              <strong>Thuế:</strong> {{ tax_amount }}<br/>
              <strong>Tổng cộng:</strong> {{ transaction_amount }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if customer_info %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Thông tin khách hàng:
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
              Thông báo này được gửi cho tất cả các giao dịch vượt quá {{ threshold_amount }} nhằm mục đích phòng chống và giám sát gian lận.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ transaction_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Xem giao dịch
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ receipt_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Xem hóa đơn
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
💰 GIAO DỊCH CÓ GIÁ TRỊ CAO

Giao dịch lớn đã được xử lý

Một giao dịch trị giá {{ transaction_amount }} đã được xử lý tại {{ terminal_name }}.

CHI TIẾT GIAO DỊCH:
- Số tiền: {{ transaction_amount }}
- Máy POS: {{ terminal_name }}
- Thu ngân: {{ cashier_name }}
- Thời gian: {{ transaction_time }}
- Mã giao dịch: {{ transaction_id }}

THÔNG TIN THANH TOÁN:
{% for payment in payment_methods %}
{{ payment.method }}: {{ payment.amount }}
{% endfor %}

TỔNG QUAN MẶT HÀNG:
- Tổng số mặt hàng: {{ item_count }}
- Tổng phụ: {{ subtotal }}
- Thuế: {{ tax_amount }}
- Tổng cộng: {{ transaction_amount }}

{% if customer_info %}
THÔNG TIN KHÁCH HÀNG:
{{ customer_info }}
{% endif %}

Thông báo này được gửi cho tất cả các giao dịch vượt quá {{ threshold_amount }} nhằm mục đích phòng chống và giám sát gian lận.

Xem giao dịch: {{ transaction_url }}
Xem hóa đơn: {{ receipt_url }}