---
template_type: shipping_tracking_milestone
category: Shipping
---

# Email Template: shipping_tracking_milestone

## Subject
Seu pedido #{{ order_number }} está {{ milestone_status }} - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Atualização de Entrega: {{ milestone_status }}
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Olá {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Boa noticia! Seu pedido alcançou uma etapa importante em sua jornada até você.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
              📦 {{ milestone_status }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
              {{ milestone_description }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Detalhes do Pedido:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Número do Pedido:</strong> {{ order_number }}<br/>
              <strong>Número de Rastreamento:</strong> {{ tracking_number }}<br/>
              <strong>Transportadora:</strong> {{ carrier_name }}<br/>
              <strong>Local Atual:</strong> {{ current_location }}<br/>
              <strong>Entrega Estimada:</strong> {{ estimated_delivery }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Rastrear Seu Pacote
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Dúvidas sobre sua entrega? <a href="{{ support_url }.json">Contate o Suporte</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Atualização de Entrega: {{ milestone_status }}

Olá {{ customer_name }},

Boa noticia! Seu pedido alcançou uma etapa importante em sua jornada até você.

📦 {{ milestone_status }}
{{ milestone_description }}

DETALHES DO PEDIDO:
- Número do Pedido: {{ order_number }}
- Número de Rastreamento: {{ tracking_number }}
- Transportadora: {{ carrier_name }}
- Local Atual: {{ current_location }}
- Entrega Estimada: {{ estimated_delivery }}

Rastrear seu pacote: {{ tracking_url }}

Dúvidas sobre sua entrega? Contate o Suporte: {{ support_url }}