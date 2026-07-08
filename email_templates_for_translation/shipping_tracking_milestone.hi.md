---
template_type: shipping_tracking_milestone
category: Shipping
---

# Email Template: shipping_tracking_milestone

## Subject
आपका ऑर्डर #{{ order_number }} {{ milestone_status }} है - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          डिलीवरी अपडेट: {{ milestone_status }}
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          हे {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          अच्छी खबर! आपका ऑर्डर आपके लिए अपनी यात्रा में एक महत्वपूर्ण मील के पत्थर तक पहुंच गया है।
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
              📦 {{ milestone_status }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
              {{ milestone_description }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              ऑर्डर विवरण:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>ऑर्डर संख्या:</strong> {{ order_number }}<br/>
              <strong>ट्रैकिंग संख्या:</strong> {{ tracking_number }}<br/>
              <strong>वाहक:</strong> {{ carrier_name }}<br/>
              <strong>वर्तमान स्थान:</strong> {{ current_location }}<br/>
              <strong>अनुमानित डिलीवरी:</strong> {{ estimated_delivery }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          अपना पैकेज ट्रैक करें
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          अपनी डिलीवरी के बारे में सवाल? <a href="{{ support_url }}">समर्थन से संपर्क करें</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
डिलीवरी अपडेट: {{ milestone_status }}

हे {{ customer_name }},

अच्छी खबर! आपका ऑर्डर आपके लिए अपनी यात्रा में एक महत्वपूर्ण मील के पत्थर तक पहुंच गया है।

📦 {{ milestone_status }}
{{ milestone_description }}

ऑर्डर विवरण:
- ऑर्डर संख्या: {{ order_number }}
- ट्रैकिंग संख्या: {{ tracking_number }}
- वाहक: {{ carrier_name }}
- वर्तमान स्थान: {{ current_location }}
- अनुमानित डिलीवरी: {{ estimated_delivery }}

अपना पैकेज ट्रैक करें: {{ tracking_url }}

अपनी डिलीवरी के बारे में सवाल? समर्थन से संपर्क करें: {{ support_url }}