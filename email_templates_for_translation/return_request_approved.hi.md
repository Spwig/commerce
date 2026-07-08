---
template_type: return_request_approved
category: Returns
---

# Email Template: return_request_approved

## Subject
आपका रिटर्न स्वीकृत कर दिया गया है - आर्डर #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f0fdf4' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#166534' }}">
          रिटर्न स्वीकृत कर दिया गया है
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#166534' }}">
          आर्डर #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          हैलो {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          आपका आर्डर <strong>#{{ order_number }}</strong> के लिए रिटर्न अनुरोध स्वीकृत कर दिया गया है।
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>अगले कदम:</strong>
        </mj-text>

        <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
          1. नीचे दिए गए रिटर्न लेबल को डाउनलोड करें और प्रिंट करें<br/>
          2. यदि संभव हो तो आइटम को उनके मूल पैकेजिंग में सुरक्षित रूप से पैक करें<br/>
          3. रिटर्न लेबल को पैकेज के बाहरी भाग पर लगाएं<br/>
          4. अपने निकटतम शिपिंग स्थान पर छोड़ दें
        </mj-text>

        {% if return_label_url %}
        <mj-spacer height="20px" />
        <mj-button href="{{ return_label_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          रिटर्न लेबल डाउनलोड करें
        </mj-button>
        {% endif %}

        {% if return_tracking_number %}
        <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>रिटर्न ट्रैकिंग नंबर:</strong> {{ return_tracking_number }}
        </mj-text>
        {% endif %}

        <mj-section background-color="{{ theme.color.surface|default:'#fffbeb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#92400e' }}">
              <strong>महत्वपूर्ण:</strong> कृपया 7 दिनों के भीतर रिटर्न भेजें ताकि आपके रिफंड की त्वरित प्रक्रिया सुनिश्चित हो सके।
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          हम आपके रिटर्न को प्राप्त कर लेने और उसकी जांच कर लेने के बाद, हम आपके मूल भुगतान विधि पर आपके रिफंड को प्रक्रिया में लाएंगे।
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
रिटर्न स्वीकृत कर दिया गया है - आर्डर #{{ order_number }}

हैलो {{ customer_name }},

आपका आर्डर #{{ order_number }} के लिए रिटर्न अनुरोध स्वीकृत कर दिया गया है।

अगले कदम:
1. रिटर्न लेबल डाउनलोड करें और प्रिंट करें
2. यदि संभव हो तो आइटम को उनके मूल पैकेजिंग में सुरक्षित रूप से पैक करें
3. रिटर्न लेबल को पैकेज के बाहरी भाग पर लगाएं
4. अपने निकटतम शिपिंग स्थान पर छोड़ दें

{% if return_label_url %}रिटर्न लेबल डाउनलोड करें: {{ return_label_url }}{% endif %}
{% if return_tracking_number %}रिटर्न ट्रैकिंग नंबर: {{ return_tracking_number }}{% endif %}

महत्वपूर्ण: कृपया 7 दिनों के भीतर रिटर्न भेजें ताकि आपके रिफंड की त्वरित प्रक्रिया सुनिश्चित हो सके।

हम आपके रिटर्न को प्राप्त कर लेने और उसकी जांच कर लेने के बाद, हम आपके मूल भुगतान विधि पर आपके रिफंड को प्रक्रिया में लाएंगे।