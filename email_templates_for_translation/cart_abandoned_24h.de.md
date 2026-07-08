---
template_type: cart_abandoned_24h
category: Cart Recovery
---

# Email Template: cart_abandoned_24h

## Subject
Noch Interesse? Dein Warenkorb läuft bald ab - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Dein {{ cart_item_count }} Artikel{{ cart_item_count|pluralize }} {{ cart_item_count|pluralize:'ist,sind' }} noch in der Wartezeit
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hallo {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Wir halten deinen Warenkorb für dich bereit, aber diese Artikel werden nicht ewig bestehen. Vervollständige deinen Kauf, bevor sie weg sind!
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
              ⚠️ Nur noch {{ item.stock_remaining }} verfügbar!
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
          Deine Bestellung jetzt abschließen
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              ✓ Kostenlose Lieferung bei Bestellungen über {{ free_shipping_threshold }}<br/>
              ✓ 30-tägige Geld-zurück-Garantie<br/>
              ✓ Sicherer Checkout
            </mj-text>
          </mj-column>
        </mj-section>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Dein {{ cart_item_count }} Artikel{{ cart_item_count|pluralize }} {{ cart_item_count|pluralize:'ist,sind' }} noch in der Wartezeit

Hallo {{ customer_name }},

Wir halten deinen Warenkorb für dich bereit, aber diese Artikel werden nicht ewig bestehen. Vervollständige deinen Kauf, bevor sie weg sind!

DEIN WARENKORB:
{% for item in cart_items %}
- {{ item.product_name }}
  Qty: {{ item.quantity }} × {{ item.price }}
  {% if item.low_stock %}⚠️ Nur noch {{ item.stock_remaining }} verfügbar!{% endif %}
{% endfor %}

Total: {{ cart_total }}

Deine Bestellung jetzt abschließen: {{ cart_url }}

WARUM BEI UNS KAUFEN:
✓ Kostenlose Lieferung bei Bestellungen über {{ free_shipping_threshold }}
✓ 30-tägige Geld-zurück-Garantie
✓ Sicherer Checkout

---
Um keine weiteren Erinnerungen für den Warenkorb zu erhalten, besuche: {{ preferences_url }}