---
template_type: shipping_delayed
category: Shipping
---

# Email Template: shipping_delayed

## Subject
Atualização sobre seu pedido #{{ order_number }} - Atraso na entrega

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Atualização sobre seu Pedido
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Olá {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Gostaríamos de informar sobre um atraso no seu pedido. Pedimos desculpas pela inconveniência e agradecemos sua paciência.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Detalhes do Pedido:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Número do Pedido:</strong> {{ order_number }}<br/>
              <strong>Data de Entrega Original:</strong> {{ original_delivery_date }}<br/>
              <strong>Nova Data de Entrega:</strong> {{ new_delivery_date }}<br/>
              <strong>Número de Rastreamento:</strong> {{ tracking_number }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Motivo do Atraso:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ delay_reason }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Rastrear seu Pedido
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          Estamos trabalhando para entregar seu pedido o mais rápido possível. Você receberá uma atualização adicional quando seu pacote estiver a caminho.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Perguntas? <a href="{{ support_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Entre em contato com nossa equipe de atendimento ao cliente</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Atualização sobre seu Pedido #{{ order_number }}

Olá {{ customer_name }},

Gostaríamos de informar sobre um atraso no seu pedido. Pedimos desculpas pela inconveniência e agradecemos sua paciência.

DETALHES DO PEDIDO:
- Número do Pedido: {{ order_number }}
- Data de Entrega Original: {{ original_delivery_date }}
- Nova Data de Entrega: {{ new_delivery_date }}
- Número de Rastreamento: {{ tracking_number }}

MOTIVO DO ATRASO:
{{ delay_reason }}

Rastrear seu pedido: {{ tracking_url }}

Estamos trabalhando para entregar seu pedido o mais rápido possível. Você receberá uma atualização adicional quando seu pacote estiver a caminho.

Perguntas? Entre em contato com nossa equipe de atendimento ao cliente: {{ support_url }}

---
Esta atualização é para o pedido #{{ order_number }} na {{ shop_name }}.