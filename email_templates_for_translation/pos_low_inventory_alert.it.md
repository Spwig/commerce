---
template_type: pos_low_inventory_alert
category: POS
---

# Email Template: pos_low_inventory_alert

## Subject
📦 Alerte di basso stock: {{ product_count }} prodotto{{ product_count|pluralize }} in esaurimento a {{ location_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          📦 Alerta di basso inventario
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Stock in esaurimento
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ product_count }} prodotto{{ product_count|pluralize }} {{ product_count|pluralize:'is,are' }} in esaurimento a {{ location_name }}.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Dettagli dell'alert:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Location:</strong> {{ location_name }}<br/>
              <strong>Prodotti interessati:</strong> {{ product_count }}<br/>
              <strong>Rilevato:</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Prodotti con basso stock:
        </mj-text>

        {% for item in low_stock_items %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ item.product_name }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              {% if item.variant_name %}<strong>Variant:</strong> {{ item.variant_name }}<br/>{% endif %}
              <strong>Stock corrente:</strong> <span style="color: #dc2626; font-weight: bold;">{{ item.current_stock }}</span><br/>
              <strong>Punto di riordino:</strong> {{ item.reorder_point }}<br/>
              <strong>SKU:</strong> {{ item.sku }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Azioni consigliate:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • Creare ordini di acquisto per gli articoli con basso stock<br/>
          • Trasferire lo stock da altre ubicazioni<br/>
          • Aggiornare i punti di riordino se necessario<br/>
          • Considerare l'adattamento dei livelli di parità
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ inventory_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Visualizza inventario
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ purchase_orders_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Crea ordine di acquisto
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📦 ALERT DI BASSO STOCK

Stock in esaurimento

{{ product_count }} prodotto{{ product_count|pluralize }} {{ product_count|pluralize:'is,are' }} in esaurimento a {{ location_name }}.

DETTAGLI DELL'ALERT:
- Location: {{ location_name }}
- Prodotti interessati: {{ product_count }}
- Rilevato: {{ detected_at }}

PRODOTTI CON BASSO STOCK:
{% for item in low_stock_items %}
{{ item.product_name }}
{% if item.variant_name %}Variant: {{ item.variant_name }}{% endif %}
Stock corrente: {{ item.current_stock }}
Punto di riordino: {{ item.reorder_point }}
SKU: {{ item.sku }}

{% endfor %}

AZIONI CONSIGLIATE:
• Creare ordini di acquisto per gli articoli con basso stock
• Trasferire lo stock da altre ubicazioni
• Aggiornare i punti di riordino se necessario
• Considerare l'adattamento dei livelli di parità

Visualizza inventario: {{ inventory_url }}
Crea ordine di acquisto: {{ purchase_orders_url }}