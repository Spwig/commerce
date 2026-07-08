---
template_type: hosted_termination_warning
category: License
---

# Email Template: hosted_termination_warning

## Subject
Quan trọng: Xóa dữ liệu trong 7 ngày - {{ store_name }}

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
    <mj-section background-color="#dc2626" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Cảnh báo xóa dữ liệu
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
          Cửa hàng của bạn <strong>{{ store_name }}</strong> và tất cả dữ liệu liên quan sẽ bị xóa vĩnh viễn vào <strong>{{ termination_date }}</strong>. Hành động này không thể hoàn tác.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What You Can Do -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Điều bạn có thể làm
        </mj-text>
        <mj-text font-size="14px">
          Nếu bạn muốn giữ lại dữ liệu, vui lòng xuất dữ liệu trước ngày này hoặc kích hoạt lại đăng ký của bạn để ngăn việc xóa.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="Reactivate Subscription" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Cảnh báo xóa dữ liệu - {{ store_name }}

Chào {{ name|default:'there' }},

Cửa hàng của bạn {{ store_name }} và tất cả dữ liệu liên quan sẽ bị xóa vĩnh viễn vào {{ termination_date }}. Hành động này không thể hoàn tác.

Điều bạn có thể làm:
Nếu bạn muốn giữ lại dữ liệu, vui lòng xuất dữ liệu trước ngày này hoặc kích hoạt lại đăng ký của bạn để ngăn việc xóa.

Kích hoạt lại đăng ký: https://spwig.com/account

Cần hỗ trợ? Liên hệ {{ support_email }}