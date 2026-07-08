---
template_type: wishlist_reminder_weekly
category: Wishlist
---

# Email Template: wishlist_reminder_weekly

## Subject
Ваш список желаний ждёт - {{ wishlist_item_count }} товаров - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ❤️ Ваш список желаний
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Здравствуйте, {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          У вас {{ wishlist_item_count }} товар{{ wishlist_item_count|pluralize }} в списке желаний. Вот что произошло:
        </mj-text>

        <mj-spacer height="30px" />

        {% if price_drops_count > 0 %}
        <mj-section background-color="#dcfce7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="16px" font-weight="bold" color="#065f46">
              🔥 {{ price_drops_count }} Снижение цены {{ price_drops_count|pluralize }} на этой неделе!
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="15px" />
        {% endif %}

        {% if back_in_stock_count > 0 %}
        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="16px" font-weight="bold" color="#059669">
              ✓ {{ back_in_stock_count }} Товар {{ back_in_stock_count|pluralize }} снова в наличии
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
              <span style="text-decoration: line-through; color: #9ca3af;"">{{ item.old_price }}</span>
              <span style="color: #059669; font-weight: bold;""> {{ item.new_price }}</span>
            </mj-text>
            {% else %}
            <mj-text font-size="15px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}">
              {{ item.price }}
            </mj-text>
            {% endif %}
            {% if not item.in_stock %}
            <mj-text font-size="13px" color="#dc2626">
              Нет в наличии
            </mj-text>
            {% endif %}
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-button href="{{ wishlist_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Просмотреть полный список желаний
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Не хотите получать напоминания еженедельно? <a href="{{ unsubscribe_url }}">Отписаться</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❤️ ВАШ СПИСОК ЖЕЛАНИЙ

Здравствуйте, {{ customer_name }},

У вас {{ wishlist_item_count }} товар{{ wishlist_item_count|pluralize }} в списке желаний. Вот что произошло:

{% if price_drops_count > 0 %}🔥 {{ price_drops_count }} Снижение цены {{ price_drops_count|pluralize }} на этой неделе!{% endif %}
{% if back_in_stock_count > 0 %}✓ {{ back_in_stock_count }} Товар {{ back_in_stock_count|pluralize }} снова в наличии{% endif %}

ВАШ СПИСОК ЖЕЛАНИЙ:
{% for item in wishlist_items %}
- {{ item.product_name }}
  {% if item.price_dropped %}Было {{ item.old_price }}, Теперь {{ item.new_price }}{% else %}{{ item.price }}{% endif %}
  {% if not item.in_stock %}Нет в наличии{% endif %}
{% endfor %}

Просмотреть полный список желаний: {{ wishlist_url }}

Не хотите получать напоминания еженедельно? Отписаться: {{ unsubscribe_url }}