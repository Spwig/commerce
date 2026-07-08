---
template_type: subscription_dunning_final_notice
category: Subscriptions
---

# Email Template: subscription_dunning_final_notice

## Subject
⚠️ THÔNG BÁO CUỐI CÙNG: Gói đăng ký của bạn sẽ bị hủy trong {{ days_until_cancellation }} ngày

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#991b1b" align="center">
          ⚠️ THÔNG BÁO CUỐI CÙNG
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Gói Đăng Ký Sắp Bị Hủy
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Đây là thông báo cuối cùng của bạn. Chúng tôi không thể xử lý thanh toán cho gói đăng ký {{ plan_name }} của bạn. Nếu không nhận được thanh toán trong {{ days_until_cancellation }} ngày, gói đăng ký của bạn sẽ bị hủy.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b" font-size="16px">
              ⚠️ Thanh Toán Thất Bại - Hành Động Yêu Cầu
            </mj-text>
            <mj-text color="#991b1b">
              <strong>Gói Đăng Ký:</strong> {{ plan_name }}<br/>
              <strong>Số Tiền Cần Trả:</strong> {{ amount_due }}<br/>
              <strong>Lần Thanh Toán Thất Bại:</strong> {{ retry_count }}<br/>
              <strong>Lần Thanh Toán Cuối Cùng:</strong> {{ last_retry_date }}<br/>
              <strong>Ngày Hủy Gói:</strong> <span style="font-weight: bold; font-size: 16px;">{{ cancellation_date }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Lỗi Thanh Toán:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" font-family="monospace" color="{{ theme.color.text|default:'#4b5563' }}">
              {{ payment_error_message }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Điều Gì Sẽ Xảy Ra:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          Nếu không nhận được thanh toán trước {{ cancellation_date }}:<br/>
          • Gói đăng ký của bạn sẽ bị hủy<br/>
          • Bạn sẽ mất quyền truy cập tất cả các lợi ích từ gói đăng ký<br/>
          • Dữ liệu của bạn có thể bị xóa (xem chính sách lưu giữ)<br/>
          • Bạn sẽ cần đăng ký lại để khôi phục quyền truy cập
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          Cập Nhật Phương Thức Thanh Toán Ngay Lập Tức
        </mj-text>

        <mj-spacer height="20px" />

        <mj-button href="{{ update_payment_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Cập Nhật Phương Thức Thanh Toán
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Các Vấn Đề Thường Gặp & Giải Pháp:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • <strong>Thẻ hết hạn:</strong> Cập nhật với thẻ tín dụng hiện tại<br/>
          • <strong>Tài khoản không đủ tiền:</strong> Đảm bảo số dư đủ<br/>
          • <strong>Thẻ bị từ chối:</strong> Liên hệ ngân hàng của bạn hoặc sử dụng thẻ khác<br/>
          • <strong>Địa chỉ không khớp:</strong> Kiểm tra địa chỉ thanh toán khớp với thẻ
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" font-weight="bold">
              Cần Hỗ Trợ?
            </mj-text>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              Nếu bạn đang gặp vấn đề thanh toán hoặc cần hỗ trợ, vui lòng liên hệ ngay với nhóm hỗ trợ của chúng tôi.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Liên Hệ Hỗ Trợ
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Nếu bạn muốn hủy gói đăng ký, bạn có thể thực hiện điều này trong cài đặt tài khoản của mình.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ THÔNG BÁO CUỐI CÙNG

Gói Đăng Ký Sắp Bị Hủy

Hi {{ customer_name }},

Đây là thông báo cuối cùng của bạn. Chúng tôi không thể xử lý thanh toán cho gói đăng ký {{ plan_name }} của bạn. Nếu không nhận được thanh toán trong {{ days_until_cancellation }} ngày, gói đăng ký của bạn sẽ bị hủy.

⚠️ THANH TOÁN THẤT BẠI - HÀNH ĐỘNG YÊU CẦU:
- Gói Đăng Ký: {{ plan_name }}
- Số Tiền Cần Trả: {{ amount_due }}
- Lần Thanh Toán Thất Bại: {{ retry_count }}
- Lần Thanh Toán Cuối Cùng: {{ last_retry_date }}
- Ngày Hủy Gói: {{ cancellation_date }}

LỖI THANH TOÁN:
{{ payment_error_message }}

ĐIỀU GÌ SẼ XẢY RA:
Nếu không nhận được thanh toán trước {{ cancellation_date }}:
• Gói đăng ký của bạn sẽ bị hủy
• Bạn sẽ mất quyền truy cập tất cả các lợi ích từ gói đăng ký
• Dữ liệu của bạn có thể bị xóa (xem chính sách lưu giữ)
• Bạn sẽ cần đăng ký lại để khôi phục quyền truy cập

CẬP NHẬT PHƯƠNG THỨC THANH TOÁN NGAY LẬP TỨC

Các Vấn Đề Thường Gặp & Giải Pháp:
• Thẻ hết hạn: Cập nhật với thẻ tín dụng hiện tại
• Tài khoản không đủ tiền: Đảm bảo số dư đủ
• Thẻ bị từ chối: Liên hệ ngân hàng của bạn hoặc sử dụng thẻ khác
• Địa chỉ không khớp: Kiểm tra địa chỉ thanh toán khớp với thẻ

CẦN HỖ TRỢ?
Nếu bạn đang gặp vấn đề thanh toán hoặc cần hỗ trợ, vui lòng liên hệ ngay với nhóm hỗ trợ của chúng tôi.

Cập nhật phương thức thanh toán: {{ update_payment_url }}
Liên hệ hỗ trợ: {{ support_url }}

Nếu bạn muốn hủy gói đăng ký, bạn có thể thực hiện điều này trong cài đặt tài khoản của mình.