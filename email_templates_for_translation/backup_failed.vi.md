---
template_type: backup_failed
category: Backups
---

# Email Template: backup_failed

## Subject
🚨 KHẨN: Sao lưu thất bại - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef2f2">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#dc2626" align="center">
          ⚠️ Sao lưu thất bại
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#1f2937' }}">
          Chào {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Một hoạt động sao lưu quan trọng đã thất bại cho cửa hàng {{ shop_name }} của bạn. Hành động ngay lập tức là cần thiết để đảm bảo bảo vệ dữ liệu.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              Chi tiết sao lưu:
            </mj-text>
            <mj-text color="#7f1d1d">
              <strong>Loại sao lưu:</strong> {{ backup_type }}<br/>
              <strong>Bắt đầu:</strong> {{ backup_started_at }}<br/>
              <strong>Thất bại:</strong> {{ backup_failed_at }}<br/>
              <strong>Thời lượng:</strong> {{ backup_duration }}
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

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Các hành động được đề xuất:
        </mj-text>

        <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
          1. Kiểm tra không gian đĩa khả dụng trên máy chủ của bạn<br/>
          2. Kiểm tra kết nối cơ sở dữ liệu<br/>
          3. Xem xét nhật ký lỗi để có stack trace chi tiết<br/>
          4. Thử sao lưu lại thủ công hoặc chờ lần chạy kế tiếp<br/>
          5. Liên hệ hỗ trợ nếu vấn đề vẫn tồn tại
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Xem nhật ký sao lưu
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ retry_backup_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          Thử sao lưu lại ngay
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>Lần sao lưu thành công cuối cùng:</strong> {{ last_successful_backup }}<br/>
          <strong>Lần sao lưu kế tiếp dự kiến:</strong> {{ next_scheduled_backup }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🚨 KHẨN: SAO LƯU THẤT BẠI

Chào {{ admin_name }},

Một hoạt động sao lưu quan trọng đã thất bại cho cửa hàng {{ shop_name }} của bạn. Hành động ngay lập tức là cần thiết để đảm bảo bảo vệ dữ liệu.

CHI TIẾT SAO LƯU:
- Loại sao lưu: {{ backup_type }}
- Bắt đầu: {{ backup_started_at }}
- Thất bại: {{ backup_failed_at }}
- Thời lượng: {{ backup_duration }}

CHI TIẾT LỖI:
{{ error_message }}

CÁC HÀNH ĐỘNG ĐƯỢC ĐỀ XUẤT:
1. Kiểm tra không gian đĩa khả dụng trên máy chủ của bạn
2. Kiểm tra kết nối cơ sở dữ liệu
3. Xem xét nhật ký lỗi để có stack trace chi tiết
4. Thử sao lưu lại thủ công hoặc chờ lần chạy kế tiếp
5. Liên hệ hỗ trợ nếu vấn đề vẫn tồn tại

Xem nhật ký sao lưu: {{ admin_backup_url }}
Thử sao lưu lại ngay: {{ retry_backup_url }}

Lần sao lưu thành công cuối cùng: {{ last_successful_backup }}
Lần sao lưu kế tiếp dự kiến: {{ next_scheduled_backup }}

---
Đây là một cảnh báo hệ thống quan trọng dành cho các quản trị viên {{ shop_name }}.