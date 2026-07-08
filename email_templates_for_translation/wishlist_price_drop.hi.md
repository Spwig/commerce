---
template_type: wishlist_price_drop
category: Wishlist
---

# Email Template: wishlist_price_drop

## Subject
🔥 कीमत में गिरावट की चेतावनी: {{ product_name }} अब {{ discount_percentage }}% छूट पर है!

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          🔥 कीमत में गिरावट की चेतावनी!
        </mj-text>
        <mj-text font-size="18px" color="#047857" align="center">
          अपनी विश्लेषण सूची आइटम पर {{ discount_percentage }}% बचाएं
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          अच्छ खबर, {{ customer_name }}!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          आपकी विश्लेषण सूची पर एक उत्पाद की कीमत अब घट गई है! बचाने के इस अवसर को छोड़ न दें।
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
          अब खरीदें और {{ discount_percentage }}% बचाएं
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#991b1b" align="center">
              ⏰ <strong>Limited Time:</strong> यह बिक्री हमेशा नहीं रहेगी। कीमतें किसी भी समय बढ़ सकती हैं!
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          विश्लेषण सूची से हटाएं: <a href="{{ remove_wishlist_url }}">यहां क्लिक करें</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🔥 कीमत में गिरावट की चेतावनी!
बचाएं {{ discount_percentage }}% अपनी विश्लेषण सूची आइटम पर

अच्छ खबर, {{ customer_name }}!

आपकी विश्लेषण सूची पर एक उत्पाद की कीमत अब घट गई है! बचाने के इस अवसर को छोड़ न दें।

{{ product_name }}
Was: {{ original_price }}
NOW: {{ new_price }}
SAVE {{ savings_amount }} ({{ discount_percentage }}% OFF)

अब खरीदें और {{ discount_percentage }}% बचाएं: {{ product_url }}

⏰ सीमित समय: यह बिक्री हमेशा नहीं रहेगी। कीमतें किसी भी समय बढ़ सकती हैं!

विश्लेषण सूची से हटाएं: {{ remove_wishlist_url }}