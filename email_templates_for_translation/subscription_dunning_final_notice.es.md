---
template_type: subscription_dunning_final_notice
category: Subscriptions
---

# Email Template: subscription_dunning_final_notice

## Subject
⚠️ AVISO FINAL: Su suscripción se cancelará en {{ days_until_cancellation }} días

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#991b1b" align="center">
          ⚠️ AVISO FINAL
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Cancelación de suscripción inminente
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hola {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Este es su aviso final. No hemos podido procesar el pago de su suscripción {{ plan_name }}. Si no recibimos el pago dentro de {{ days_until_cancellation }} días, su suscripción se cancelará.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b" font-size="16px">
              ⚠️ Pago fallido - Acción requerida
            </mj-text>
            <mj-text color="#991b1b">
              <strong>Suscripción:</strong> {{ plan_name }}<br/>
              <strong>Monto adeudado:</strong> {{ amount_due }}<br/>
              <strong>Intentos fallidos:</strong> {{ retry_count }}<br/>
              <strong>Último intento:</strong> {{ last_retry_date }}<br/>
              <strong>Fecha de cancelación:</strong> <span style="font-weight: bold; font-size: 16px;">{{ cancellation_date }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Error de pago:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" font-family="monospace" color="{{ theme.color.text|default:'#4b5563' }}">
              {{ payment_error_message }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ¿Qué ocurrirá:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          Si no se recibe el pago para {{ cancellation_date }}:<br/>
          • Su suscripción se cancelará<br/>
          • Perderá el acceso a todos los beneficios de la suscripción<br/>
          • Sus datos podrían eliminarse (consulte la política de retención)<br/>
          • Tendrá que suscribirse nuevamente para recuperar el acceso
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          Actualice su método de pago ahora
        </mj-text>

        <mj-spacer height="20px" />

        <mj-button href="{{ update_payment_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Actualizar método de pago
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Problemas comunes y soluciones:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • <strong>Tarjeta caducada:</strong> Actualice con una tarjeta de crédito actual<br/>
          • <strong>Fondos insuficientes:</strong> Asegúrese de tener un saldo suficiente<br/>
          • <strong>Tarjeta rechazada:</strong> Contacte su banco o use una tarjeta diferente<br/>
          • <strong>Discrepancia de dirección:</strong> Verifique que la dirección de facturación coincida con la tarjeta
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" font-weight="bold">
              ¿Necesita ayuda?
            </mj-text>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              Si está experimentando problemas con los pagos o necesita asistencia, por favor póngase en contacto con nuestro equipo de soporte lo antes posible.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Contactar soporte
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Si desea cancelar su suscripción, puede hacerlo en la configuración de su cuenta.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ AVISO FINAL

Cancelación de suscripción inminente

Hola {{ customer_name }},

Este es su aviso final. No hemos podido procesar el pago de su suscripción {{ plan_name }}. Si no recibimos el pago dentro de {{ days_until_cancellation }} días, su suscripción se cancelará.

⚠️ PAGO FALLIDO - ACCIÓN REQUERIDA:
- Suscripción: {{ plan_name }}
- Monto adeudado: {{ amount_due }}
- Intentos fallidos: {{ retry_count }}
- Último intento: {{ last_retry_date }}
- Fecha de cancelación: {{ cancellation_date }}

ERROR DE PAGO:
{{ payment_error_message }}

¿QUÉ OCURRIRÁ:
Si no se recibe el pago para {{ cancellation_date }}:
• Su suscripción se cancelará
• Perderá el acceso a todos los beneficios de la suscripción
• Sus datos podrían eliminarse (consulte la política de retención)
• Tendrá que suscribirse nuevamente para recuperar el acceso

ACTUALICE SU MÉTODO DE PAGO AHORA

Problemas comunes y soluciones:
• Tarjeta caducada: Actualice con una tarjeta de crédito actual
• Fondos insuficientes: Asegúrese de tener un saldo suficiente
• Tarjeta rechazada: Contacte su banco o use una tarjeta diferente
• Discrepancia de dirección: Verifique que la dirección de facturación coincida con la tarjeta

¿NECESITA AYUDA?
Si está experimentando problemas con los pagos o necesita asistencia, por favor póngase en contacto con nuestro equipo de soporte lo antes posible.

Actualizar método de pago: {{ update_payment_url }}
Contactar soporte: {{ support_url }}

Si desea cancelar su suscripción, puede hacerlo en la configuración de su cuenta.