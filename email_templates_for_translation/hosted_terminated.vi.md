---
template_type: hosted_terminated
category: License
---

# Email Template: hosted_terminated

## Subject
Cửa hàng đã bị xóa - {{ store_name }}

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
    <mj-section background-color="#374151" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Store Removed
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
          Hi {{ name|default:'there' }},
        </mj-text>
        <mj-text>
          Your store <strong>{{ store_name }}</strong> has been permanently removed.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Data Backup Info -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Data Backup
        </mj-text>
        <mj-text font-size="14px">
          A backup of your data will be available for 90 days upon request. Contact <strong>support@spwig.com</strong> if you need a data export.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Thank You -->
    <mj-section>
      <mj-column>
        <mj-text>
          Thank you for being a Spwig customer. We hope to see you again in the future.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Cửa hàng đã bị xóa - {{ store_name }}

Hi {{ name|default:'there' }},

Cửa hàng {{ store_name }} đã bị xóa vĩnh viễn.

Dữ liệu lưu trữ:
Một bản sao lưu dữ liệu của bạn sẽ có sẵn trong 90 ngày nếu bạn yêu cầu. Liên hệ với <strong>support@spwig.com</strong> nếu bạn cần xuất dữ liệu.

Cảm ơn bạn đã là khách hàng của Spwig. Chúng tôi hy vọng sẽ được phục vụ bạn một lần nữa trong tương lai.

Cần hỗ trợ? Liên hệ {{ support_email }}