---
template_type: hosted_suspension_warning
category: License
---

# Email Template: hosted_suspension_warning

## Subject
Cảnh báo tạm dừng - {{ store_name }}

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
    <mj-section background-color="#ea580c" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Cảnh báo tạm dừng
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Hành động cần thực hiện cho {{ store_name }}
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
          Giao dịch thanh toán cho <strong>{{ plan_name }}</strong> đã quá hạn. Nếu không được giải quyết trước <strong>{{ grace_end_date }}</strong>, cửa hàng của bạn sẽ bị chuyển sang chế độ chỉ đọc.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What Suspension Means -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Ý nghĩa của việc tạm dừng
        </mj-text>
        <mj-text font-size="14px">
          Nếu cửa hàng của bạn bị tạm dừng, nó vẫn sẽ hiển thị với khách truy cập nhưng bạn sẽ không thể thực hiện bất kỳ thay đổi nào. Các đơn hàng mới sẽ bị tạm dừng cho đến khi khoản nợ còn lại được thanh toán.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Resolve -->
    <mj-section>
      <mj-column>
        <mj-text>
          Vui lòng cập nhật phương thức thanh toán của bạn để tránh gián đoạn cho cửa hàng.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="Cập nhật phương thức thanh toán" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Cảnh báo tạm dừng - {{ store_name }}

Chào {{ name|default:'there' }},

Giao dịch thanh toán cho {{ plan_name }} đã quá hạn. Nếu không được giải quyết trước {{ grace_end_date }}, cửa hàng của bạn sẽ bị chuyển sang chế độ chỉ đọc.

Ý nghĩa của việc tạm dừng:
Nếu cửa hàng của bạn bị tạm dừng, nó vẫn sẽ hiển thị với khách truy cập nhưng bạn sẽ không thể thực hiện bất kỳ thay đổi nào. Các đơn hàng mới sẽ bị tạm dừng cho đến khi khoản nợ còn lại được thanh toán.

Vui lòng cập nhật phương thức thanh toán của bạn để tránh gián đoạn cho cửa hàng.

Cập nhật phương thức thanh toán: https://spwig.com/account

Cần hỗ trợ? Liên hệ {{ support_email }}