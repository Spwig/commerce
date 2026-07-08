---
template_type: pos_low_inventory_alert
category: POS
---

# Email Template: pos_low_inventory_alert

## Subject
📦 Lagerwarnung: {{ product_count }} Produkt{{ product_count|pluralize }} haben einen niedrigen Bestand bei {{ location_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          📦 Lagerwarnung
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Bestand wird knapp
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ product_count }} Produkt{{ product_count|pluralize }} {{ product_count|pluralize:'ist,sind' }} bei {{ location_name }} knapp.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Warnungsdetails:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Lagerort:</strong> {{ location_name }}<br/>
              <strong>Betroffene Produkte:</strong> {{ product_count }}<br/>
              <strong>Erkannt um:</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Produkte mit niedrigem Bestand:
        </mj-text>

        {% for item in low_stock_items %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ item.product_name }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              {% if item.variant_name %}<strong>Variante:</strong> {{ item.variant_name }}<br/>{% endif %}
              <strong>Aktueller Bestand:</strong> <span style="color: #dc2626; font-weight: bold;">{{ item.current_stock }}</span><br/>
              <strong>Neuauftragspunkt:</strong> {{ item.reorder_point }}<br/>
              <strong>SKU:</strong> {{ item.sku }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Empfohlene Maßnahmen:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • Bestellungen für Produkte mit niedrigem Bestand erstellen<br/>
          • Bestand von anderen Lagerorten übertragen<br/>
          • Neuauftragspunkte aktualisieren, wenn nötig<br/>
          • Übereinen Sie ggf. die Sicherheitsbestandsstufen
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ inventory_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Lagerbestand ansehen
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ purchase_orders_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Bestellung erstellen
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📦 LAGERWARNUNG

Bestand wird knapp

{{ product_count }} Produkt{{ product_count|pluralize }} {{ product_count|pluralize:'ist,sind' }} bei {{ location_name }} knapp.

WARNUNGSDetails:
- Lagerort: {{ location_name }}
- Betroffene Produkte: {{ product_count }}
- Erkannt um: {{ detected_at }}

PRODUKTE MIT NIEDRIGEM BESTAND:
{% for item in low_stock_items %}
{{ item.product_name }}
{% if item.variant_name %}Variante: {{ item.variant_name }}{% endif %}
Aktueller Bestand: {{ item.current_stock }}
Neuauftragspunkt: {{ item.reorder_point }}
SKU: {{ item.sku }}

{% endfor %}

EMPFOHLENE MAßNAHMEN:
• Bestellungen für Produkte mit niedrigem Bestand erstellen
• Bestand von anderen Lagerorten übertragen
• Neuauftragspunkte aktualisieren, wenn nötig
• Übereinen Sie ggf. die Sicherheitsbestandsstufen

Lagerbestand ansehen: {{ inventory_url }}
Bestellung erstellen: {{ purchase_orders_url }}