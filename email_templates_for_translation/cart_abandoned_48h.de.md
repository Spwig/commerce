---
template_type: cart_abandoned_48h
category: Cart Recovery
---

# Email Template: cart_abandoned_48h

## Subject
Letzte Chance! Ihr Warenkorb läuft in 24 Stunden ab - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="#92400e" align="center">
          ⏰ Letzte Chance - Warenkorb läuft in 24 Stunden ab
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Verpassen Sie nicht, {{ customer_name }}!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Dies ist Ihre letzte Erinnerung. Ihr Warenkorb läuft in 24 Stunden ab und wir können diese Artikel nicht länger behalten.
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
              {{ item.quantity }} × {{ item.price }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        <mj-spacer height="20px" />

        <mj-text font-size="20px" font-weight="bold" align="right" color="{{ theme.color.text|default:'#1f2937' }}">
          Total: {{ cart_total }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ cart_url }}" background-color="#dc2626" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          Bestellung vervollständigen, bevor es zu spät ist
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Fragen? Unser Team ist hier, um zu helfen: <a href="{{ support_url }.json">Kontaktieren Sie den Support</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⏰ LETZTE CHANCE - WARENKORB LÄUFT IN 24 STUNDEN AB

Verpassen Sie nicht, {{ customer_name }}!

Dies ist Ihre letzte Erinnerung. Ihr Warenkorb läuft in 24 Stunden ab und wir können diese Artikel nicht länger behalten.

IHR WARENKORB:
{% for item in cart_items %}
- {{ item.product_name }}
  {{ item.quantity }} × {{ item.price }}
{% endfor %}

Total: {{ cart_total }}

Bestellung vervollständigen, bevor es zu spät ist: {{ cart_url }}

Fragen? Unser Team ist hier, um zu helfen: {{ support_url }}

---
Dies ist die letzte Erinnerung für den Warenkorb #{{ cart_id }}.