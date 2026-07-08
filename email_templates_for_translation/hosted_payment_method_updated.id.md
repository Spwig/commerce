---
template_type: hosted_payment_method_updated
category: License
---

# Email Template: hosted_payment_method_updated

## Subject
Metode Pembayaran Diperbarui - {{ store_name }}

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
    <mj-section background-color="#16a34a" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Metode Pembayaran Diperbarui
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
          Hi there,
        </mj-text>
        <mj-text>
          Metode pembayaran untuk rencana <strong>{{ plan_name }}</strong> Anda di <strong>{{ store_name }}</strong> telah berhasil diperbarui.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Security Notice -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Tidak Melakukan Perubahan Ini?
        </mj-text>
        <mj-text font-size="14px">
          Jika Anda tidak memperbarui metode pembayaran Anda, silakan hubungi tim dukungan kami segera agar kami dapat memastikan keamanan akun Anda.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Go to Your Store" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Metode Pembayaran Diperbarui - {{ store_name }}

Hi there,

Metode pembayaran untuk rencana {{ plan_name }} Anda di {{ store_name }} telah berhasil diperbarui.

Tidak Melakukan Perubahan Ini?
Jika Anda tidak memperbarui metode pembayaran Anda, silakan hubungi tim dukungan kami segera agar kami dapat memastikan keamanan akun Anda.

Go to Your Store: {{ admin_url }}

Need help? Contact {{ support_email }}