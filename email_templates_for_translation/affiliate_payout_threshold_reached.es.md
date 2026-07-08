---
template_type: affiliate_payout_threshold_reached
category: Affiliate Program
---

# Email Template: affiliate_payout_threshold_reached

## Subject
💰 ¡Has alcanzado el umbral de pago mínimo!

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          💰 ¡Umbral de pago alcanzado!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ¡Buena noticia!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hola {{ affiliate_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          ¡Felicidades! Tu saldo de afiliado ha alcanzado el umbral mínimo de pago. Ahora puedes solicitar un pago.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Tu saldo:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Saldo disponible:</strong> <span style="font-size: 24px; font-weight: bold; color: #059669;">{{ available_balance }}</span><br/>
              <strong>Mínimo de pago:</strong> {{ minimum_payout }}<br/>
              <strong>Comisiones pendientes:</strong> {{ pending_balance }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ¿Qué sigue:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • Solicite un pago desde su panel de afiliados<br/>
          • Los pagos se procesan {{ payout_schedule }}<br/>
          • Los fondos se enviarán mediante {{ payment_method }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ request_payout_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Solicitar pago
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ portal_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Ver panel
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
💰 ¡SE HA ALCANZADO EL LÍMITE DE PAGO!

¡Buena noticia!

Hola {{ affiliate_name }},

¡Felicidades! Tu saldo de afiliado ha alcanzado el umbral mínimo de pago. Ahora puedes solicitar un pago.

TU SALDO:
- Saldo disponible: {{ available_balance }}
- Mínimo de pago: {{ minimum_payout }}
- Comisiones pendientes: {{ pending_balance }}

¿QUÉ SIGUE:
• Solicite un pago desde su panel de afiliados
• Los pagos se procesan {{ payout_schedule }}
• Los fondos se enviarán mediante {{ payment_method }}

Solicitar pago: {{ request_payout_url }}
Ver panel: {{ portal_url }}