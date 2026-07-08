---
template_type: affiliate_payout_failed
category: Affiliate Program
---

# Email Template: affiliate_payout_failed

## Subject
Acción requerida: Pago fallido

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
          ⚠️ Pago fallido
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Warning Display -->
    <mj-section background-color="#fff3cd" padding="40px 20px">
      <mj-column>
        <mj-text font-size="48px" font-weight="bold" color="#856404" align="center" line-height="1">
          {{ payout_amount }}
        </mj-text>
        <mj-text font-size="16px" color="#856404" align="center" padding-top="10px">
          ID de pago: {{ payout_id }}
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
          Nos encontramos con un problema al procesar su pago de {{ payout_amount }}.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Esto suele deberse a información de pago incorrecta o un problema con su proveedor de pago.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Por favor, actualice su información de pago en su panel de afiliados y póngase en contacto con nuestro equipo de soporte para resolver este problema.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#dc3545" color="#ffffff" href="{{ portal_url }}">
          Actualizar información de pago
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          ¿Necesita ayuda? <a href="mailto:{{ support_email }}" style="color: #007bff;">Contáctenos</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Acción requerida: Pago fallido

Hola {{ affiliate_name }},

Nos encontramos con un problema al procesar su pago de {{ payout_amount }} (ID de pago: {{ payout_id }}).

Esto suele deberse a información de pago incorrecta o un problema con su proveedor de pago.

Por favor, actualice su información de pago en su panel de afiliados y póngase en contacto con nuestro equipo de soporte para resolver este problema.

Actualizar información de pago: {{ portal_url }}

{{ shop_name }}
¿Necesita ayuda? Contáctenos {{ support_email }}