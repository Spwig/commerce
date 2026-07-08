---
template_type: pos_low_inventory_alert
category: POS
---

# Email Template: pos_low_inventory_alert

## Subject
📦 Alerta de Estoque Baixo: {{ product_count }} produto{{ product_count|pluralize }} com estoque baixo em {{ location_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          📦 Alerta de Estoque Baixo
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Estoque Baixo
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ product_count }} produto{{ product_count|pluralize }} {{ product_count|pluralize:'is,are' }} com estoque baixo em {{ location_name }}.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Detalhes do Alerta:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Local:</strong> {{ location_name }}<br/>
              <strong>Produtos Afetados:</strong> {{ product_count }}<br/>
              <strong>Detectado:</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Itens com Estoque Baixo:
        </mj-text>

        {% for item in low_stock_items %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ item.product_name }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              {% if item.variant_name %}<strong>Variação:</strong> {{ item.variant_name }}<br/>{% endif %}
              <strong>Estoque Atual:</strong> <span style="color: #dc2626; font-weight: bold;">{{ item.current_stock }}</span><br/>
              <strong>Ponto de Reordem:</strong> {{ item.reorder_point }}<br/>
              <strong>SKU:</strong> {{ item.sku }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Ações Recomendadas:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • Criar pedidos de compra para itens com estoque baixo<br/>
          • Transferir estoque de outras localizações<br/>
          • Atualizar os pontos de reordem, se necessário<br/>
          • Considere ajustar os níveis de par
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ inventory_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Ver Estoque
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ purchase_orders_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Criar Pedido de Compra
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📦 ALERTA DE ESTOQUE BAIXO

Estoque Baixo

{{ product_count }} produto{{ product_count|pluralize }} {{ product_count|pluralize:'is,are' }} com estoque baixo em {{ location_name }}.

DETALHES DO ALERTA:
- Local: {{ location_name }}
- Produtos Afetados: {{ product_count }}
- Detectado: {{ detected_at }}

ITENS COM ESTOQUE BAIXO:
{% for item in low_stock_items %}
{{ item.product_name }}
{% if item.variant_name %}Variação: {{ item.variant_name }}{% endif %}
Estoque Atual: {{ item.current_stock }}
Reorder Point: {{ item.reorder_point }}
SKU: {{ item.sku }}

{% endfor %}

AÇÕES RECOMENDADAS:
• Criar pedidos de compra para itens com estoque baixo
• Transferir estoque de outras localizações
• Atualizar os pontos de reordem, se necessário
• Considere ajustar os níveis de par

Ver estoque: {{ inventory_url }}
Criar pedido de compra: {{ purchase_orders_url }}