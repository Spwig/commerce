---
template_type: cart_recovered_thank_you
category: Cart Recovery
---

# Email Template: cart_recovered_thank_you

## Subject
आपके ऑर्डर #{{ order_number }} के लिए धन्यवाद! - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          🎉 आपके ऑर्डर के लिए धन्यवाद!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          हेलो {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          हम आपके खरीदारी पूरी करने के लिए खुश हैं! आपका ऑर्डर पुष्टि कर दिया गया है और हम इसे भेजने के लिए तैयार कर रहे हैं।
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              ऑर्डर समारोह
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>ऑर्डर संख्या:</strong> {{ order_number }}<br/>
              <strong>ऑर्डर तिथि:</strong> {{ order_date }}<br/>
              <strong>कुल:</strong> {{ order_total }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ order_tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          अपने ऑर्डर की प्रगति देखें
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          अगला क्या होगा?
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. हम आपके ऑर्डर की तैयारी करेंगे (आमतौर पर 1-2 व्यावसायिक दिनों के भीतर)<br/>
          2. आप ट्रैकिंग जानकारी के साथ एक शिपमेंट पुष्टि प्राप्त करेंगे<br/>
          3. आपका ऑर्डर इस पते पर डिलीवर किया जाएगा: {{ shipping_address }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              💡 <strong>क्या आप जानते हैं?</strong><br/>
              आप अपने खाते के डैशबोर्ड में कभी भी अपने ऑर्डर की प्रगति देख सकते हैं।
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          सवाल हैं? <a href="{{ support_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">हमारी समर्थन टीम से संपर्क करें</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎉 आपके ऑर्डर के लिए धन्यवाद!

हेलो {{ customer_name }},

हम आपके खरीदारी पूरी करने के लिए खुश हैं! आपका ऑर्डर पुष्टि कर दिया गया है और हम इसे भेजने के लिए तैयार कर रहे हैं।

ऑर्डर समारोह:
- ऑर्डर संख्या: {{ order_number }}
- ऑर्डर तिथि: {{ order_date }}
- कुल: {{ order_total }}

अपने ऑर्डर की प्रगति देखें: {{ order_tracking_url }}

अगला क्या होगा?
1. हम आपके ऑर्डर की तैयारी करेंगे (आमतौर पर 1-2 व्यावसायिक दिनों के भीतर)
2. आप ट्रैकिंग जानकारी के साथ एक शिपमेंट पुष्टि प्राप्त करेंगे
3. आपका ऑर्डर इस पते पर डिलीवर किया जाएगा: {{ shipping_address }}

💡 क्या आप जानते हैं?
आप अपने खाते के डैशबोर्ड में कभी भी अपने ऑर्डर की प्रगति देख सकते हैं।

सवाल हैं? हमारी समर्थन टीम से संपर्क करें: {{ support_url }}

---
ऑर्डर #{{ order_number }} के {{ shop_name }} पर