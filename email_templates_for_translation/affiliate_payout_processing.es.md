---
template_type: affiliate_payout_processing
category: Affiliate Program
---

# Email Template: affiliate_payout_processing

## Subject
Se está procesando su pago de {{ payout_amount }}

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
          💸 Procesamiento de pago
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Payout Display -->
    <mj-section background-color="#17a2b8" padding="40px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-bottom="10px">
          Procesando su pago
        </mj-text>
        <mj-text font-size="48px" font-weight="bold" color="#ffffff" align="center" line-height="1">
          {{ payout_amount }}
        </mj-text>
        <mj-text font-size="14px" color="rgba(255, 255, 255, 0.9)" align="center" padding-top="10px">
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
          ¡Buena noticia! Su pago de {{ payout_amount }} ahora está siendo procesado.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Los fondos deberían llegar a su cuenta dentro de 3 a 5 días hábiles. Recibirá otro correo electrónico cuando el pago se complete.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Payout Details -->
    <mj-section background-color="#f8f9fa" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          <strong>ID de pago:</strong> {{ payout_id }}<br/>
          <strong>Cantidad:</strong> {{ payout_amount }}<br/>
          <strong>Método de pago:</strong> {{ payout_method }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          Ver historial de pagos
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          ¿Tiene preguntas? <a href="mailto:{{ support_email }}" style="color: #007bff;">Contactar soporte</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Se está procesando su pago de {{ payout_amount }}

Hola {{ affiliate_name }},

¡Buena noticia! Su pago de {{ payout_amount }} ahora está siendo procesado.

Detalles del pago:
- ID de pago: {{ payout_id }}
- Cantidad: {{ payout_amount }}
- Método de pago: {{ payout_method }}

Los fondos deberían llegar a su cuenta dentro de 3 a 5 días hábiles. Recibirá otro correo electrónico cuando el pago se complete.

Ver historial de pagos: {{ portal_url }}

{{ shop_name }}
¿Tiene preguntas? Contactar {{ support_email }}