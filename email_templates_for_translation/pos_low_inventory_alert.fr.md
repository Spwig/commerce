---
template_type: pos_low_inventory_alert
category: POS
---

# Email Template: pos_low_inventory_alert

## Subject
📦 Alerte stock bas : {{ product_count }} produit{{ product_count|pluralize }} en stock bas à {{ location_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          📦 Alerte stock bas
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Stock bas
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ product_count }} produit{{ product_count|pluralize }} {{ product_count|pluralize:'is,are' }} en stock bas à {{ location_name }}.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Détails de l'alerte:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Location:</strong> {{ location_name }}<br/>
              <strong>Products Affected:</strong> {{ product_count }}<br/>
              <strong>Detected:</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Articles en stock bas:
        </mj-text>

        {% for item in low_stock_items %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ item.product_name }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              {% if item.variant_name %}<strong>Variant:</strong> {{ item.variant_name }}<br/>{% endif %}
              <strong>Current Stock:</strong> <span style="color: #dc2626; font-weight: bold;">{{ item.current_stock }}</span><br/>
              <strong>Reorder Point:</strong> {{ item.reorder_point }}<br/>
              <strong>SKU:</strong> {{ item.sku }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Actions recommandées:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • Créer des commandes d'achat pour les articles en stock bas<br/>
          • Transférer du stock depuis d'autres emplacements<br/>
          • Mettre à jour les points de commande si nécessaire<br/>
          • Considérer l'ajustement des niveaux de stock minimum
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ inventory_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Voir le stock
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ purchase_orders_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Créer une commande d'achat
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📦 ALERTE STOCK BAS

Stock bas

{{ product_count }} produit{{ product_count|pluralize }} {{ product_count|pluralize:'is,are' }} en stock bas à {{ location_name }}.

DÉTAILS DE L'ALERTE:
- Emplacement : {{ location_name }}
- Produits affectés : {{ product_count }}
- Détection : {{ detected_at }}

ARTICLES EN STOCK BAS:
{% for item in low_stock_items %}
{{ item.product_name }}
{% if item.variant_name %}Variant : {{ item.variant_name }}{% endif %}
Stock actuel : {{ item.current_stock }}
Point de commande : {{ item.reorder_point }}
SKU : {{ item.sku }}

{% endfor %}

ACTIONS RECOMMANDÉES:
• Créer des commandes d'achat pour les articles en stock bas
• Transférer du stock depuis d'autres emplacements
• Mettre à jour les points de commande si nécessaire
• Considérer l'ajustement des niveaux de stock minimum

Voir le stock : {{ inventory_url }}
Créer une commande d'achat : {{ purchase_orders_url }}