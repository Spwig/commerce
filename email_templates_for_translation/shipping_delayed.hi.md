---
template_type: shipping_delayed
category: Shipping
---

# Email Template: shipping_delayed

## Subject
आपके ऑर्डर #{{ order_number }} के बारे में अपडेट - डिलीवरी डिलेड

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          आपके ऑर्डर के बारे में अपडेट
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          हेलो {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          हम आपको अपने ऑर्डर के संबंध में एक डिलेड के बारे में बताना चाहते हैं। हम आपके असुविधा के लिए क्षमा चाहते हैं और आपकी धैर्य के लिए धन्यवाद करते हैं।
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              ऑर्डर विवरण:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>ऑर्डर संख्या:</strong> {{ order_number }}<br/>
              <strong>मूल एटीई:</strong> {{ original_delivery_date }}<br/>
              <strong>नई एटीई:</strong> {{ new_delivery_date }}<br/>
              <strong>ट्रैकिंग संख्या:</strong> {{ tracking_number }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          डिलेड का कारण:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ delay_reason }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          अपने ऑर्डर को ट्रैक करें
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          हम आपके ऑर्डर को आपके पास जल्द से जल्द पहुँचाने के लिए कड़ी मेहनत कर रहे हैं। जब आपका पैकेट रास्ते में होगा, तो आपको एक अन्य अपडेट मिलेगा।
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          प्रश्न हैं? <a href="{{ support_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">हमारे ग्राहक सेवा टीम से संपर्क करें</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
आपके ऑर्डर #{{ order_number }} के बारे में अपडेट

हेलो {{ customer_name }},

हम आपको अपने ऑर्डर के संबंध में एक डिलेड के बारे में बताना चाहते हैं। हम आपके असुविधा के लिए क्षमा चाहते हैं और आपकी धैर्य के लिए धन्यवाद करते हैं।

ऑर्डर विवरण:
- ऑर्डर संख्या: {{ order_number }}
- मूल एटीई: {{ original_delivery_date }}
- नई एटीई: {{ new_delivery_date }}
- ट्रैकिंग संख्या: {{ tracking_number }}

डिलेड का कारण:
{{ delay_reason }}

अपने ऑर्डर को ट्रैक करें: {{ tracking_url }}

हम आपके ऑर्डर को आपके पास जल्द से जल्द पहुँचाने के लिए कड़ी मेहनत कर रहे हैं। जब आपका पैकेट रास्ते में होगा, तो आपको एक अन्य अपडेट मिलेगा।

प्रश्न हैं? हमारे ग्राहक सेवा टीम से संपर्क करें: {{ support_url }}

---
यह अपडेट {{ shop_name }} पर ऑर्डर #{{ order_number }} के लिए है।