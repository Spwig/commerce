---
template_type: affiliate_account_suspended
category: Affiliate Program
---

# Email Template: affiliate_account_suspended

## Subject
Importante: Cuenta suspendida

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="#f8f9fa">
    <!-- Header -->
    <mj-section background-color="#ffffff" padding="40px 20px">
      <mj-column>
        <mj-text font-size="32px" font-weight="bold" color="#dc3545" align="center">
          Cuenta suspendida
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          Hola {{ affiliate_name }},
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Su cuenta de afiliado con {{ shop_name }} ha sido suspendida.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Esto suele deberse a una violación de los términos y condiciones del programa de afiliados.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Si cree que esto es un error o desea discutir esta decisión, por favor póngase en contacto con nuestro equipo de soporte.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          ¿Preguntas? <a href="mailto:{{ support_email }}" style="color: #007bff;">Contactar soporte</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Importante: Cuenta suspendida

Hola {{ affiliate_name }},

Su cuenta de afiliado con {{ shop_name }} ha sido suspendida.

Esto suele deberse a una violación de los términos y condiciones del programa de afiliados.

Si cree que esto es un error o desea discutir esta decisión, por favor póngase en contacto con nuestro equipo de soporte.

{{ shop_name }}
¿Preguntas? Contactar {{ support_email }}