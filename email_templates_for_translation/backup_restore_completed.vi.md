---
template_type: backup_restore_completed
category: Backups
---

# Email Template: backup_restore_completed

## Subject
✓ Khôi phục sao lưu đã hoàn tất - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#f0fdf4">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#059669" align="center">
          ✓ Khôi phục sao lưu đã hoàn tất
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Chào {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Thao tác khôi phục sao lưu của bạn đã hoàn tất thành công. Dữ liệu cửa hàng của bạn đã được khôi phục.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Chi tiết khôi phục:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Tệp sao lưu:</strong> {{ backup_filename }}<br/>
              <strong>Ngày sao lưu:</strong> {{ backup_date }}<br/>
              <strong>Bắt đầu:</strong> {{ restore_started_at }}<br/>
              <strong>Kết thúc:</strong> {{ restore_completed_at }}<br/>
              <strong>Thời lượng:</strong> {{ restore_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ Các bước quan trọng tiếp theo:
            </mj-text>
            <mj-text font-size="14px" color="#92400e">
              1. Kiểm tra cửa hàng của bạn đang hoạt động đúng cách<br/>
              2. Kiểm tra dữ liệu chính (sản phẩm, đơn hàng, khách hàng)<br/>
              3. Xóa bộ nhớ đệm nếu cần<br/>
              4. Kiểm tra quy trình làm việc quan trọng (thanh toán, truy cập quản trị)
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_dashboard_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Chuyển đến bảng điều khiển quản trị
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ BACKUP RESTORE COMPLETED

Chào {{ admin_name }},

Thao tác khôi phục sao lưu của bạn đã hoàn tất thành công. Dữ liệu cửa hàng của bạn đã được khôi phục.

RESTORE DETAILS:
- Tệp sao lưu: {{ backup_filename }}
- Ngày sao lưu: {{ backup_date }}
- Bắt đầu: {{ restore_started_at }}
- Kết thúc: {{ restore_completed_at }}
- Thời lượng: {{ restore_duration }}

⚠️ IMPORTANT NEXT STEPS:
1. Kiểm tra cửa hàng của bạn đang hoạt động đúng cách
2. Kiểm tra dữ liệu chính (sản phẩm, đơn hàng, khách hàng)
3. Xóa bộ nhớ đệm nếu cần
4. Kiểm tra quy trình làm việc quan trọng (thanh toán, truy cập quản trị)

Go to admin dashboard: {{ admin_dashboard_url }}