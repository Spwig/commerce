---
template_type: backup_storage_quota_alert
category: Backups
---

# Email Template: backup_storage_quota_alert

## Subject
🚨 संग्रहण अनुमान चिन्ह गंभीर - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef2f2">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#dc2626" align="center">
          🚨 संग्रहण अनुमान गंभीर
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          हेलो {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>आवश्यक:</strong> आपका संग्रहण अनुमान बहुत कम है। यदि संग्रहण जगह खाली नहीं करते हैं, तो भविष्य के संग्रहण विफल हो सकते हैं।
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              संग्रहण स्थिति:
            </mj-text>
            <mj-text color="#7f1d1d">
              <strong>प्रयोग:</strong> {{ storage_used }} of {{ storage_total }}<br/>
              <strong>उपयोग:</strong> {{ storage_percentage }}%<br/>
              <strong>उपलब्ध:</strong> {{ storage_available }}<br/>
              <strong>स्थिति:</strong> <span style="color: #dc2626; font-weight: bold;">{{ storage_status }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="#fef3c7" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#92400e">
              तत्काल कार्रवाई आवश्यक:
            </mj-text>
            <mj-text color="#92400e">
              1. उन पुराने संग्रहण को हटाएं जो आवश्यक नहीं हैं<br/>
              2. संग्रहण को बाहरी संग्रहण में आर्काइव करें<br/>
              3. संग्रहण अनुमान / क्षमता बढ़ाएं<br/>
              4. संग्रहण अनुमान नीति की समीक्षा करें<br/>
              5. समाधान तक प्रतिदिन संग्रहण की निगरानी करें
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          अब संग्रहण का प्रबंधन करें
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🚨 संग्रहण अनुमान गंभीर

हेलो {{ admin_name }},

आवश्यक: आपका संग्रहण अनुमान बहुत कम है। यदि संग्रहण जगह खाली नहीं करते हैं, तो भविष्य के संग्रहण विफल हो सकते हैं।

संग्रहण स्थिति:
- प्रयोग: {{ storage_used }} of {{ storage_total }}
- उपयोग: {{ storage_percentage }}%
- उपलब्ध: {{ storage_available }}
- स्थिति: {{ storage_status }}

तत्काल कार्रवाई आवश्यक:
1. उन पुराने संग्रहण को हटाएं जो आवश्यक नहीं हैं
2. संग्रहण को बाहरी संग्रहण में आर्काइव करें
3. संग्रहण अनुमान / क्षमता बढ़ाएं
4. संग्रहण अनुमान नीति की समीक्षा करें
5. समाधान तक प्रतिदिन संग्रहण की निगरानी करें

अब संग्रहण का प्रबंधन करें: {{ admin_backup_url }}