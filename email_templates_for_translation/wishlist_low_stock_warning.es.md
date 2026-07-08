---
template_type: wishlist_low_stock_warning
category: Wishlist
---

# Email Template: wishlist_low_stock_warning

## Subject
⚠️ ¡Date prisa! {{ product_name }} se está agotando rápido - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ ¡Alerta de stock bajo!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Actúa rápido, {{ customer_name }}!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Un producto en tu lista de deseos está por agotarse. Solo quedan {{ stock_remaining }} unidad{{ stock_remaining|pluralize }} - ordena ahora antes de que se agote!
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
            <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}">
              {{ product_price }}
            </mj-text>
            <mj-text font-size="14px" color="#dc2626" font-weight="bold">
              ⚠️ Solo quedan {{ stock_remaining }} en stock!
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ product_url }}" background-color="#dc2626" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          Compra antes de que se agote
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ ALERTA DE STOCK BAJO!

Actúa rápido, {{ customer_name }}!

Un producto en tu lista de deseos está por agotarse. Solo quedan {{ stock_remaining }} unidad{{ stock_remaining|pluralize }} - ordena ahora antes de que se agote!

{{ product_name }}
Precio: {{ product_price }}
⚠️ Solo quedan {{ stock_remaining }} en stock!

Compra antes de que se agote: {{ product_url }}