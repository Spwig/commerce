---
template_type: pos_terminal_offline
category: POS
---

# Email Template: pos_terminal_offline

## Subject
⚠️ POS टर्मिनल ऑफ़लाइन: {{ terminal_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#991b1b" align="center">
          ⚠️ टर्मिनल अनुबंधित नहीं
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          POS टर्मिनल ऑफ़लाइन
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ terminal_name }} ऑफ़लाइन हो गया है और अब उत्तर नहीं दे रहा है।
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              टर्मिनल जानकारी:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>टर्मिनल:</strong> {{ terminal_name }}<br/>
              <strong>स्थान:</strong> {{ location }}<br/>
              <strong>अंतिम दृश्य:</strong> {{ last_seen }}<br/>
              <strong>ऑफ़लाइन से:</strong> {{ offline_since }}<br/>
              <strong>अवधि:</strong> {{ offline_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          सामान्य कारण:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • नेटवर्क कनेक्टिविटी समस्याएं<br/>
          • टर्मिनल बंद या पुनः शुरू कर दिया गया<br/>
          • सॉफ्टवेयर क्रैश या जमा<br/>
          • इंटरनेट सेवा बंदी
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          सिफारिश की गई कार्रवाई:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. टर्मिनल की शक्ति और नेटवर्क कनेक्शन की जांच करें<br/>
          2. टर्मिनल उपकरण को पुनः शुरू करें<br/>
          3. इंटरनेट कनेक्टिविटी की पुष्टि करें<br/>
          4. फायरवॉल और सुरक्षा सेटिंग्स की जांच करें
        </mj-text>

        {% if active_shift %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ सक्रिय शिफ्ट चेतावनी
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              इस टर्मिनल में एक सक्रिय शिफ्ट है। टर्मिनल के पुनः जोड़े जाने तक बिक्री डेटा सिंक नहीं किया जा सकता।
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_terminals_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          टर्मिनल स्थिति के बारे में देखें
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          टर्मिनल पुनः जुड़ते हैं जब आप एक अन्य सूचना प्राप्त करेंगे।
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ टर्मिनल अनुबंधित नहीं

POS टर्मिनल ऑफ़लाइन

{{ terminal_name }} ऑफ़लाइन हो गया है और अब उत्तर नहीं दे रहा है।

टर्मिनल जानकारी:
- टर्मिनल: {{ terminal_name }}
- स्थान: {{ location }}
- अंतिम दृश्य: {{ last_seen }}
- ऑफ़लाइन से: {{ offline_since }}
- अवधि: {{ offline_duration }}

सामान्य कारण:
• नेटवर्क कनेक्टिविटी समस्याएं
• टर्मिनल बंद या पुनः शुरू कर दिया गया
• सॉफ्टवेयर क्रैश या जमा
• इंटरनेट सेवा बंदी

सिफारिश की गई कार्रवाई:
1. टर्मिनल की शक्ति और नेटवर्क कनेक्शन की जांच करें
2. टर्मिनल उपकरण को पुनः शुरू करें
3. इंटरनेट कनेक्टिविटी की पुष्टि करें
4. फायरवॉल और सुरक्षा सेटिंग्स की जांच करें

{% if active_shift %}
⚠️ सक्रिय शिफ्ट चेतावनी:
इस टर्मिनल में एक सक्रिय शिफ्ट है। टर्मिनल के पुनः जोड़े जाने तक बिक्री डेटा सिंक नहीं किया जा सकता।
{% endif %}

टर्मिनल स्थिति के बारे में देखें: {{ admin_terminals_url }}

आप टर्मिनल के पुनः जोड़े जाने पर एक अन्य सूचना प्राप्त करेंगे।
