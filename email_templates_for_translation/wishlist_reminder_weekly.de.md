---
template_type: wishlist_reminder_weekly
category: Wishlist
---

# Email Template: wishlist_reminder_weekly

## Subject
Ihr Wunschzettel wartet - {{ wishlist_item_count }} Artikel gespeichert - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ❤️ Ihr Wunschzettel
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Sie haben {{ wishlist_item_count }} Artikel{{ wishlist_item_count|pluralize }} in Ihrem Wunschzettel wartend. Hier sind die neuesten Updates:
        </mj-text>

        <mj-spacer height="30px" />

        {% if price_drops_count > 0 %}
        <mj-section background-color="#dcfce7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="16px" font-weight="bold" color="#065f46">
              🔥 {{ price_drops_count }} Preisverfall{{ price_drops_count|pluralize }} Diese Woche!
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="15px" />
        {% endif %}

        {% if back_in_stock_count > 0 %}
        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="16px" font-weight="bold" color="#059669">
              ✓ {{ back_in_stock_count }} Artikel{{ back_in_stock_count|pluralize }} Wieder auf Lager
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
              <span style="text-decoration: line-through; color: #9ca3af;">
                {{ item.old_price }}
              </span>
              <span style="color: #059669; font-weight: bold;">
                {{ item.new_price }}
              </span>
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
          Wunschzettel vollständig ansehen
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Keine wöchentlichen Erinnerungen mehr? <a href="{{ unsubscribe_url }}">Abonnieren</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❤️ IHR WUNSCHZETTEL

Hi {{ customer_name }},

Sie haben {{ wishlist_item_count }} Artikel{{ wishlist_item_count|pluralize }} in Ihrem Wunschzettel wartend. Hier sind die neuesten Updates:

{% if price_drops_count > 0 %}🔥 {{ price_drops_count }} Preisverfall{{ price_drops_count|pluralize }} Diese Woche!{% endif %}
{% if back_in_stock_count > 0 %}✓ {{ back_in_stock_count }} Artikel{{ back_in_stock_count|pluralize }} Wieder auf Lager{% endif %}

IHR WUNSCHZETTEL:
{% for item in wishlist_items %}- {{ item.product_name }}
  {% if item.price_dropped %}War {{ item.old_price }}, Jetzt {{ item.new_price }}{% else %}{{ item.price }}{% endif %}
  {% if not item.in_stock %}Out of Stock{% endif %}
{% endfor %}

Wunschzettel vollständig ansehen: {{ wishlist_url }}

Keine wöchentlichen Erinnerungen mehr? Abonnieren: {{ unsubscribe_url }}