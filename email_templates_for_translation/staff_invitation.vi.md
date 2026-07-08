---
template_type: staff_invitation
category: Core E-commerce
---

# Email Template: staff_invitation

## Subject
Bạn đã được mời tham gia {{ store_name }}

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
    <mj-section background-color="{{ theme.color.primary|default:'#2563eb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Mời tham gia nhân viên
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Bạn đã được mời tham gia {{ store_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Chào {{ first_name }},
        </mj-text>
        <mj-text>
          {{ invited_by }} đã mời bạn tham gia {{ store_name }} với vai trò là nhân viên. Bạn sẽ có thể giúp quản lý cửa hàng từ bảng điều khiển quản trị.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Button -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=invitation_url text="Chấp nhận lời mời" %}

    <!-- Expiry Note -->
    <mj-section>
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Lời mời này sẽ hết hạn vào {{ expires_at|date:"N j, Y" }}. Nếu bạn không mong đợi lời mời này, bạn có thể an toàn bỏ qua email này.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Bạn đã được mời tham gia {{ store_name }}

Chào {{ first_name }},

{{ invited_by }} đã mời bạn tham gia {{ store_name }} với vai trò là nhân viên. Bạn sẽ có thể giúp quản lý cửa hàng từ bảng điều khiển quản trị.

Chấp nhận lời mời: {{ invitation_url }}

Lời mời này sẽ hết hạn vào {{ expires_at|date:"N j, Y" }}. Nếu bạn không mong đợi lời mời này, bạn có thể an toàn bỏ qua email này.

Cần hỗ trợ? Liên hệ {{ support_email }}