---
template_type: delivery_confirmation
category: Core E-commerce
---

# Email Template: delivery_confirmation

## Subject
आदेश स्थानांतरित - आदेश #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          आदेश स्थानांतरित
        </mj-text>
        <mj-text>
          आपका आदेश #{{ order_number }} डिलीवर कर दिया गया है!
        </mj-text>
        <mj-text>
          हम आशा करते हैं कि आप अपनी खरीदारी का आनंद ले रहे हैं। अगर आपके कोई प्रश्न या चिंताएं हैं, तो कृपया हमसे संपर्क करने में संकोच न करें।
        </mj-text>
        <mj-button href="{{ order_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          ऑर्डर देखें
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
आदेश स्थानांतरित

आपका आदेश #{{ order_number }} डिलीवर कर दिया गया है!

हम आशा करते हैं कि आप अपनी खरीदारी का आनंद ले रहे हैं। अगर आपके कोई प्रश्न या चिंताएं हैं, तो कृपया हमसे संपर्क करने में संकोच न करें।

ऑर्डर देखें: {{ order_url }}