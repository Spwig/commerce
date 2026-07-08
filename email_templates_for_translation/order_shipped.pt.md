---
template_type: order_shipped
category: Core E-commerce
---

# Email Template: order_shipped

## Subject
Seu pedido #{{ order_number }} foi enviado!

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          📦 Pedido Enviado!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          No Caminho!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Olá {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Boa notícia! Seu pedido foi enviado e está a caminho.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Detalhes de Envio:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Número do Pedido:</strong> {{ order_number }}<br/>
              <strong>Número de Rastreamento:</strong> {{ tracking_number }}<br/>
              <strong>Transportadora:</strong> {{ carrier_name }}<br/>
              <strong>Entrega Estimada:</strong> {{ estimated_delivery }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Rastrear seu Pacote
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📦 PEDIDO ENVIADO!

No Caminho!

Olá {{ customer_name }},

Boa notícia! Seu pedido foi enviado e está a caminho.

DETALHES DE ENVIO:
- Número do Pedido: {{ order_number }}
- Número de Rastreamento: {{ tracking_number }}
- Transportadora: {{ carrier_name }}
- Entrega Estimada: {{ estimated_delivery }}

Rastrear seu pacote: {{ tracking_url }}