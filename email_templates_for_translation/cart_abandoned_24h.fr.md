---
template_type: cart_abandoned_24h
category: Cart Recovery
---

# Email Template: cart_abandoned_24h

## Subject
Toujours intéressé(e) ? Votre panier expirera bientôt - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Votre {{ cart_item_count }} article{{ cart_item_count|pluralize }} {{ cart_item_count|pluralize:'est,sont' }} toujours en attente
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Bonjour {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Nous conservons votre panier pour vous, mais ces articles ne dureront pas éternellement. Terminez votre achat avant qu'ils ne soient plus disponibles !
        </mj-text>

        <mj-spacer height="20px" />

        {% for item in cart_items %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column width="30%">
            <mj-image src="{{ item.product_image }}" alt="{{ item.product_name }}" border-radius="4px" />
          </mj-column>
          <mj-column width="70%">
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ item.product_name }}
            </mj-text>
            <mj-text color="{{ theme.color.text_secondary|default:'#6b7280' }}">
              Qty: {{ item.quantity }} × {{ item.price }}
            </mj-text>
            {% if item.low_stock %}
            <mj-text color="#dc2626" font-size="13px">
              ⚠️ Seulement {{ item.stock_remaining }} restant en stock !
            </mj-text>
            {% endif %}
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        <mj-spacer height="20px" />

        <mj-text font-size="18px" font-weight="bold" align="right" color="{{ theme.color.text|default:'#1f2937' }}">
          Total: {{ cart_total }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ cart_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Terminez votre commande maintenant
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              ✓ Livraison gratuite pour les commandes supérieures à {{ free_shipping_threshold }}<br/>
              ✓ Garantie de remboursement de 30 jours<br/>
              ✓ Paiement sécurisé
            </mj-text>
          </mj-column>
        </mj-section>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Votre {{ cart_item_count }} article{{ cart_item_count|pluralize }} {{ cart_item_count|pluralize:'est,sont' }} toujours en attente

Bonjour {{ customer_name }},

Nous conservons votre panier pour vous, mais ces articles ne dureront pas éternellement. Terminez votre achat avant qu'ils ne soient plus disponibles !

VOTRE PANIER:
{% for item in cart_items %}
- {{ item.product_name }}
  Qty: {{ item.quantity }} × {{ item.price }}
  {% if item.low_stock %}⚠️ Seulement {{ item.stock_remaining }} restant !{% endif %}
{% endfor %}

Total: {{ cart_total }}

Terminez votre commande maintenant: {{ cart_url }}

POURQUOI ACHETER CHEZ NOUS:
✓ Livraison gratuite pour les commandes supérieures à {{ free_shipping_threshold }}
✓ Garantie de remboursement de 30 jours
✓ Paiement sécurisé

---
Pour arrêter de recevoir des rappels de panier, visitez : {{ preferences_url }}