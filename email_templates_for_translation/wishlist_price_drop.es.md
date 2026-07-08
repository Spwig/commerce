---
template_type: wishlist_price_drop
category: Wishlist
---

# Email Template: wishlist_price_drop

## Subject
🔥 ¡Alerta de Descuento: {{ product_name }} ahora tiene {{ discount_percentage }}% de descuento!

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          🔥 ¡Alerta de Descuento!
        </mj-text>
        <mj-text font-size="18px" color="#047857" align="center">
          Ahorra {{ discount_percentage }}% en tu artículo de la lista de deseos
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ¡Buena noticia, {{ customer_name }}!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Un producto de tu lista de deseos acaba de reducir su precio. ¡No te lo pierdas!
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
            <mj-spacer height="10px" />
            <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
              Was: <span style="text-decoration: line-through;">{{ original_price }}</span>
            </mj-text>
            <mj-text font-size="24px" font-weight="bold" color="#059669">
              Now: {{ new_price }}
            </mj-text>
            <mj-text font-size="16px" font-weight="bold" color="#dc2626">
              Save {{ savings_amount }} ({{ discount_percentage }}% OFF)
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ product_url }}" background-color="#059669" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          Comprar ahora y ahorrar {{ discount_percentage }}%
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#991b1b" align="center">
              ⏰ <strong>Limited Time:</strong> This sale won't last forever. Prices may go back up at any time!
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Remove from wishlist: <a href="{{ remove_wishlist_url }}">Click here</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🔥 ¡ALERTA DE REDUCCIÓN DE PRECIO!
Ahorra {{ discount_percentage }}% en tu artículo de la lista de deseos

¡Buena noticia, {{ customer_name }}!

Un producto de tu lista de deseos acaba de reducir su precio. ¡No te lo pierdas!

{{ product_name }}
Was: {{ original_price }}
NOW: {{ new_price }}
SAVE {{ savings_amount }} ({{ discount_percentage }}% OFF)

Comprar ahora y ahorrar {{ discount_percentage }}%: {{ product_url }}

⏰ TIEMPO LIMITADO: Esta venta no durará para siempre. Los precios pueden subir en cualquier momento.

Eliminar de la lista de deseos: {{ remove_wishlist_url }}