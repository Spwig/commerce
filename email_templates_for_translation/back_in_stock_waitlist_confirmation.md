---
template_type: back_in_stock_waitlist_confirmation
category: Stock Notifications
---

# Email Template: back_in_stock_waitlist_confirmation

## Subject
✓ You're on the waitlist for {{ product_name }} - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ✓ You're on the Waitlist!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Thanks for signing up! We'll notify you as soon as this product is back in stock.
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
            <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}">
              {{ product_price }}
            </mj-text>
            {% if variant_name %}
            <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
              Variant: {{ variant_name }}
            </mj-text>
            {% endif %}
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              💡 <strong>What to expect:</strong><br/>
              We'll email you the moment this item is restocked. Stock is limited, so act fast when you get notified!
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          While You Wait...
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Check out these similar products that are in stock now:
        </mj-text>

        {% for product in similar_products %}
        <mj-spacer height="10px" />
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="4px" padding="12px">
          <mj-column width="25%">
            <mj-image src="{{ product.image }}" alt="{{ product.name }}" border-radius="4px" />
          </mj-column>
          <mj-column width="75%">
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ product.name }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.primary|default:'#2563eb' }}">
              {{ product.price }}
            </mj-text>
            <mj-text font-size="13px">
              <a href="{{ product.url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">View Product →</a>
            </mj-text>
          </mj-column>
        </mj-section>
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Changed your mind? <a href="{{ unsubscribe_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Unsubscribe from this waitlist</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ YOU'RE ON THE WAITLIST!

Hi {{ customer_name }},

Thanks for signing up! We'll notify you as soon as this product is back in stock.

PRODUCT:
{{ product_name }}
{{ product_description }}
Price: {{ product_price }}
{% if variant_name %}Variant: {{ variant_name }}{% endif %}

💡 WHAT TO EXPECT:
We'll email you the moment this item is restocked. Stock is limited, so act fast when you get notified!

WHILE YOU WAIT...
Check out these similar products that are in stock now:
{% for product in similar_products %}
- {{ product.name }} - {{ product.price }}
  {{ product.url }}
{% endfor %}

Changed your mind? Unsubscribe from this waitlist: {{ unsubscribe_url }}

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| customer_name | Customer's first name | Emma |
| product_name | Product name | Classic Cotton T-Shirt |
| product_description | Short description | Soft, breathable 100% organic cotton |
| product_price | Price | $29.99 |
| product_image | Product image URL | https://shop.com/media/products/tshirt.jpg |
| variant_name | Optional variant | Size: M, Color: Navy |
| similar_products | List of alternatives | [{name, price, image, url}] |
| unsubscribe_url | Waitlist unsub link | https://shop.com/en/waitlist/unsubscribe/ABC123 |
| shop_name | Store name | Amazing Shop |

## Notes

- Confirmation email after waitlist signup
- Marketing email - respects communication preferences
- Includes cross-sell opportunities (similar products)
- Manages expectations about notification
- Provides unsubscribe option
- Sent immediately after signup
