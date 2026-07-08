---
template_type: backup_failed
category: Backups
---

# Email Template: backup_failed

## Subject
🚨 आपातकालीन: बैकअप विफल - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef2f2">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#dc2626" align="center">
          ⚠️ बैकअप विफल
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#1f2937' }}">
          हेलो {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          आपके {{ shop_name }} स्टोर के लिए एक महत्वपूर्ण बैकअप संचालन विफल रहा। डेटा सुरक्षा सुनिश्चित करने के लिए तत्काल कार्रवाई आवश्यक है।
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              बैकअप विवरण:
            </mj-text>
            <mj-text color="#7f1d1d">
              <strong>बैकअप प्रकार:</strong> {{ backup_type }}<br/>
              <strong>शुरू:</strong> {{ backup_started_at }}<br/>
              <strong>विफल:</strong> {{ backup_failed_at }}<br/>
              <strong>अवधि:</strong> {{ backup_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          त्रुटि विवरण:
        </mj-text>

        <mj-section background-color="#f9fafb" border-radius="4px" padding="15px">
          <mj-column>
            <mj-text font-family="'Courier New', monospace" font-size="13px" color="#dc2626">
              {{ error_message }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          सिफारिश की गई कार्रवाई:
        </mj-text>

        <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
          1. सर्वर पर उपलब्ध डिस्क स्पेस की जांच करें<br/>
          2. डेटाबेस कनेक्टिविटी की पुष्टि करें<br/>
          3. विस्तृत स्टैक ट्रेस के लिए त्रुटि लॉग की समीक्षा करें<br/>
          4. बैकअप को मनमाने तौर पर दोबारा प्रयास करें या अगले निर्धारित चलाने के लिए इंतजार करें<br/>
          5. यदि समस्या बनी रहती है तो समर्थन से संपर्क करें
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          बैकअप लॉग देखें
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ retry_backup_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          अब बैकअप दोबारा प्रयास करें
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>अंतिम सफल बैकअप:</strong> {{ last_successful_backup }}<br/>
          <strong>अगला निर्धारित बैकअप:</strong> {{ next_scheduled_backup }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🚨 आपातकालीन: बैकअप विफल

हेलो {{ admin_name }},

आपके {{ shop_name }} स्टोर के लिए एक महत्वपूर्ण बैकअप संचालन विफल रहा। डेटा सुरक्षा सुनिश्चित करने के लिए तत्काल कार्रवाई आवश्यक है।

बैकअप विवरण:
- बैकअप प्रकार: {{ backup_type }}
- शुरू: {{ backup_started_at }}
- विफल: {{ backup_failed_at }}
- अवधि: {{ backup_duration }}

त्रुटि विवरण:
{{ error_message }}

सिफारिश की गई कार्रवाई:
1. सर्वर पर उपलब्ध डिस्क स्पेस की जांच करें
2. डेटाबेस कनेक्टिविटी की पुष्टि करें
3. विस्तृत स्टैक ट्रेस के लिए त्रुटि लॉग की समीक्षा करें
4. बैकअप को मनमाने तौर पर दोबारा प्रयास करें या अगले निर्धारित चलाने के लिए इंतजार करें
5. यदि समस्या बनी रहती है तो समर्थन से संपर्क करें

बैकअप लॉग देखें: {{ admin_backup_url }}
अब बैकअप दोबारा प्रयास करें: {{ retry_backup_url }}

अंतिम सफल बैकअप: {{ last_successful_backup }}
अगला निर्धारित बैकअप: {{ next_scheduled_backup }}

---
यह {{ shop_name }} प्रशासकों के लिए एक महत्वपूर्ण प्रणाली चेतावनी है।

याद रखें: सभी Django टेम्पलेट सिंटैक्स ({{ }}, {% %}), सभी MJML टैग (<mj-*>), सभी HTML एट्रिब्यूट और सभी इमोजी को संरक्षित करें।