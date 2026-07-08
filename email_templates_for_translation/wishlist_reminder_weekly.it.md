---
template_type: wishlist_reminder_weekly
category: Wishlist
---

# Email Template: wishlist_reminder_weekly

## Subject
La tua lista dei desideri è in attesa - {{ wishlist_item_count }} articoli salvati - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ❤️ La tua Lista dei Desideri
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hai {{ wishlist_item_count }} articolo{{ wishlist_item_count|pluralize }} in attesa nella tua lista dei desideri. Ecco cosa è successo:
        </mj-text>

        <mj-spacer height="30px" />

        {% if price_drops_count > 0 %}
        <mj-section background-color="#dcfce7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="16px" font-weight="bold" color="#065f46">
              🔥 {{ price_drops_count }} Riduzione di Prezzo{{ price_drops_count|pluralize }} Questa Settimana!
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="15px" />
        {% endif %}

        {% if back_in_stock_count > 0 %}
        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="16px" font-weight="bold" color="#059669">
              ✓ {{ back_in_stock_count }} Articolo{{ back_in_stock_count|pluralize }} Disponibile di Nuovo
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="30px" />
        {% endif %}

        {% for item in wishlist_items %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column width="25%">
            <mj-image src="{{ item.product_image }}" alt="{{ item.product_name }}" border-radius="4px" />
          </mj-column>
          <mj-column width="75%">
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ item.product_name }}
            </mj-text>
            {% if item.price_dropped %}
            <mj-text font-size="14px">
              <span style="text-decoration: line-through; color: #9ca3af;">{{ item.old_price }}</span>
              <span style="color: #059669; font-weight: bold;"> {{ item.new_price }}</span>
            </mj-text>
            {% else %}
            <mj-text font-size="15px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}">
              {{ item.price }}
            </mj-text>
            {% endif %}
            {% if not item.in_stock %}
            <mj-text font-size="13px" color="#dc2626">
              Out of Stock
            </mj-text>
            {% endif %}
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-button href="{{ wishlist_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Visualizza l'intera lista dei desideri
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Non vuoi ricevere promemoria settimanali? <a href="{{ unsubscribe_url }}">Annulla l'iscrizione</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❤️ LA TUA LISTA DEI DESIDERI

Hi {{ customer_name }},

Hai {{ wishlist_item_count }} articolo{{ wishlist_item_count|pluralize }} in attesa nella tua lista dei desideri. Ecco cosa è successo:

{% if price_drops_count > 0 %}🔥 {{ price_drops_count }} Riduzione di Prezzo{{ price_drops_count|pluralize }} Questa Settimana!{% endif %}
{% if back_in_stock_count > 0 %}✓ {{ back_in_stock_count }} Articolo{{ back_in_stock_count|pluralize }} Disponibile di Nuovo{% endif %}

LA TUA LISTA DEI DESIDERI:
{% for item in wishlist_items %}- {{ item.product_name }}
  {% if item.price_dropped %}Was {{ item.old_price }}, Now {{ item.new_price }}{% else %}{{ item.price }}{% endif %}
  {% if not item.in_stock %}Out of Stock{% endif %}
{% endfor %}

Visualizza l'intera lista dei desideri: {{ wishlist_url }}

Non vuoi ricevere promemoria settimanali? Annulla l'iscrizione: {{ unsubscribe_url }}
