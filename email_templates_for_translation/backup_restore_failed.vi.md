---
template_type: backup_restore_failed
category: Backups
---

# Email Template: backup_restore_failed

## Subject
🚨 KHẨN: Khôi phục sao lưu thất bại - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef2f2">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#dc2626" align="center">
          🚨 KHẨN: Khôi phục sao lưu thất bại
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#1f2937' }}" font-weight="bold">
          Hi {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Một thao tác khôi phục sao lưu quan trọng đã thất bại. Cửa hàng của bạn có thể đang ở trạng thái không nhất quán và cần được xử lý ngay lập tức.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              Chi tiết khôi phục:
            </mj-text>
            <mj-text color="#7f1d1d">
              <strong>Tệp sao lưu:</strong> {{ backup_filename }}<br/>
              <strong>Bắt đầu:</strong> {{ restore_started_at }}<br/>
              <strong>Thất bại:</strong> {{ restore_failed_at }}<br/>
              <strong>Thời lượng:</strong> {{ restore_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Chi tiết lỗi:
        </mj-text>

        <mj-section background-color="#f9fafb" border-radius="4px" padding="15px">
          <mj-column>
            <mj-text font-family="'Courier New', monospace" font-size="13px" color="#dc2626">
              {{ error_message }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="#fef3c7" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#92400e">
              🚨 HÀNH ĐỘNG KHẨN CẤP CẦN THIẾT:
            </mj-text>
            <mj-text color="#92400e">
              1. <strong>ĐỪNG</strong> thay đổi cửa hàng<br/>
              2. Kiểm tra tính kết nối và toàn vẹn cơ sở dữ liệu<br/>
              3. Xem lại nhật ký lỗi để có stack trace chi tiết<br/>
              4. Liên hệ ngay với bộ phận hỗ trợ kỹ thuật<br/>
              5. Xem xét quay lại trạng thái tốt nhất đã biết trước đó
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Xem nhật ký khôi phục
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ support_url }}" background-color="#92400e" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          Liên hệ hỗ trợ khẩn cấp
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🚨 KHẨN: KHÔI PHỤC SAO LƯU THẤT BẠI

Hi {{ admin_name }},

Một thao tác khôi phục sao lưu quan trọng đã thất bại. Cửa hàng của bạn có thể đang ở trạng thái không nhất quán và cần được xử lý ngay lập tức.

CHI TIẾT KHÔI PHỤC:
- Tệp sao lưu: {{ backup_filename }}
- Bắt đầu: {{ restore_started_at }}
- Thất bại: {{ restore_failed_at }}
- Thời lượng: {{ restore_duration }}

CHI TIẾT LỖI:
{{ error_message }}

🚨 HÀNH ĐỘNG KHẨN CẤP CẦN THIẾT:
1. ĐỪNG thay đổi cửa hàng
2. Kiểm tra tính kết nối và toàn vẹn cơ sở dữ liệu
3. Xem lại nhật ký lỗi để có stack trace chi tiết
4. Liên hệ ngay với bộ phận hỗ trợ kỹ thuật
5. Xem xét quay lại trạng thái tốt nhất đã biết trước đó

Xem nhật ký khôi phục: {{ admin_backup_url }}
Liên hệ hỗ trợ khẩn cấp: {{ support_url }}