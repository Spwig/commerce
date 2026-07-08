---
template_type: wishlist_item_added_confirmation
category: Wishlist
---

# Email Template: wishlist_item_added_confirmation

## Subject
✓ {{ product_name }} añadido a tu lista de deseos - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ❤️ Añadido a tu lista de deseos!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hola {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Has añadido exitosamente {{ product_name }} a tu lista de deseos. ¡Lo mantendremos vigilado para ti!
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
              ✓ En stock
            </mj-text>
            {% else %}
            <mj-text font-size="13px" color="#dc2626">
              ⚠️ Fuera de stock - ¡Te notificaremos cuando esté disponible!
            </mj-text>
            {% endif %}
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              💡 <strong>Te notificaremos sobre:</strong><br/>
              • Descuentos de precios<br/>
              • Alertas de disponibilidad<br/>
              • Ventas con descuento limitado
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ wishlist_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Ver mi lista de deseos
        </mj-button>

        {% if product_in_stock %}
        <mj-spacer height="10px" />
        <mj-button href="{{ product_url }}" background-color="#059669" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Comprar ahora
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❤️ AÑADIDO A TU LISTA DE DESEOS!

Hola {{ customer_name }},

Has añadido exitosamente {{ product_name }} a tu lista de deseos. ¡Lo mantendremos vigilado para ti!

{{ product_name }}
Precio: {{ product_price }}
{% if product_in_stock %}✓ En stock{% else %}⚠️ Fuera de stock - ¡Te notificaremos cuando esté disponible!{% endif %}

💡 TE NOTIFICAREMOS SOBRE:
• Descuentos de precios
• Alertas de disponibilidad
• Ventas con descuento limitado

Ver mi lista de deseos: {{ wishlist_url }}
{% if product_in_stock %}Comprar ahora: {{ product_url }}{% endif %}