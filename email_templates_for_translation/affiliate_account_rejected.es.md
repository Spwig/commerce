---
template_type: affiliate_account_rejected
category: Affiliate Program
---

# Email Template: affiliate_account_rejected

## Subject
Actualización de la solicitud de afiliado

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
          Actualización de la solicitud
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
          Gracias por tu interés en unirte al programa de afiliados de {{ shop_name }}.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Después de revisar tu solicitud, hemos decidido no continuar en este momento.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Esta decisión se basa en los requisitos actuales del programa de afiliados y puede no reflejar tus cualificaciones o potencial.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Estás invitado a re aplicar en el futuro si tus circunstancias cambian.
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
Actualización de la solicitud de afiliado

Hola {{ affiliate_name }},

Gracias por tu interés en unirte al programa de afiliados de {{ shop_name }}.

Después de revisar tu solicitud, hemos decidido no continuar en este momento.

Esta decisión se basa en los requisitos actuales del programa de afiliados y puede no reflejar tus cualificaciones o potencial.

Estás invitado a re aplicar en el futuro si tus circunstancias cambian.

{{ shop_name }}
¿Preguntas? Contactar {{ support_email }}}