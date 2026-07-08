---
template_type: blog_subscription_confirmed
category: Blog
---

# Email Template: blog_subscription_confirmed

## Subject
Xác nhận đăng ký của bạn cho {{ blog_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Xác nhận Đăng ký của bạn
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Chào {{ subscriber_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Cảm ơn bạn đã đăng ký vào {{ blog_name }}! Để hoàn tất việc đăng ký và bắt đầu nhận các bản cập nhật, vui lòng xác nhận địa chỉ email của bạn.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ confirmation_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          Xác nhận Đăng ký
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              Không thể nhấp vào nút? Sao chép và dán liên kết này vào trình duyệt của bạn:<br/>
              <span style="color: {{ theme.color.primary|default:'#2563eb' }}; font-family: 'Courier New', monospace;">{{ confirmation_url }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>Tại sao cần xác nhận?</strong><br/>
          Việc xác nhận email giúp chúng tôi đảm bảo bạn muốn nhận các bản cập nhật và ngăn chặn spam. Quyền riêng tư và hộp thư đến của bạn rất quan trọng đối với chúng tôi.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Không đăng ký? Bạn có thể an toàn bỏ qua email này.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
XÁC NHẬN ĐĂNG KÝ

Chào {{ subscriber_name }},

Cảm ơn bạn đã đăng ký vào {{ blog_name }}! Để hoàn tất việc đăng ký và bắt đầu nhận các bản cập nhật, vui lòng xác nhận địa chỉ email của bạn.

Xác nhận đăng ký: {{ confirmation_url }}

TẠI SAO CẦN XÁC NHẬN?
Việc xác nhận email giúp chúng tôi đảm bảo bạn muốn nhận các bản cập nhật và ngăn chặn spam. Quyền riêng tư và hộp thư đến của bạn rất quan trọng đối với chúng tôi.

Không đăng ký? Bạn có thể an toàn bỏ qua email này.