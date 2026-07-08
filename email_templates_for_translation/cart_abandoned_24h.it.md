---
template_type: cart_abandoned_24h
category: Cart Recovery
---

# Email Template: cart_abandoned_24h

## Subject
Ancora interessato? Il tuo carrello scade presto - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Il tuo {{ cart_item_count }} articolo{{ cart_item_count|pluralize }} {{ cart_item_count|pluralize:'is,are' }} in attesa
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Ciao {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Ti stiamo tenendo il carrello, ma questi articoli non dureranno per sempre. Completa l'acquisto prima che siano andati!
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
              ⚠️ Solo {{ item.stock_remaining }} rimasti in magazzino!
            </mj-text>
            {% endif %}
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        <mj-spacer height="20px" />

        <mj-text font-size="18px" font-weight="bold" align="right" color="{{ theme.color.text|default:'#1f2937' }}">
          Totale: {{ cart_total }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ cart_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Completa il tuo ordine adesso
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              ✓ Spedizione gratuita per ordini superiori a {{ free_shipping_threshold }}<br/>
              ✓ Garanzia di rimborso di 30 giorni<br/>
              ✓ Checkout sicuro
            </mj-text>
          </mj-column>
        </mj-section>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Il tuo {{ cart_item_count }} articolo{{ cart_item_count|pluralize }} {{ cart_item_count|pluralize:'is,are' }} in attesa

Ciao {{ customer_name }},

Ti stiamo tenendo il carrello, ma questi articoli non dureranno per sempre. Completa l'acquisto prima che siano andati!

IL TUO CARRELLO:
{% for item in cart_items %}
- {{ item.product_name }}
  Qty: {{ item.quantity }} × {{ item.price }}
  {% if item.low_stock %}⚠️ Solo {{ item.stock_remaining }} rimasti!{% endif %}
{% endfor %}

Totale: {{ cart_total }}

Completa il tuo ordine adesso: {{ cart_url }}

PERCHÉ ACQUISTARE DA NOI:
✓ Spedizione gratuita per ordini superiori a {{ free_shipping_threshold }}
✓ Garanzia di rimborso di 30 giorni
✓ Checkout sicuro

---
Per smettere di ricevere i ricordi del carrello, visita: {{ preferences_url }}