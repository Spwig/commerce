---
template_type: return_received
category: Returns
---

# Email Template: return_received

## Subject
हमने आपके रिटर्न को प्राप्त कर लिया - ऑर्डर #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#eff6ff' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.primary|default:'#1d4ed8' }}">
          रिटर्न प्राप्त
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.primary|default:'#1d4ed8' }}">
          ऑर्डर #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          हेलो {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          हमने आपके द्वारा लौटाए गए ऑर्डर <strong>#{{ order_number }}</strong> के लिए आइटम प्राप्त कर लिए हैं।
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>अगला क्या होता है:</strong>
        </mj-text>

        <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
          1. हमारी टीम 2-3 व्यावसायिक दिनों के भीतर रिटर्न किए गए आइटम की जांच करेगी<br/>
          2. हम आइटम की मूल स्थिति की पुष्टि करेंगे<br/>
          3. जांच पूर्ण होने के बाद, हम आपके रिफंड को प्रक्रिया में लाएंगे<br/>
          4. रिफंड प्रक्रिया में एक बार आपको एक पुष्टि ईमेल मिलेगा
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          रिफंड आपके मूल भुगतान विधि में क्रेडिट किया जाएगा और आपके खाते में दिखाई देने में 5-10 व्यावसायिक दिन लग सकते हैं।
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          आपके धैर्य के लिए धन्यवाद!
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
रिटर्न प्राप्त - ऑर्डर #{{ order_number }}

हेलो {{ customer_name }},

हमने आपके द्वारा लौटाए गए ऑर्डर #{{ order_number }} के लिए आइटम प्राप्त कर लिए हैं।

अगला क्या होता है:
1. हमारी टीम 2-3 व्यावसायिक दिनों के भीतर रिटर्न किए गए आइटम की जांच करेगी
2. हम आइटम की मूल स्थिति की पुष्टि करेंगे
3. जांच पूर्ण होने के बाद, हम आपके रिफंड को प्रक्रिया में लाएंगे
4. रिफंड प्रक्रिया में एक बार आपको एक पुष्टि ईमेल मिलेगा

रिफंड आपके मूल भुगतान विधि में क्रेडिट किया जाएगा और आपके खाते में दिखाई देने में 5-10 व्यावसायिक दिन लग सकते हैं।

आपके धैर्य के लिए धन्यवाद!