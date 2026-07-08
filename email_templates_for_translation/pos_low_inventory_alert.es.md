---
template_type: pos_low_inventory_alert
category: POS
---

# Email Template: pos_low_inventory_alert

## Subject
📦 Alerta de Stock Bajo: {{ product_count }} producto{{ product_count|pluralize }} con stock bajo en {{ location_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          📦 Alerta de Inventario Bajo
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Stock con Bajo Nivel
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ product_count }} producto{{ product_count|pluralize }} {{ product_count|pluralize:'is,are' }} con stock bajo en {{ location_name }}.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Detalles de la Alerta:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Ubicación:</strong> {{ location_name }}<br/>
              <strong>Productos Afectados:</strong> {{ product_count }}<br/>
              <strong>Detectado:</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Productos con Bajo Stock:
        </mj-text>

        {% for item in low_stock_items %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ item.product_name }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              {% if item.variant_name %}<strong>Variedad:</strong> {{ item.variant_name }}<br/>{% endif %}
              <strong>Stock Actual:</strong> <span style="color: #dc2626; font-weight: bold;">{{ item.current_stock }}</span><br/>
              <strong>Punto de Reorden:</strong> {{ item.reorder_point }}<br/>
              <strong>SKU:</strong> {{ item.sku }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Acciones Recomendadas:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • Crear pedidos de compra para productos con bajo stock<br/>
          • Transferir stock desde otras ubicaciones<br/>
          • Actualizar puntos de reorden si es necesario<br/>
          • Considerar ajustar los niveles de par
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ inventory_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Ver Inventario
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ purchase_orders_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Crear Pedido de Compra
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📦 ALERTA DE INVENTARIO BAJO

Stock con Bajo Nivel

{{ product_count }} producto{{ product_count|pluralize }} {{ product_count|pluralize:'is,are' }} con stock bajo en {{ location_name }}.

DETALLES DE LA ALERTA:
- Ubicación: {{ location_name }}
- Productos Afectados: {{ product_count }}
- Detectado: {{ detected_at }}

PRODUCTOS CON BAJO STOCK:
{% for item in low_stock_items %}
{{ item.product_name }}
{% if item.variant_name %}Variedad: {{ item.variant_name }}{% endif %}
Stock Actual: {{ item.current_stock }}
Reorder Point: {{ item.reorder_point }}
SKU: {{ item.sku }}

{% endfor %}

ACCIONES RECOMENDADAS:
• Crear pedidos de compra para productos con bajo stock
• Transferir stock desde otras ubicaciones
• Actualizar puntos de reorden si es necesario
• Considerar ajustar los niveles de par

Ver inventario: {{ inventory_url }}
Crear pedido de compra: {{ purchase_orders_url }}