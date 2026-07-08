---
template_type: pos_daily_z_report
category: POS
---

# Email Template: pos_daily_z_report

## Subject
📊 Báo cáo Z hàng ngày - {{ report_date }} - {{ location_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📊 Báo cáo Z hàng ngày
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Báo cáo Kết thúc Ca làm việc
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Tổng kết hàng ngày cho {{ location_name }} ngày {{ report_date }}.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Tổng kết Doanh thu:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Tổng doanh thu:</strong> <span style="font-size: 20px; font-weight: bold; color: #059669;">{{ total_sales }}</span><br/>
              <strong>Giao dịch:</strong> {{ transaction_count }}<br/>
              <strong>Sản phẩm bán được:</strong> {{ items_sold }}<br/>
              <strong>Trung bình mỗi giao dịch:</strong> {{ average_sale }}<br/>
              <strong>Thuế thu được:</strong> {{ tax_collected }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Phương thức thanh toán:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            {% for payment in payment_methods %}
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>{{ payment.method }}:</strong> {{ payment.amount }} ({{ payment.count }} giao dịch)
            </mj-text>
            {% endfor %}
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Tổng kết Ca làm việc:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Tổng số ca làm việc:</strong> {{ shift_count }}<br/>
              <strong>Số máy POS đã sử dụng:</strong> {{ terminal_count }}<br/>
              <strong>Số nhân viên thu ngân đang làm việc:</strong> {{ cashier_count }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% for terminal in terminal_stats %}
        <mj-spacer height="15px" />
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ terminal.name }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              Doanh thu: {{ terminal.sales }} | Giao dịch: {{ terminal.transactions }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Các điều chỉnh & Giảm giá:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Giảm giá đã áp dụng:</strong> {{ discounts_total }}<br/>
              <strong>Hoàn tiền đã phát hành:</strong> {{ refunds_total }}<br/>
              <strong>Hủy giao dịch:</strong> {{ voids_total }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if cash_variance != 0 %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ Tổng chênh lệch tiền mặt: {{ cash_variance }}
            </mj-text>
            <mj-text font-size="14px" color="#92400e">
              {{ variance_note }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Sản phẩm bán chạy nhất:
        </mj-text>

        {% for product in top_products %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>{{ product.rank }}. {{ product.name }}</strong> - {{ product.quantity }} sản phẩm bán được ({{ product.revenue }})
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="8px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-button href="{{ full_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Xem báo cáo đầy đủ
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📊 BÁO CÁO Z HÀNG NGÀY

Báo cáo Kết thúc Ca làm việc

Tổng kết hàng ngày cho {{ location_name }} ngày {{ report_date }}.

TỔNG KẾT DOANH THU:
- Tổng doanh thu: {{ total_sales }}
- Giao dịch: {{ transaction_count }}
- Sản phẩm bán được: {{ items_sold }}
- Trung bình mỗi giao dịch: {{ average_sale }}
- Thuế thu được: {{ tax_collected }}

PHƯƠNG THỨC THANH TOÁN:
{% for payment in payment_methods %}
{{ payment.method }}: {{ payment.amount }} ({{ payment.count }} giao dịch)
{% endfor %}

TỔNG KẾT CA LÀM VIỆC:
- Tổng số ca làm việc: {{ shift_count }}
- Số máy POS đã sử dụng: {{ terminal_count }}
- Số nhân viên thu ngân đang làm việc: {{ cashier_count }}

TÌNH HÌNH CÁC MÁY POS:
{% for terminal in terminal_stats %}
{{ terminal.name }}: {{ terminal.sales }} | {{ terminal.transactions }} giao dịch
{% endfor %}

CÁC ĐIỀU CHỈNH & GIẢM GIÁ:
- Giảm giá đã áp dụng: {{ discounts_total }}
- Hoàn tiền đã phát hành: {{ refunds_total }}
- Hủy giao dịch: {{ voids_total }}

{% if cash_variance != 0 %}
⚠️ TỔNG CHÊNH LỆCH TIỀN MẶT: {{ cash_variance }}
{{ variance_note }}
{% endif %}

SẢN PHẨM BÁN CHẠY NHẤT:
{% for product in top_products %}
{{ product.rank }}. {{ product.name }} - {{ product.quantity }} sản phẩm bán được ({{ product.revenue }})
{% endfor %}

Xem báo cáo đầy đủ: {{ full_report_url }}