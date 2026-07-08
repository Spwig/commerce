---
template_type: affiliate_high_commission_alert
category: Affiliate Program
---

# Email Template: affiliate_high_commission_alert

## Subject
⚠️ Atividade de Comissão Anormal Detectada - {{ affiliate_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Alerta de Comissão Alta
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Atividade Incomum Detectada
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Uma comissão anormalmente alta foi obtida pelo afiliado {{ affiliate_name }}. Isso requer revisão para prevenção de fraudes.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Detalhes do Alerta:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Afiliado:</strong> {{ affiliate_name }} ({{ affiliate_id }})<br/>
              <strong>Valor da Comissão:</strong> <span style="font-weight: bold; color: #dc2626;">
                {{ commission_amount }}
              </span><br/>
              <strong>Valor do Pedido:</strong> {{ order_value }}<br/>
              <strong>ID do Pedido:</strong> {{ order_number }}<br/>
              <strong>Detectado:</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Por Que Isso Foi Marcado:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ flag_reason }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Ações Recomendadas:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • Revise os detalhes do pedido para verificar legitimidade<br/>
          • Verifique o histórico de indicações do afiliado<br/>
          • Confirme que o cliente não está associado ao indicador<br/>
          • Aprova ou rejeita a comissão no painel de administração
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ review_commission_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Revisar Comissão
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ affiliate_details_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Ver Detalhes do Afiliado
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Esta comissão está pendente de revisão e não será paga até a aprovação.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ ALERTA DE COMISSÃO ALTA

Atividade Incomum Detectada

Uma comissão anormalmente alta foi obtida pelo afiliado {{ affiliate_name }}. Isso requer revisão para prevenção de fraudes.

DETALHES DO ALERTA:
- Afiliado: {{ affiliate_name }} ({{ affiliate_id }})
- Valor da Comissão: {{ commission_amount }}
- Valor do Pedido: {{ order_value }}
- ID do Pedido: {{ order_number }}
- Detectado: {{ detected_at }}

POR QUE ISSO FOI MARCADO:
{{ flag_reason }}

AÇÕES RECOMENDADAS:
• Revise os detalhes do pedido para verificar legitimidade
• Verifique o histórico de indicações do afiliado
• Confirme que o cliente não está associado ao indicador
• Aprova ou rejeita a comissão no painel de administração

Revisar comissão: {{ review_commission_url }}
Ver detalhes do afiliado: {{ affiliate_details_url }}

Esta comissão está pendente de revisão e não será paga até a aprovação.