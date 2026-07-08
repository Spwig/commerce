---
template_type: wishlist_low_stock_warning
category: Wishlist
---

# Email Template: wishlist_low_stock_warning

## Subject
⚠️ Affrettati! {{ product_name }} sta vendendo velocemente - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Alert di basso stock!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Agisci velocemente, {{ customer_name }}!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Un prodotto nella tua lista dei desideri sta per esaurirsi. Solo {{ stock_remaining }} unit{{ stock_remaining|pluralize }} rimaste - ordina ora prima che scompaia!
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
              ⚠️ Solo {{ stock_remaining }} rimaste in stock!
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ product_url }}" background-color="#dc2626" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          Acquista Prima Che Scompaia
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ ALERT DI BASSO STOCK!

Agisci velocemente, {{ customer_name }}!

Un prodotto nella tua lista dei desideri sta per esaurirsi. Solo {{ stock_remaining }} unit{{ stock_remaining|pluralize }} rimaste - ordina ora prima che scompaia!

{{ product_name }}
Prezzo: {{ product_price }}
⚠️ Solo {{ stock_remaining }} rimaste in stock!

Acquista prima che scompaia: {{ product_url }}