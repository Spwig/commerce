---
template_type: backup_restore_completed
category: Backups
---

# Email Template: backup_restore_completed

## Subject
✓ प्रतिलिपि पुनर्स्थापन पूर्ण - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#f0fdf4">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#059669" align="center">
          ✓ प्रतिलिपि पुनर्स्थापन पूर्ण
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          हेलो {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          आपकी प्रतिलिपि पुनर्स्थापन कार्य सफलतापूर्वक पूरा हो गया है। आपके स्टोर डेटा को पुनर्स्थापित कर दिया गया है।
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              पुनर्स्थापन विवरण:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>प्रतिलिपि फ़ाइल:</strong> {{ backup_filename }}<br/>
              <strong>प्रतिलिपि तारीख:</strong> {{ backup_date }}<br/>
              <strong>शुरू करें:</strong> {{ restore_started_at }}<br/>
              <strong>पूर्ण:</strong> {{ restore_completed_at }}<br/>
              <strong>अवधि:</strong> {{ restore_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ महत्वपूर्ण अगले कदम:
            </mj-text>
            <mj-text font-size="14px" color="#92400e">
              1. अपने स्टोर के सही रूप से काम कर रहा है जांच करें<br/>
              2. महत्वपूर्ण डेटा (उत्पाद, आदेश, ग्राहक) की जांच करें<br/>
              3. आवश्यकता हो तो कैश को साफ करें<br/>
              4. महत्वपूर्ण कार्यप्रवाहों (चेकआउट, प्रशासन पहुँच) का परीक्षण करें
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_dashboard_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          प्रशासन डैशबोर्ड पर जाएं
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ प्रतिलिपि पुनर्स्थापन पूर्ण

हेलो {{ admin_name }},

आपकी प्रतिलिपि पुनर्स्थापन कार्य सफलतापूर्वक पूरा हो गया है। आपके स्टोर डेटा को पुनर्स्थापित कर दिया गया है।

पुनर्स्थापन विवरण:
- प्रतिलिपि फ़ाइल: {{ backup_filename }}
- प्रतिलिपि तारीख: {{ backup_date }}
- शुरू करें: {{ restore_started_at }}
- पूर्ण: {{ restore_completed_at }}
- अवधि: {{ restore_duration }}

⚠️ महत्वपूर्ण अगले कदम:
1. अपने स्टोर के सही रूप से काम कर रहा है जांच करें
2. महत्वपूर्ण डेटा (उत्पाद, आदेश, ग्राहक) की जांच करें
3. आवश्यकता हो तो कैश को साफ करें
4. महत्वपूर्ण कार्यप्रवाहों (चेकआउट, प्रशासन पहुँच) का परीक्षण करें

प्रशासन डैशबोर्ड पर जाएं: {{ admin_dashboard_url }}