---
template_type: return_received
category: Returns
---

# Email Template: return_received

## Subject
Hemos Recibido Tu Devolución - Orden #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#eff6ff' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.primary|default:'#1d4ed8' }}">
          Devolución Recibida
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.primary|default:'#1d4ed8' }}">
          Orden #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hola {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hemos recibido tus artículos devueltos para la orden <strong>#{{ order_number }}</strong>.
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>¿Qué sucede a continuación:</strong>
        </mj-text>

        <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
          1. Nuestro equipo inspeccionará los artículos devueltos dentro de 2-3 días hábiles<br/>
          2. Verificaremos que los artículos estén en su estado original<br/>
          3. Una vez completada la inspección, procesaremos tu reembolso<br/>
          4. Recibirás un correo electrónico de confirmación una vez que se haya procesado el reembolso
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          El reembolso se acreditará en tu método de pago original y puede tomar 5-10 días hábiles para aparecer en tu cuenta.
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Gracias por tu paciencia!
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Devolución Recibida - Orden #{{ order_number }}

Hola {{ customer_name }},

Hemos recibido tus artículos devueltos para la orden #{{ order_number }}.

¿Qué sucede a continuación:
1. Nuestro equipo inspeccionará los artículos devueltos dentro de 2-3 días hábiles
2. Verificaremos que los artículos estén en su estado original
3. Una vez completada la inspección, procesaremos tu reembolso
4. Recibirás un correo electrónico de confirmación una vez que se haya procesado el reembolso

El reembolso se acreditará en tu método de pago original y puede tomar 5-10 días hábiles para aparecer en tu cuenta.

Gracias por tu paciencia!