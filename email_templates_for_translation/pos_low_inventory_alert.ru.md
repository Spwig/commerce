---
template_type: pos_low_inventory_alert
category: POS
---

# Email Template: pos_low_inventory_alert

## Subject
📦 Оповещение о низком запасе: {{ product_count }} товар{{ product_count|pluralize }} с низким запасом на {{ location_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          📦 Оповещение о низком запасе
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Низкий запас
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ product_count }} товар{{ product_count|pluralize }} {{ product_count|pluralize:'is,are' }} с низким запасом на {{ location_name }}.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Детали оповещения:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Местоположение:</strong> {{ location_name }}<br/>
              <strong>Пострадавшие товары:</strong> {{ product_count }}<br/>
              <strong>Обнаружено:</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Товары с низким запасом:
        </mj-text>

        {% for item in low_stock_items %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ item.product_name }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              {% if item.variant_name %}<strong>Вариант:</strong> {{ item.variant_name }}<br/>{% endif %}
              <strong>Текущий запас:</strong> <span style="color: #dc2626; font-weight: bold;">{{ item.current_stock }}</span><br/>
              <strong>Точка заказа:</strong> {{ item.reorder_point }}<br/>
              <strong>SKU:</strong> {{ item.sku }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Рекомендуемые действия:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • Создать заказы на приобретение для товаров с низким запасом<br/>
          • Перенести запасы с других местоположений<br/>
          • Обновить точки заказа при необходимости<br/>
          • Рассмотреть возможность корректировки уровней запасов
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ inventory_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Просмотр запасов
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ purchase_orders_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Создать заказ на приобретение
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📦 ОПОВЕЩЕНИЕ О НИЗКОМ ЗАПАСЕ

Низкий запас

{{ product_count }} товар{{ product_count|pluralize }} {{ product_count|pluralize:'is,are' }} с низким запасом на {{ location_name }}.

ДЕТАЛИ ОПОВЕЩЕНИЯ:
- Местоположение: {{ location_name }}
- Пострадавшие товары: {{ product_count }}
- Обнаружено: {{ detected_at }}

ТОВАРЫ С НИЗКИМ ЗАПАСОМ:
{% for item in low_stock_items %}
{{ item.product_name }}
{% if item.variant_name %}Вариант: {{ item.variant_name }}{% endif %}
Текущий запас: {{ item.current_stock }}
Точка заказа: {{ item.reorder_point }}
SKU: {{ item.sku }}

{% endfor %}

РЕКОМЕНДУЕМЫЕ ДЕЙСТВИЯ:
• Создать заказы на приобретение для товаров с низким запасом
• Перенести запасы с других местоположений
• Обновить точки заказа при необходимости
• Рассмотреть возможность корректировки уровней запасов

Просмотр запасов: {{ inventory_url }}
Создать заказ на приобретение: {{ purchase_orders_url }}