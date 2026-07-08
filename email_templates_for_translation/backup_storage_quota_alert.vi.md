---
template_type: backup_storage_quota_alert
category: Backups
---

# Email Template: backup_storage_quota_alert

## Subject
🚨 Quota Lưu trữ Sao lưu Đã tới Giới hạn - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef2f2">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#dc2626" align="center">
          🚨 Quota Lưu trữ Đã tới Giới hạn
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>KHẨN CẤP:</strong> Lưu trữ sao lưu của bạn đang ở mức rất thấp. Các bản sao lưu trong tương lai có thể thất bại nếu không giải phóng không gian lưu trữ.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              Trạng thái lưu trữ:
            </mj-text>
            <mj-text color="#7f1d1d">
              <strong>Đã dùng:</strong> {{ storage_used }} của {{ storage_total }}<br/>
              <strong>Tỷ lệ sử dụng:</strong> {{ storage_percentage }}%<br/>
              <strong>Còn lại:</strong> {{ storage_available }}<br/>
              <strong>Trạng thái:</strong> <span style="color: #dc2626; font-weight: bold;">{{ storage_status }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="#fef3c7" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#92400e">
              Các hành động cần thực hiện ngay:
            </mj-text>
            <mj-text color="#92400e">
              1. Xóa các bản sao lưu cũ không còn cần thiết<br/>
              2. Lưu trữ các bản sao lưu vào thiết bị ngoài<br/>
              3. Tăng dung lượng lưu trữ<br/>
              4. Xem lại chính sách lưu trữ sao lưu<br/>
              5. Theo dõi lưu trữ hàng ngày cho đến khi khắc phục
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Quản lý lưu trữ ngay bây giờ
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🚨 QUOTA LƯU TRỮ ĐÃ TỚI GIỚ HẠN

Hi {{ admin_name }},

KHẨN CẤP: Lưu trữ sao lưu của bạn đang ở mức rất thấp. Các bản sao lưu trong tương lai có thể thất bại nếu không giải phóng không gian lưu trữ.

TRẠNG THÁI LƯU TRỮ:
- Đã dùng: {{ storage_used }} của {{ storage_total }}
- Tỷ lệ sử dụng: {{ storage_percentage }}%
- Còn lại: {{ storage_available }}
- Trạng thái: {{ storage_status }}

CÁC HÀNH ĐỘNG CẦN THỰC HIỆN NGAY:
1. Xóa các bản sao lưu cũ không còn cần thiết
2. Lưu trữ các bản sao lưu vào thiết bị ngoài
3. Tăng dung lượng lưu trữ
4. Xem lại chính sách lưu trữ sao lưu
5. Theo dõi lưu trữ hàng ngày cho đến khi khắc phục

Quản lý lưu trữ ngay bây giờ: {{ admin_backup_url }}