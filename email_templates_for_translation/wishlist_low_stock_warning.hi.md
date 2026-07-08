---
template_type: wishlist_low_stock_warning
category: Wishlist
---

# Email Template: wishlist_low_stock_warning

## Subject
⚠️ जल्दी करें! {{ product_name }} तेजी से बिक रहा है - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ कम स्टॉक चेतावनी!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          जल्दी करें, {{ customer_name }}!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          आपकी विशिष्ट सूची पर एक उत्पाद कम हो रहा है। केवल {{ stock_remaining }} इकाई{{ stock_remaining|pluralize }} बची हुई हैं - अब ऑर्डर करें ताकि यह नहीं खत्म हो जाए!
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
              ⚠️ केवल {{ stock_remaining }} स्टॉक में बचे हुए हैं!
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ product_url }}" background-color="#dc2626" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          खत्म होने से पहले खरीदें
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ कम स्टॉक चेतावनी!

जल्दी करें, {{ customer_name }}!

आपकी विशिष्ट सूची पर एक उत्पाद कम हो रहा है। केवल {{ stock_remaining }} इकाई{{ stock_remaining|pluralize }} बची हुई हैं - अब ऑर्डर करें ताकि यह नहीं खत्म हो जाए!

{{ product_name }}
मूल्य: {{ product_price }}
⚠️ केवल {{ stock_remaining }} स्टॉक में बचे हुए हैं!

खत्म होने से पहले खरीदें: {{ product_url }}