---
template_type: cart_abandoned_1h
category: Cart Recovery
---

# Email Template: cart_abandoned_1h

## Subject
Ihr Warenkorb wartet! Bestellung abschließen - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Sie haben {{ cart_item_count }} Artikel{{ cart_item_count|pluralize }} in Ihrem Warenkorb gelassen
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj:text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Wir haben bemerkt, dass Sie Ihren Kauf nicht abgeschlossen haben. Ihre Artikel warten weiterhin in Ihrem Warenkorb!
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
          Bestellung abschließen
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Benötigen Sie Hilfe? <a href="{{ support_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Kontaktieren Sie unser Support-Team</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Sie haben {{ cart_item_count }} Artikel{{ cart_item_count|pluralize }} in Ihrem Warenkorb gelassen

Hi {{ customer_name }},

Wir haben bemerkt, dass Sie Ihren Kauf nicht abgeschlossen haben. Ihre Artikel warten weiterhin in Ihrem Warenkorb!

IHR WARENKORB:
{% for item in cart_items %}
- {{ item.product_name }}
  Qty: {{ item.quantity }} × {{ item.price }}
{% endfor %}

Total: {{ cart_total }}

Bestellung abschließen: {{ cart_url }}

Benötigen Sie Hilfe? Kontaktieren Sie unser Support-Team: {{ support_url }}

---
Sie erhalten diese E-Mail, weil Sie Artikel zu Ihrem Warenkorb bei {{ shop_name }} hinzugefügt haben.
Um keine weiteren Warenkorb-Erinnerungen mehr zu erhalten, besuchen Sie: {{ preferences_url }}

