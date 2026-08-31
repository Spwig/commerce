---
template_type: newsletter_signup_confirm
category: Newsletter
---

# Email Template: newsletter_signup_confirm

## Subject
Vui lòng xác nhận đăng ký của bạn tại {{ store_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Xác nhận đăng ký của bạn
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Cảm ơn bạn đã đăng ký để nhận thông tin từ {{ store_name }}! Vui lòng xác nhận địa chỉ email của bạn để bắt đầu nhận các bản cập nhật và ưu đãi từ chúng tôi.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ confirmation_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          Xác nhận đăng ký
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              Không thể nhấp vào nút? Hãy sao chép và dán liên kết này vào trình duyệt của bạn:<br/>
              <span style="color: {{ theme.color.primary|default:'#2563eb' }}; font-family: 'Courier New', monospace;">{{ confirmation_url }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>Tại sao cần xác nhận?</strong><br/>
          Việc xác nhận email giúp chúng tôi đảm bảo rằng bạn thực sự muốn nhận các bản cập nhật và giữ cho hộp thư của bạn không bị thư rác.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Bạn không đăng ký? Bạn có thể an toàn bỏ qua email này.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Xác nhận đăng ký của bạn tại {{ store_name }}

Cảm ơn bạn đã đăng ký để nhận thông tin từ {{ store_name }}! Vui lòng xác nhận địa chỉ email của bạn để bắt đầu nhận các bản cập nhật và ưu đãi từ chúng tôi:

{{ confirmation_url }}

Việc xác nhận email giúp chúng tôi đảm bảo rằng bạn thực sự muốn nhận các bản cập nhật và giữ cho hộp thư của bạn không bị thư rác.

Bạn không đăng ký? Bạn có thể an toàn bỏ qua email này.