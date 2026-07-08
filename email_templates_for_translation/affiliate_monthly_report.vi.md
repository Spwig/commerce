---
template_type: affiliate_monthly_report
category: Affiliate Program
---

# Email Template: affiliate_monthly_report

## Subject
Báo cáo đại lý hàng tháng - {{ month_name }} {{ year }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="#f8f9fa">
    <!-- Header -->
    <mj-section background-color="#ffffff" padding="40px 20px">
      <mj-column>
        <mj-text font-size="32px" font-weight="bold" color="#212529" align="center">
          📊 Báo cáo đại lý hàng tháng
        </mj-text>
        <mj-text font-size="18px" color="#6c757d" align="center">
          Tóm tắt hiệu suất {{ month_name }} {{ year }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Summary Cards -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column width="33%">
        <mj-text font-size="14px" color="#6c757d" align="center" padding-bottom="5px">
          💰 Tổng số tiền đã kiếm được
        </mj-text>
        <mj-text font-size="28px" font-weight="bold" color="#28a745" align="center" line-height="1">
          {{ total_earned }}
        </mj-text>
      </mj-column>
      <mj-column width="33%">
        <mj-text font-size="14px" color="#6c757d" align="center" padding-bottom="5px">
          📦 Số lượng hoa hồng
        </mj-text>
        <mj-text font-size="28px" font-weight="bold" color="#007bff" align="center" line-height="1">
          {{ commission_count }}
        </mj-text>
      </mj-column>
      <mj-column width="33%">
        <mj-text font-size="14px" color="#6c757d" align="center" padding-bottom="5px">
          📈 Trung bình mỗi giao dịch
        </mj-text>
        <mj-text font-size="28px" font-weight="bold" color="#6f42c1" align="center" line-height="1">
          {{ avg_commission }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section background-color="#f8f9fa" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          Chào {{ affiliate_name }},
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Đây là hiệu suất của bạn cho tháng {{ month_name }} {{ year }}. Công việc tuyệt vời trong tháng này!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Top Orders Table -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="#212529" padding-bottom="15px">
          🏆 Top {{ top_orders_count }} Đơn hàng
        </mj-text>
        <mj-text font-size="14px" color="#212529">
          <table style="width: 100%; border-collapse: collapse;">
            <thead>
              <tr style="background-color: #f8f9fa;">
                <th style="padding: 10px; text-align: left; border-bottom: 2px solid #dee2e6;">Đơn hàng</th>
                <th style="padding: 10px; text-align: right; border-bottom: 2px solid #dee2e6;">Hoa hồng</th>
                <th style="padding: 10px; text-align: right; border-bottom: 2px solid #dee2e6;">Ngày</th>
              </tr>
            </thead>
            <tbody>
              {% for order in top_orders %}
              <tr>
                <td style="padding: 10px; border-bottom: 1px solid #dee2e6;">#{{ order.order_number }}</td>
                <td style="padding: 10px; text-align: right; border-bottom: 1px solid #dee2e6; color: #28a745; font-weight: 600;">{{ order.commission_amount }}</td>
                <td style="padding: 10px; text-align: right; border-bottom: 1px solid #dee2e6; color: #6c757d;">{{ order.order_date }}</td>
              </tr>
              {% endfor %}
            </tbody>
          </table>
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Payment Status -->
    <mj-section background-color="#e3f2fd" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          <strong>💳 Trạng thái thanh toán</strong>
        </mj-text>
        <mj-text font-size="14px" color="#212529">
          Số dư chờ: <strong>{{ pending_balance }}</strong><br/>
          Trạng thái: {{ payment_status }}
          {% if next_payout_date %}
          <br/>Ngày thanh toán tiếp theo: {{ next_payout_date }}
          {% endif %}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          Xem bảng điều khiển đầy đủ
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          Có câu hỏi? <a href="mailto:{{ support_email }}" style="color: #007bff;">Liên hệ hỗ trợ</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Báo cáo đại lý hàng tháng - {{ month_name }} {{ year }}

Chào {{ affiliate_name }},

Đây là hiệu suất của bạn cho {{ month_name }} {{ year }}:

📊 TÓM TẮT THÁNG
- Tổng số tiền đã kiếm được: {{ total_earned }}
- Số lượng hoa hồng: {{ commission_count }}
- Trung bình mỗi giao dịch: {{ avg_commission }}

🏆 TOP {{ top_orders_count }} ĐƠN HÀNG
{% for order in top_orders %}
#{{ order.order_number }} - {{ order.commission_amount }} ({{ order.order_date }})
{% endfor %}

💳 TRẠNG THÁI THANH TOÁN
Số dư chờ: {{ pending_balance }}
Trạng thái: {{ payment_status }}
{% if next_payout_date %}Ngày thanh toán tiếp theo: {{ next_payout_date }}{% endif %}

Xem bảng điều khiển đầy đủ: {{ portal_url }}

Công việc tuyệt vời trong tháng này!

{{ shop_name }}
Có câu hỏi? Liên hệ {{ support_email }}
