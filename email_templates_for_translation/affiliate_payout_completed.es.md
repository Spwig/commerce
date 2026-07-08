---
template_type: affiliate_payout_completed
category: Affiliate Program
---

# Email Template: affiliate_payout_completed

## Subject
✓ Pago completado: {{ payout_amount }}

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
          🎉 Pago Completado!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Payout Display -->
    <mj-section background-color="#28a745" padding="40px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-bottom="10px">
          ✓ Pago Exitoso
        </mj-text>
        <mj-text font-size="48px" font-weight="bold" color="#ffffff" align="center" line-height="1">
          {{ payout_amount }}
        </mj-text>
        <mj-text font-size="14px" color="rgba(255, 255, 255, 0.9)" align="center" padding-top="10px">
          ID del Pago: {{ payout_id }}
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
          ¡Tu pago de {{ payout_amount }} se ha completado con éxito!
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Los fondos se han enviado a tu método de pago. Dependiendo de tu banco o procesador de pagos, puede tomar 1-2 días hábiles para aparecer en tu cuenta.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          ¡Gracias por promocionar {{ shop_name }}. ¡Sigue así!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          Ver detalles del pago
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          ¿Tiene preguntas? <a href="mailto:{{ support_email }}" style="color: #007bff;">Contáctenos</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ Pago completado: {{ payout_amount }}

Hola {{ affiliate_name }},

¡Tu pago de {{ payout_amount }} se ha completado con éxito!

Detalles del pago:
- ID del pago: {{ payout_id }}
- Monto: {{ payout_amount }}
- Método de pago: {{ payout_method }}

Los fondos se han enviado a tu método de pago. Dependiendo de tu banco o procesador de pagos, puede tomar 1-2 días hábiles para aparecer en tu cuenta.

¡Gracias por promocionar {{ shop_name }}. ¡Sigue así!

Ver detalles del pago: {{ portal_url }}

{{ shop_name }}
¿Tiene preguntas? Contáctenos a {{ support_email }}