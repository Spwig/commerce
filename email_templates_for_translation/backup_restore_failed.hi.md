---
template_type: backup_restore_failed
category: Backups
---

# Email Template: backup_restore_failed

## Subject
🚨 गंभीर: बैकअप पुनर्स्थापन विफल - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef2f2">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#dc2626" align="center">
          🚨 गंभीर: बैकअप पुनर्स्थापन विफल
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#1f2937' }}" font-weight="bold">
          हैलो {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          एक गंभीर बैकअप पुनर्स्थापन संचालन विफल रहा। आपका स्टोर एक असंगत अवस्था में हो सकता है और तत्काल ध्यान आवश्यक है।
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              पुनर्स्थापन विवरण:
            </mj-text>
            <mj-text color="#7f1d1d">
              <strong>बैकअप फ़ाइल:</strong> {{ backup_filename }}<br/>
              <strong>शुरू किया गया:</strong> {{ restore_started_at }}<br/>
              <strong>विफल:</strong> {{ restore_failed_at }}<br/>
              <strong>अवधि:</strong> {{ restore_duration }}
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

        <mj-section background-color="#fef3c7" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#92400e">
              🚨 तत्काल कार्रवाई आवश्यक:
            </mj-text>
            <mj-text color="#92400e">
              1. <strong>कोई भी बदलाव न करें</strong> स्टोर में<br/>
              2. डेटाबेस कनेक्टिविटी और अखंडता की जांच करें<br/>
              3. विस्तृत स्टैक ट्रेस के लिए त्रुटि लॉग की जांच करें<br/>
              4. तत्काल तकनीकी समर्थन से संपर्क करें<br/>
              5. पिछले ज्ञात अच्छा अवस्था में वापसी करने की विचार करें
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          पुनर्स्थापन लॉग देखें
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ support_url }}" background-color="#92400e" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          आपातकालीन समर्थन से संपर्क करें
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🚨 गंभीर: बैकअप पुनर्स्थापन विफल

हैलो {{ admin_name }},

एक गंभीर बैकअप पुनर्स्थापन संचालन विफल रहा। आपका स्टोर एक असंगत अवस्था में हो सकता है और तत्काल ध्यान आवश्यक है।

पुनर्स्थापन विवरण:
- बैकअप फ़ाइल: {{ backup_filename }}
- शुरू किया गया: {{ restore_started_at }}
- विफल: {{ restore_failed_at }}
- अवधि: {{ restore_duration }}

त्रुटि विवरण:
{{ error_message }}

🚨 तत्काल कार्रवाई आवश्यक:
1. कोई भी बदलाव न करें स्टोर में
2. डेटाबेस कनेक्टिविटी और अखंडता की जांच करें
3. विस्तृत स्टैक ट्रेस के लिए त्रुटि लॉग की जांच करें
4. तत्काल तकनीकी समर्थन से संपर्क करें
5. पिछले ज्ञात अच्छा अवस्था में वापसी करने की विचार करें

पुनर्स्थापन लॉग देखें: {{ admin_backup_url }}
आपातकालीन समर्थन से संपर्क करें: {{ support_url }}