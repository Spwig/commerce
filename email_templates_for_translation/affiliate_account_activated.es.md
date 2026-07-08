---
template_type: affiliate_account_activated
category: Affiliate Program
---

# Email Template: affiliate_account_activated

## Subject
¡Bienvenido de nuevo! Cuenta reactivada

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
        <mj-text font-size="32px" font-weight="bold" color="#212529" align="center">
          🎉 Cuenta Reactivada!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Success Banner -->
    <mj-section background-color="#28a745" padding="40px 20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#ffffff" align="center">
          ¡Bienvenido de nuevo!
        </mj-text>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-top="10px">
          Su cuenta de afiliado está activa de nuevo
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
          ¡Buena noticia! Su cuenta de afiliado con {{ shop_name }} ha sido reactivada.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Puede reanudar la promoción de nuestros productos y ganar comisiones de inmediato.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          Acceder al Panel de Afiliados
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          ¿Preguntas? <a href="mailto:{{ support_email }}" style="color: #007bff;">
          Contactar al Soporte</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
¡Bienvenido de nuevo! Cuenta reactivada

Hola {{ affiliate_name }},

¡Buena noticia! Su cuenta de afiliado con {{ shop_name }} ha sido reactivada.

Puede reanudar la promoción de nuestros productos y ganar comisiones de inmediato.

Acceder al panel de afiliados: {{ portal_url }}

{{ shop_name }}
¿Preguntas? Contactar a {{ support_email }}