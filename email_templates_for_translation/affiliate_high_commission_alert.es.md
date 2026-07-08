---
template_type: affiliate_high_commission_alert
category: Affiliate Program
---

# Email Template: affiliate_high_commission_alert

## Subject
⚠️ Actividad de comisión inusual detectada - {{ affiliate_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ High Commission Alert
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Unusual Activity Detected
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          An unusually high commission has been earned by affiliate {{ affiliate_name }}. This requires review for fraud prevention.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Alert Details:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Affiliate:</strong> {{ affiliate_name }} ({{ affiliate_id }})<br/>
              <strong>Commission Amount:</strong> <span style="font-weight: bold; color: #dc2626;">{{ commission_amount }}</span><br/>
              <strong>Order Value:</strong> {{ order_value }}<br/>
              <strong>Order ID:</strong> {{ order_number }}<br/>
              <strong>Detected:</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Why This Was Flagged:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ flag_reason }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Recommended Actions:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • Review the order details for legitimacy<br/>
          • Check affiliate's referral history<br/>
          • Verify customer is not affiliated with referrer<br/>
          • Approve or reject commission in admin panel
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ review_commission_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Review Commission
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ affiliate_details_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          View Affiliate Details
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          This commission is pending review and will not be paid until approved.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ ALTA COMISIÓN DETECTADA

Actividad inusual detectada

Se ha obtenido una comisión inusualmente alta por parte del afiliado {{ affiliate_name }}. Esto requiere revisión para la prevención de fraude.

DETALLES DE LA ALERTA:
- Afiliado: {{ affiliate_name }} ({{ affiliate_id }})
- Monto de la comisión: {{ commission_amount }}
- Valor del pedido: {{ order_value }}
- ID del pedido: {{ order_number }}
- Detectado: {{ detected_at }}

POR QUÉ SE MARCÓ ESTO:
{{ flag_reason }}

ACCIONES RECOMENDADAS:
• Revisar los detalles del pedido para verificar su legitimidad
• Revisar el historial de referidos del afiliado
• Verificar que el cliente no esté relacionado con el referidor
• Aprobar o rechazar la comisión en el panel de administración

Revisar comisión: {{ review_commission_url }}
Ver detalles del afiliado: {{ affiliate_details_url }}

Esta comisión está pendiente de revisión y no se pagará hasta que se apruebe.