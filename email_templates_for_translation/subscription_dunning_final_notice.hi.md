---
template_type: subscription_dunning_final_notice
category: Subscriptions
---

# Email Template: subscription_dunning_final_notice

## Subject
⚠️ अंतिम सूचना: आपका सदस्यता {{ days_until_cancellation }} दिन में रद्द कर दी जाएगी

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#991b1b" align="center">
          ⚠️ अंतिम सूचना
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          सदस्यता रद्द होने वाली है
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          हेलो {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          यह आपकी अंतिम सूचना है। हम आपकी {{ plan_name }} सदस्यता के लिए भुगतान प्रक्रिया करने में असमर्थ रहे हैं। यदि हमें {{ days_until_cancellation }} दिनों के भीतर भुगतान नहीं मिलता है, तो आपकी सदस्यता रद्द कर दी जाएगी।
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b" font-size="16px">
              ⚠️ भुगतान विफल - कार्रवाई आवश्यक है
            </mj-text>
            <mj-text color="#991b1b">
              <strong>सदस्यता:</strong> {{ plan_name }}<br/>
              <strong>कर जोड़ा गया है:</strong> {{ amount_due }}<br/>
              <strong>असफल प्रयास:</strong> {{ retry_count }}<br/>
              <strong>अंतिम प्रयास:</strong> {{ last_retry_date }}<br/>
              <strong>रद्द करने की तारीख:</strong> <span style="font-weight: bold; font-size: 16px;">{{ cancellation_date }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          भुगतान त्रुटि:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" font-family="monospace" color="{{ theme.color.text|default:'#4b5563' }}">
              {{ payment_error_message }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          क्या होगा:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          यदि {{ cancellation_date }} तक भुगतान नहीं प्राप्त किया गया:
          <br/>
          • आपकी सदस्यता रद्द कर दी जाएगी
          <br/>
          • आप सभी सदस्यता लाभों के लिए पहले अधिग्रहण खो देंगे
          <br/>
          • आपके डेटा को हटा दिया जा सकता है (अवधि नीति देखें)
          <br/>
          • आपको पहले अधिग्रहण बहाल करने के लिए फिर से सदस्यता लेने की आवश्यकता होगी
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          अब अपने भुगतान विधि को अपडेट करें
        </mj-text>

        <mj-spacer height="20px" />

        <mj-button href="{{ update_payment_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          भुगतान विधि को अपडेट करें
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          सामान्य समस्याएं और समाधान:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • <strong>कार्ड अमूल्य:</strong> वर्तमान क्रेडिट कार्ड के साथ अपडेट करें
          <br/>
          • <strong>अपर्याप्त धन राशि:</strong> पर्याप्त शेष राशि सुनिश्चित करें
          <br/>
          • <strong>कार्ड अस्वीकृत:</strong> अपने बैंक से संपर्क करें या अलग कार्ड का उपयोग करें
          <br/>
          • <strong>पता असंगतता:</strong> बिलिंग पता कार्ड के साथ मेल खाता है कि सत्यापित करें
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" font-weight="bold">
              सहायता की आवश्यकता है?
            </mj-text>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              यदि आप भुगतान समस्याओं का अनुभव कर रहे हैं या सहायता की आवश्यकता है, कृपया तुरंत हमारे समर्थन टीम से संपर्क करें।
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          समर्थन से संपर्क करें
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          यदि आप अपनी सदस्यता को रद्द करना चाहते हैं, तो आप अपने खाता सेटिंग में ऐसा कर सकते हैं।
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ अंतिम सूचना

सदस्यता रद्द होने वाली है

हेलो {{ customer_name }},

यह आपकी अंतिम सूचना है। हम आपकी {{ plan_name }} सदस्यता के लिए भुगतान प्रक्रिया करने में असमर्थ रहे हैं। यदि हमें {{ days_until_cancellation }} दिनों के भीतर भुगतान नहीं मिलता है, तो आपकी सदस्यता रद्द कर दी जाएगी।

⚠️ भुगतान विफल - कार्रवाई आवश्यक है:
- सदस्यता: {{ plan_name }}
- कर जोड़ा गया है: {{ amount_due }}
- असफल प्रयास: {{ retry_count }}
- अंतिम प्रयास: {{ last_retry_date }}
- रद्द करने की तारीख: {{ cancellation_date }}

भुगतान त्रुटि:
{{ payment_error_message }}

क्या होगा:
यदि {{ cancellation_date }} तक भुगतान नहीं प्राप्त किया गया:
• आपकी सदस्यता रद्द कर दी जाएगी
• आप सभी सदस्यता लाभों के लिए पहले अधिग्रहण खो देंगे
• आपके डेटा को हटा दिया जा सकता है (अवधि नीति देखें)
• आपको पहले अधिग्रहण बहाल करने के लिए फिर से सदस्यता लेने की आवश्यकता होगी

अब अपने भुगतान विधि को अपडेट करें

सामान्य समस्याएं और समाधान:
• कार्ड अमूल्य: वर्तमान क्रेडिट कार्ड के साथ अपडेट करें
• अपर्याप्त धन राशि: पर्याप्त शेष राशि सुनिश्चित करें
• कार्ड अस्वीकृत: अपने बैंक से संपर्क करें या अलग कार्ड का उपयोग करें
• पता असंगतता: बिलिंग पता कार्ड के साथ मेल खाता है कि सत्यापित करें

सहायता की आवश्यकता है?
यदि आप भुगतान समस्याओं का अनुभव कर रहे हैं या सहायता की आवश्यकता है, कृपया तुरंत हमारे समर्थन टीम से संपर्क करें।

अपडेट भुगतान विधि: {{ update_payment_url }}
समर्थन से संपर्क करें: {{ support_url }}

यदि आप अपनी सदस्यता को रद्द करना चाहते हैं, तो आप अपने खाता सेटिंग में ऐसा कर सकते हैं।
