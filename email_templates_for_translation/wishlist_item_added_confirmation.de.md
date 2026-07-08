---
template_type: wishlist_item_added_confirmation
category: Wishlist
---

# Email Template: wishlist_item_added_confirmation

## Subject
✓ {{ product_name }} wurde zur Wunschliste hinzugefügt - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ❤️ Zur Wunschliste hinzugefügt!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Sie haben {{ product_name }} erfolgreich zur Wunschliste hinzugefügt. Wir werden darauf achten!
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column width="35%">
            <mj-image src="{{ product_image }}" alt="{{ product_name }}" border-radius="8px" />
          </mj-column>
          <mj-column width="65%">
            <mj-text font-weight="bold" font-size="18px" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ product_name }}
            </mj-text>
            <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}">
              {{ product_price }}
            </mj-text>
            {% if product_in_stock %}
            <mj-text font-size="13px" color="#059669">
              ✓ Auf Lager
            </mj-text>
            {% else %}
            <mj-text font-size="13px" color="#dc2626">
              ⚠️ Ausverkauft - Wir benachrichtigen Sie, sobald es wieder verfügbar ist!
            </mj-text>
            {% endif %}
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              💡 <strong>Wir benachrichtigen Sie über:</strong><br/>
              • Preissenkungen<br/>
              • Benachrichtigungen, wenn wieder auf Lager<br/>
              • Begrenzte Verkaufsaktionen
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ wishlist_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Wunschliste ansehen
        </mj-button>

        {% if product_in_stock %}
        <mj-spacer height="10px" />
        <mj-button href="{{ product_url }}" background-color="#059669" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Jetzt kaufen
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❤️ ZUR WUNSCHLISTE HINZUGEFÜGT!

Hi {{ customer_name }},

Sie haben {{ product_name }} erfolgreich zur Wunschliste hinzugefügt. Wir werden darauf achten!

{{ product_name }}
Preis: {{ product_price }}
{% if product_in_stock %}✓ Auf Lager{% else %}⚠️ Ausverkauft - Wir benachrichtigen Sie, sobald es wieder verfügbar ist!{% endif %}

💡 WIR BENACHRICHTIGEN SIE ÜBER:
• Preissenkungen
• Benachrichtigungen, wenn wieder auf Lager
• Begrenzte Verkaufsaktionen

Wunschliste ansehen: {{ wishlist_url }}
{% if product_in_stock %}Jetzt kaufen: {{ product_url }}{% endif %}