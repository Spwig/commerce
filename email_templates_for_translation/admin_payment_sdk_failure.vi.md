---
template_type: admin_payment_sdk_failure
category: Admin Notifications
---

# Email Template: admin_payment_sdk_failure

## Subject
Vấn đề nhà cung cấp thanh toán - SDK {{ provider_name }} không thể tải

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.warning|default:'#f59e0b' }}">
          Vấn đề nhà cung cấp thanh toán
        </mj-text>
        <mj-text>
          SDK thanh toán {{ provider_name }} không thể tải cho khách hàng trong quá trình thanh toán. Điều này có thể cho thấy sự gián đoạn dịch vụ từ nhà cung cấp.
        </mj-text>
        <mj-text>
          <strong>Provider:</strong> {{ provider_name }}
        </mj-text>
        <mj-text>
          <strong>Loại lỗi:</strong> {{ error_type }}
        </mj-text>
        <mj-text>
          <strong>Thời gian:</strong> {{ timestamp }}
        </mj-text>
        <mj-text>
          <strong>Số lần thất bại (trong 1 giờ):</strong> {{ failure_count }}
        </mj-text>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Thông báo này được giới hạn tốc độ, chỉ hiển thị một lần mỗi nhà cung cấp mỗi giờ. Nếu vấn đề vẫn tiếp diễn, vui lòng kiểm tra bảng điều khiển của nhà cung cấp hoặc liên hệ với bộ phận hỗ trợ của họ.
        </mj-text>
        <mj-button href="{{ admin_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          Xem cài đặt thanh toán
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Vấn đề nhà cung cấp thanh toán

SDK thanh toán {{ provider_name }} không thể tải cho khách hàng trong quá trình thanh toán. Điều này có thể cho thấy sự gián đoạn dịch vụ từ nhà cung cấp.

Provider: {{ provider_name }}
Loại lỗi: {{ error_type }}
Thời gian: {{ timestamp }}
Số lần thất bại (trong 1 giờ): {{ failure_count }}

Thông báo này được giới hạn tốc độ, chỉ hiển thị một lần mỗi nhà cung cấp mỗi giờ. Nếu vấn đề vẫn tiếp diễn, vui lòng kiểm tra bảng điều khiển của nhà cung cấp hoặc liên hệ với bộ phận hỗ trợ của họ.

Xem cài đặt thanh toán: {{ admin_url }}