---
template_type: hosted_provision_failed
category: License
---

# Email Template: hosted_provision_failed

## Subject
Hành động cần thiết - Lỗi thiết lập cửa hàng cho {{ store_name }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.error|default:'#dc2626' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Lỗi thiết lập cửa hàng
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Chào {{ name|default:'there' }},
        </mj-text>
        <mj-text>
          Chúng tôi đã gặp phải một vấn đề khi thiết lập cửa hàng của bạn <strong>{{ store_name }}</strong>. Đội ngũ của chúng tôi đã được thông báo và đang xử lý vấn đề này.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Error Details -->
    <mj-section background-color="#fef2f2" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="14px" font-weight="bold" color="#991b1b" padding-bottom="10px">
          Điều gì đã xảy ra
        </mj-text>
        <mj-text font-size="14px" color="#7f1d1d">
          {{ provision_error }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What's Next -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Điều gì sẽ xảy ra tiếp theo?
        </mj-text>
        <mj-text font-size="14px">
          Đội ngũ hỗ trợ của chúng tôi đã được thông báo tự động về vấn đề này. Bạn không cần thực hiện bất kỳ hành động nào - chúng tôi sẽ liên hệ với bạn khi vấn đề được giải quyết.
        </mj-text>
        <mj-text font-size="14px" padding-top="10px">
          Nếu bạn có bất kỳ câu hỏi nào trong thời gian chờ đợi, vui lòng không ngần ngại liên hệ với chúng tôi.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Lỗi thiết lập cửa hàng - {{ store_name }}

Chào {{ name|default:'there' }},

Chúng tôi đã gặp phải một vấn đề khi thiết lập cửa hàng {{ store_name }}. Đội ngũ của chúng tôi đã được thông báo và đang xử lý vấn đề này.

Điều gì đã xảy ra:
{{ provision_error }}

Điều gì sẽ xảy ra tiếp theo?
Đội ngũ hỗ trợ của chúng tôi đã được thông báo tự động về vấn đề này. Bạn không cần thực hiện bất kỳ hành động nào - chúng tôi sẽ liên hệ với bạn khi vấn đề được giải quyết.

Nếu bạn có bất kỳ câu hỏi nào trong thời gian chờ đợi, vui lòng không ngần ngại liên hệ với chúng tôi.

Cần hỗ trợ? Liên hệ {{ support_email }}