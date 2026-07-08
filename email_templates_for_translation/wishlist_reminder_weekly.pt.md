---
template_type: wishlist_reminder_weekly
category: Wishlist
---

# Email Template: wishlist_reminder_weekly

## Subject
Seu lista de desejos está esperando - {{ wishlist_item_count }} itens salvos - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ❤️ Seu Lista de Desejos
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Olá {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Você tem {{ wishlist_item_count }} item{{ wishlist_item_count|pluralize }} aguardando em sua lista de desejos. Aqui está o que está acontecendo:
        </mj-text>

        <mj-spacer height="30px" />

        {% if price_drops_count > 0 %}
        <mj-section background-color="#dcfce7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="16px" font-weight="bold" color="#065f46">
              🔥 {{ price_drops_count }} Redução de Preço{{ price_drops_count|pluralize }} Esta Semana!
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="15px" />
        {% endif %}

        {% if back_in_stock_count > 0 %}
        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="16px" font-weight="bold" color="#059669">
              ✓ {{ back_in_stock_count }} Item{{ back_in_stock_count|pluralize }} Disponível Novamente
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
              Fora de Estoque
            </mj-text>
            {% endif %}
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-button href="{{ wishlist_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Ver Lista de Desejos Completa
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Não quer mais lembretes semanais? <a href="{{ unsubscribe_url }}">Cancelar Inscrição</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❤️ SEU LISTA DE DESEJOS

Olá {{ customer_name }},

Você tem {{ wishlist_item_count }} item{{ wishlist_item_count|pluralize }} aguardando em sua lista de desejos. Aqui está o que está acontecendo:

{% if price_drops_count > 0 %}🔥 {{ price_drops_count }} Redução de Preço{{ price_drops_count|pluralize }} Esta Semana!{% endif %}
{% if back_in_stock_count > 0 %}✓ {{ back_in_stock_count }} Item{{ back_in_stock_count|pluralize }} Disponível Novamente{% endif %}

SEU LISTA DE DESEJOS:
{% for item in wishlist_items %}
- {{ item.product_name }}
  {% if item.price_dropped %}Foi {{ item.old_price }}, Agora {{ item.new_price }}{% else %}{{ item.price }}{% endif %}
  {% if not item.in_stock %}Fora de Estoque{% endif %}
{% endfor %}

Ver lista de desejos completa: {{ wishlist_url }}

Não quer mais lembretes semanais? Cancelar inscrição: {{ unsubscribe_url }}