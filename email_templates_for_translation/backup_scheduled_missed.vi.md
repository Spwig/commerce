---
template_type: backup_scheduled_missed
category: Backups
---

# Email Template: backup_scheduled_missed

## Subject
⚠️ Sao lưu định kỳ không chạy - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Sao lưu định kỳ bị bỏ sót
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Chào {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Sao lưu định kỳ cho {{ shop_name }} không chạy như mong đợi. Dữ liệu của bạn có thể chưa được bảo vệ đầy đủ.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Chi tiết lịch sao lưu:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Thời gian đã lên lịch:</strong> {{ scheduled_time }}<br/>
              <strong>Loại sao lưu:</strong> {{ backup_type }}<br/>
              <strong>Lần sao lưu thành công cuối cùng:</strong> {{ last_successful_backup }}<br/>
              <strong>Thời gian kể từ lần sao lưu cuối cùng:</strong> {{ time_since_last }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Nguyên nhân có thể:
        </mj-text>

        <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
          • Máy chủ không hoạt động hoặc không thể truy cập được<br/>
          • Dịch vụ nhiệm vụ định kỳ không chạy<br/>
          • Quyền truy cập không đủ<br/>
          • Không gian lưu trữ đầy<br/>
          • Vấn đề kết nối cơ sở dữ liệu
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Chạy sao lưu thủ công
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ admin_logs_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Xem nhật ký hệ thống
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ SAO LƯU ĐỊNH KỲ BỊ BỎ SÓT

Chào {{ admin_name }},

Sao lưu định kỳ cho {{ shop_name }} không chạy như mong đợi. Dữ liệu của bạn có thể chưa được bảo vệ đầy đủ.

CHI TIẾT LỊCH SAO LƯU:
- Thời gian đã lên lịch: {{ scheduled_time }}
- Loại sao lưu: {{ backup_type }}
- Lần sao lưu thành công cuối cùng: {{ last_successful_backup }}
- Thời gian kể từ lần sao lưu cuối cùng: {{ time_since_last }}

NGUYÊN NHÂN CÓ THỂ:
• Máy chủ không hoạt động hoặc không thể truy cập được
• Dịch vụ nhiệm vụ định kỳ không chạy
• Quyền truy cập không đủ
• Không gian lưu trữ đầy
• Vấn đề kết nối cơ sở dữ liệu

Chạy sao lưu thủ công: {{ admin_backup_url }}
Xem nhật ký hệ thống: {{ admin_logs_url }}