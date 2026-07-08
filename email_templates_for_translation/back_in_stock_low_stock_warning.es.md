---
template_type: back_in_stock_low_stock_warning
category: Stock Notifications
---

# Email Template: back_in_stock_low_stock_warning

## Subject
⚠️ {{ product_name }} está de vuelta pero ¡se agota rápido! - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Stock limitado - ¡Actúa rápido!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          {{ product_name }} está de vuelta en stock!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hola {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          ¡Buena noticia! El producto que estabas esperando está de vuelta en stock. ¡Pero date prisa! Solo tenemos {{ stock_remaining }} unidad{{ stock_remaining|pluralize }} left!
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
            <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
              {{ product_description }}
            </mj-text>
            <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}">
              {{ product_price }}
            </mj-text>
            {% if variant_name %}
            <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
              Variante: {{ variant_name }}
            </mj-text>
            {% endif %}
            <mj-spacer height="10px" />
            <mj-text font-size="14px" color="#dc2626" font-weight="bold">
              ⚠️ Solo {{ stock_remaining }} left in stock!
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ product_url }}" background-color="#dc2626" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          Compra ahora antes de que se agote
        </mj-button>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#991b1b" align="center">
              🔥 <strong>Este producto se agotó {{ times_sold_out }} vez{{ times_sold_out|pluralize }} en el último mes!</strong><br/>
              ¡No te pierdas de nuevo! - ordene ahora mientras haya existencias.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          ¿Ya no estás interesado? <a href="{{ unsubscribe_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Desuscribirse de esta notificación</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ STOCK LIMITADO - ACTÚA RÁPIDO!

{{ product_name }} está de vuelta en stock!

Hola {{ customer_name }},

¡Buena noticia! El producto que estabas esperando está de vuelta en stock. ¡Pero date prisa! Solo tenemos {{ stock_remaining }} unidad{{ stock_remaining|pluralize }} left!

PRODUCTO:
{{ product_name }}
{{ product_description }}
Precio: {{ product_price }}
{% if variant_name %}Variante: {{ variant_name }}{% endif %}

⚠️ SOLO {{ stock_remaining }} RESTANTE EN STOCK!

Compra ahora antes de que se agote: {{ product_url }}

🔥 Este producto se agotó {{ times_sold_out }} vez{{ times_sold_out|pluralize }} en el último mes!
¡No te pierdas de nuevo! - ordene ahora mientras haya existencias.

¿Ya no estás interesado? Desuscribirse: {{ unsubscribe_url }}