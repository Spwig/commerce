---
template_type: backup_scheduled_missed
category: Backups
---

# Email Template: backup_scheduled_missed

## Subject
⚠️ नियोजित बैकअप चला नहीं - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ नियोजित बैकअप चला नहीं
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          हेलो {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ shop_name }} के लिए एक नियोजित बैकअप अपेक्षित रूप से चला नहीं। आपके डेटा पूरी तरह से सुरक्षित नहीं हो सकता।
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              बैकअप नियोजन विवरण:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>नियोजित समय:</strong> {{ scheduled_time }}<br/>
              <strong>बैकअप प्रकार:</strong> {{ backup_type }}<br/>
              <strong>अंतिम सफल बैकअप:</strong> {{ last_successful_backup }}<br/>
              <strong>अंतिम बैकअप से बीता समय:</strong> {{ time_since_last }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          संभावित कारण:
        </mj-text>

        <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
          • सर्वर ऑफ़लाइन या अप्रोचेबल था<br/>
          • नियोजित कार्य सेवा चल रही नहीं है<br/>
          • अपर्याप्त अनुमति<br/>
          • संग्रहण स्थान भर गया<br/>
          • डेटाबेस कनेक्टिविटी समस्याएं
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          मनमाने मोड में बैकअप चलाएं
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ admin_logs_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          सिस्टम लॉग देखें
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ नियोजित बैकअप चला नहीं

हेलो {{ admin_name }},

{{ shop_name }} के लिए एक नियोजित बैकअप अपेक्षित रूप से चला नहीं। आपके डेटा पूरी तरह से सुरक्षित नहीं हो सकता।

बैकअप नियोजन विवरण:
- नियोजित समय: {{ scheduled_time }}
- बैकअप प्रकार: {{ backup_type }}
- अंतिम सफल बैकअप: {{ last_successful_backup }}
- अंतिम बैकअप से बीता समय: {{ time_since_last }}

संभावित कारण:
• सर्वर ऑफ़लाइन या अप्रोचेबल था
• नियोजित कार्य सेवा चल रही नहीं है
• अपर्याप्त अनुमति
• संग्रहण स्थान भर गया
• डेटाबेस कनेक्टिविटी समस्याएं

मनमाने मोड में बैकअप चलाएं: {{ admin_backup_url }}
सिस्टम लॉग देखें: {{ admin_logs_url }}

