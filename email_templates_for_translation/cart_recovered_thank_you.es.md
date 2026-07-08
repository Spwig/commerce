---
template_type: cart_recovered_thank_you
category: Cart Recovery
---

# Email Template: cart_recovered_thank_you

## Subject
¡Gracias por tu pedido #{{ order_number }}! - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          🎉 ¡Gracias por tu pedido!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hola {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Estamos encantados de que hayas completado tu compra. Tu pedido ha sido confirmado y lo estamos preparando para el envío.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Resumen del Pedido
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Número de Pedido:</strong> {{ order_number }}<br/>
              <strong>Fecha del Pedido:</strong> {{ order_date }}<br/>
              <strong>Total:</strong> {{ order_total }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ order_tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Rastrear tu Pedido
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ¿Qué sucede a continuación?
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Prepararemos tu pedido (normalmente dentro de 1-2 días hábiles)<br/>
          2. Recibirás una confirmación de envío con información de seguimiento<br/>
          3. Tu pedido se entregará a: {{ shipping_address }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              💡 <strong>¿Sabías que?</strong><br/>
              Puedes rastrear tu pedido en cualquier momento en tu panel de control de cuenta.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          ¿Tienes preguntas? <a href="{{ support_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Contáctanos</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎉 ¡GRACIAS POR TU PEDIDO!

Hola {{ customer_name }},

Estamos encantados de que hayas completado tu compra. Tu pedido ha sido confirmado y lo estamos preparando para el envío.

RESUMEN DEL PEDIDO:
- Número de Pedido: {{ order_number }}
- Fecha del Pedido: {{ order_date }}
- Total: {{ order_total }}

Rastrear tu pedido: {{ order_tracking_url }}

¿QUÉ SUCEDERÁ A CONTINUACIÓN?
1. Prepararemos tu pedido (normalmente dentro de 1-2 días hábiles)
2. Recibirás una confirmación de envío con información de seguimiento
3. Tu pedido se entregará a: {{ shipping_address }}

💡 ¿SABÍAS QUE?
Puedes rastrear tu pedido en cualquier momento en tu panel de control de cuenta.

¿Tienes preguntas? Contáctanos: {{ support_url }}

---
Pedido #{{ order_number }} en {{ shop_name }}