---
template_type: wishlist_reminder_weekly
category: Wishlist
---

# Email Template: wishlist_reminder_weekly

## Subject
Tu lista de deseos está esperando - {{ wishlist_item_count }} artículos guardados - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ❤️ Tu Lista de Deseos
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hola {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Tienes {{ wishlist_item_count }} artículo{{ wishlist_item_count|pluralize }} esperando en tu lista de deseos. Aquí te decimos qué ha pasado:
        </mj-text>

        <mj-spacer height="30px" />

        {% if price_drops_count > 0 %}
        <mj-section background-color="#dcfce7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="16px" font-weight="bold" color="#065f46">
              🔥 {{ price_drops_count }} Descuento de Precio{{ price_drops_count|pluralize }} Esta Semana!
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="15px" />
        {% endif %}

        {% if back_in_stock_count > 0 %}
        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="16px" font-weight="bold" color="#059669">
              ✓ {{ back_in_stock_count }} Artículo{{ back_in_stock_count|pluralize }} Disponible de Nuevo
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
              Fuera de Stock
            </mj-text>
            {% endif %}
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-button href="{{ wishlist_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Ver Lista de Deseos Completa
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          ¿No quieres recordatorios semanales? <a href="{{ unsubscribe_url }}">Dar de Baja</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❤️ TU LISTA DE DESEOS

Hola {{ customer_name }},

Tienes {{ wishlist_item_count }} artículo{{ wishlist_item_count|pluralize }} esperando en tu lista de deseos. Aquí te decimos qué ha pasado:

{% if price_drops_count > 0 %}🔥 {{ price_drops_count }} Descuento de Precio{{ price_drops_count|pluralize }} Esta Semana!{% endif %}
{% if back_in_stock_count > 0 %}✓ {{ back_in_stock_count }} Artículo{{ back_in_stock_count|pluralize }} Disponible de Nuevo{% endif %}

TU LISTA DE DESEOS:
{% for item in wishlist_items %}
- {{ item.product_name }}
  {% if item.price_dropped %}Was {{ item.old_price }}, Now {{ item.new_price }}{% else %}{{ item.price }}{% endif %}
  {% if not item.in_stock %}Fuera de Stock{% endif %}
{% endfor %}

Ver lista de deseos completa: {{ wishlist_url }}

¿No quieres recordatorios semanales? Dar de baja: {{ unsubscribe_url }}