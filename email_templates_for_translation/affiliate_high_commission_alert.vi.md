---
template_type: affiliate_high_commission_alert
category: Affiliate Program
---

# Email Template: affiliate_high_commission_alert

## Subject
⚠️ Phát hiện hoạt động hoa hồng bất thường - {{ affiliate_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Cảnh báo hoa hồng cao
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Phát hiện hoạt động bất thường
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Một khoản hoa hồng bất thường cao đã được tạo bởi đại lý {{ affiliate_name }}. Điều này cần được xem xét để ngăn chặn gian lận.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Chi tiết cảnh báo:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Đại lý:</strong> {{ affiliate_name }} ({{ affiliate_id }})<br/>
              <strong>Số tiền hoa hồng:</strong> <span style="font-weight: bold; color: #dc2626;">{{ commission_amount }}</span><br/>
              <strong>Giá trị đơn hàng:</strong> {{ order_value }}<br/>
              <strong>Mã đơn hàng:</strong> {{ order_number }}<br/>
              <strong>Phát hiện:</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Tại sao điều này bị đánh dấu:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ flag_reason }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Các hành động được đề xuất:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • Kiểm tra chi tiết đơn hàng để đảm bảo tính hợp lệ<br/>
          • Kiểm tra lịch sử giới thiệu của đại lý<br/>
          • Xác minh khách hàng không liên quan đến người giới thiệu<br/>
          • Duyệt hoặc từ chối hoa hồng trong bảng điều khiển quản trị
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ review_commission_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Xem xét hoa hồng
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ affiliate_details_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Xem chi tiết đại lý
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Khoản hoa hồng này đang chờ xem xét và sẽ không được thanh toán cho đến khi được phê duyệt.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ CẢNH BÁO HOA HỒNG CAO

Phát hiện hoạt động bất thường

Một khoản hoa hồng bất thường cao đã được tạo bởi đại lý {{ affiliate_name }}. Điều này cần được xem xét để ngăn chặn gian lận.

CHI TIẾT CẢNH BÁO:
- Đại lý: {{ affiliate_name }} ({{ affiliate_id }})
- Số tiền hoa hồng: {{ commission_amount }}
- Giá trị đơn hàng: {{ order_value }}
- Mã đơn hàng: {{ order_number }}
- Phát hiện: {{ detected_at }}

TẠI SAO ĐIỀU NÀY BỊ ĐÁNH DẤU:
{{ flag_reason }}

CÁC HÀNH ĐỘNG ĐƯỢC ĐỀ NGHỊ:
• Kiểm tra chi tiết đơn hàng để đảm bảo tính hợp lệ
• Kiểm tra lịch sử giới thiệu của đại lý
• Xác minh khách hàng không liên quan đến người giới thiệu
• Duyệt hoặc từ chối hoa hồng trong bảng điều khiển quản trị

Xem xét hoa hồng: {{ review_commission_url }}
Xem chi tiết đại lý: {{ affiliate_details_url }}

Khoản hoa hồng này đang chờ xem xét và sẽ không được thanh toán cho đến khi được phê duyệt.