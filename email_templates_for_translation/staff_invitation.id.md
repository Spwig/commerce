---
template_type: staff_invitation
category: Core E-commerce
---

# Email Template: staff_invitation

## Subject
Anda Telah Diundang untuk Bergabung dengan {{ store_name }}

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
          Undangan untuk Staf
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Anda telah diundang untuk bergabung dengan {{ store_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Hai {{ first_name }},
        </mj-text>
        <mj-text>
          {{ invited_by }} telah mengundang Anda untuk bergabung dengan <strong>{{ store_name }}</strong> sebagai staf. Anda akan dapat membantu mengelola toko dari dashboard admin.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Button -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=invitation_url text="Terima Undangan" %}

    <!-- Expiry Note -->
    <mj-section>
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Undangan ini akan kedaluwarsa pada {{ expires_at|date:"N j, Y" }}. Jika Anda tidak mengharapkan undangan ini, Anda dapat dengan aman mengabaikan email ini.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Anda Telah Diundang untuk Bergabung dengan {{ store_name }}

Hai {{ first_name }},

{{ invited_by }} telah mengundang Anda untuk bergabung dengan {{ store_name }} sebagai staf. Anda akan dapat membantu mengelola toko dari dashboard admin.

Terima undangan: {{ invitation_url }}

Undangan ini akan kedaluwarsa pada {{ expires_at|date:"N j, Y" }}. Jika Anda tidak mengharapkan undangan ini, Anda dapat dengan aman mengabaikan email ini.

Butuh bantuan? Hubungi {{ support_email }}