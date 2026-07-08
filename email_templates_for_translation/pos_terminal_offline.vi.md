---
template_type: pos_terminal_offline
category: POS
---

# Email Template: pos_terminal_offline

## Subject
⚠️ Thiết bị đầu cuối POS ngoại tuyến: {{ terminal_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#991b1b" align="center">
          ⚠️ Thiết bị đầu cuối bị ngắt kết nối
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Thiết bị đầu cuối POS ngoại tuyến
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ terminal_name }} đã ngoại tuyến và không còn phản hồi.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Thông tin thiết bị đầu cuối:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Thiết bị đầu cuối:</strong> {{ terminal_name }}<br/>
              <strong>Vị trí:</strong> {{ location }}<br/>
              <strong>Lần cuối thấy:</strong> {{ last_seen }}<br/>
              <strong>Ngoại tuyến từ:</strong> {{ offline_since }}<br/>
              <strong>Thời lượng:</strong> {{ offline_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Nguyên nhân thường gặp:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • Vấn đề kết nối mạng<br/>
          • Thiết bị đầu cuối bị tắt hoặc khởi động lại<br/>
          • Lỗi phần mềm hoặc bị treo<br/>
          • Sự cố dịch vụ internet
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Các hành động được khuyến nghị:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Kiểm tra nguồn điện và kết nối mạng của thiết bị đầu cuối<br/>
          2. Khởi động lại thiết bị đầu cuối<br/>
          3. Kiểm tra kết nối internet<br/>
          4. Kiểm tra tường lửa và cài đặt bảo mật
        </mj-text>

        {% if active_shift %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ Cảnh báo ca làm việc đang hoạt động
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              Thiết bị đầu cuối này có ca làm việc đang hoạt động. Dữ liệu bán hàng có thể không được đồng bộ hóa cho đến khi được nối lại.
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_terminals_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Xem trạng thái thiết bị đầu cuối
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Bạn sẽ nhận được thông báo khác khi thiết bị đầu cuối được nối lại.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ THIẾT BỊ ĐẦU CUỐI BỊ NGẮT KẾT NỐI

Thiết bị đầu cuối POS ngoại tuyến

{{ terminal_name }} đã ngoại tuyến và không còn phản hồi.

THÔNG TIN THIẾT BỊ ĐẦU CUỐI:
- Thiết bị đầu cuối: {{ terminal_name }}
- Vị trí: {{ location }}
- Lần cuối thấy: {{ last_seen }}
- Ngoại tuyến từ: {{ offline_since }}
- Thời lượng: {{ offline_duration }}

NGUYÊN NHÂN THƯỜNG GẶP:
• Vấn đề kết nối mạng
• Thiết bị đầu cuối bị tắt hoặc khởi động lại
• Lỗi phần mềm hoặc bị treo
• Sự cố dịch vụ internet

CÁC HÀNH ĐỘNG ĐƯỢC KHUYẾN NGHỊ:
1. Kiểm tra nguồn điện và kết nối mạng của thiết bị đầu cuối
2. Khởi động lại thiết bị đầu cuối
3. Kiểm tra kết nối internet
4. Kiểm tra tường lửa và cài đặt bảo mật

{% if active_shift %}
⚠️ CẢNH BÁO CA LÀM VIỆC ĐANG HOẠT ĐỘNG:
Thiết bị đầu cuối này có ca làm việc đang hoạt động. Dữ liệu bán hàng có thể không được đồng bộ hóa cho đến khi được nối lại.
{% endif %}

Xem trạng thái thiết bị đầu cuối: {{ admin_terminals_url }}

Bạn sẽ nhận được thông báo khác khi thiết bị đầu cuối được nối lại.