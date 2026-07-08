---
template_type: wishlist_item_added_confirmation
category: Wishlist
---

# Email Template: wishlist_item_added_confirmation

## Subject
✓ {{ product_name }} को आपके विश्लेषण सूची में जोड़ दिया गया - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ❤️ आपकी विश्लेषण सूची में जोड़ दिया गया!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          हेलो {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          आपने सफलतापूर्वक {{ product_name }} को अपनी विश्लेषण सूची में जोड़ दिया। हम इसकी निगरानी करेंगे!
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
              ✓ उपलब्ध
            </mj-text>
            {% else %}
            <mj-text font-size="13px" color="#dc2626">
              ⚠️ बाहर उपलब्ध - जब यह वापस आएगा तो हम आपको सूचना देंगे!
            </mj-text>
            {% endif %}
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              💡 <strong>हम आपको इसके बारे में सूचना देंगे:</strong><br/>
              • कीमत कम हो जाएगा<br/>
              • वापस उपलब्ध होने की सूचना<br/>
              • सीमित समय की बिक्री
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ wishlist_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          अपनी विश्लेषण सूची देखें
        </mj-button>

        {% if product_in_stock %}
        <mj-spacer height="10px" />
        <mj-button href="{{ product_url }}" background-color="#059669" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          अब खरीदें
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❤️ आपकी विश्लेषण सूची में जोड़ दिया गया!

हेलो {{ customer_name }},

आपने सफलतापूर्वक {{ product_name }} को अपनी विश्लेषण सूची में जोड़ दिया। हम इसकी निगरानी करेंगे!

{{ product_name }}
कीमत: {{ product_price }}
{% if product_in_stock %}✓ उपलब्ध{% else %}⚠️ बाहर उपलब्ध - जब यह वापस आएगा तो हम आपको सूचना देंगे!{% endif %}

💡 हम आपको इसके बारे में सूचना देंगे:
• कीमत कम हो जाएगा
• वापस उपलब्ध होने की सूचना
• सीमित समय की बिक्री

अपनी विश्लेषण सूची देखें: {{ wishlist_url }}
{% if product_in_stock %}अब खरीदें: {{ product_url }}{% endif %}