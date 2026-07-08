---
template_type: affiliate_commission_earned
category: Affiliate Program
---

# Email Template: affiliate_commission_earned

## Subject
¡Ganaste una comisión de {{ commission_amount }}!

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
          💰 ¡Comisión Ganada!
        </mj-text>
        <mj-text font-size="18px" color="#6c757d" align="center">
          ¡Buena noticia desde {{ shop_name }}!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Commission Display -->
    <mj-section background-color="#28a745" padding="40px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-bottom="10px">
          💵 Tu Comisión
        </mj-text>
        <mj-text font-size="48px" font-weight="bold" color="#ffffff" align="center" line-height="1">
          {{ commission_amount }}
        </mj-text>
        <mj-text font-size="14px" color="rgba(255, 255, 255, 0.9)" align="center" padding-top="10px">
          Desde el pedido #{{ order_number }}
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
          ¡Felicidades! Ganaste una comisión de {{ commission_amount }} desde el pedido #{{ order_number }}.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          ¡Sigue promocionando {{ shop_name }} para ganar más comisiones! Cuantas más ventas generes, más ganarás.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Commission Details -->
    <mj-section background-color="#f8f9fa" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          <strong>Número de pedido:</strong> #{{ order_number }}<br/>
          <strong>Cantidad de comisión:</strong> {{ commission_amount }}<br/>
          <strong>Tasa de comisión:</strong> {{ commission_rate }}%
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          Ver Panel de Afiliado
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          ¿Tienes preguntas? <a href="mailto:{{ support_email }}" style="color: #007bff;">Contactar Soporte</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
¡Ganaste una comisión de {{ commission_amount }}!

Hola {{ affiliate_name }},

¡Felicidades! Ganaste una comisión de {{ commission_amount }} desde el pedido #{{ order_number }}.

Detalles de la comisión:
- Número de pedido: #{{ order_number }}
- Cantidad de comisión: {{ commission_amount }}
- Tasa de comisión: {{ commission_rate }}%

¡Sigue promocionando {{ shop_name }} para ganar más comisiones!

Ver tu panel: {{ portal_url }}

{{ shop_name }}
¿Tienes preguntas? Contacta a {{ support_email }}