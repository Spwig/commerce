---
template_type: translation_job_started
category: Translation Service
---

# Email Template: translation_job_started

## Subject
🌐 अनुवाद कार्य शुरू हुआ: {{ content_type }} ({{ source_language }} → {{ target_languages }})

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          🌐 अनुवाद कार्य शुरू हुआ
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          बैच अनुवाद प्रगति में
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          आपका बैच अनुवाद कार्य शुरू हो गया है और अब प्रोसेस कर रहा है।
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              कार्य विवरण:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>कार्य ID:</strong> {{ job_id }}<br/>
              <strong>कंटेंट प्रकार:</strong> {{ content_type }}<br/>
              <strong>मूल भाषा:</strong> {{ source_language }}<br/>
              <strong>लक्ष्य भाषाएं:</strong> {{ target_languages }}<br/>
              <strong>अनुवाद के लिए आइटम:</strong> {{ item_count }}<br/>
              <strong>शुरू हुआ:</strong> {{ started_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          अनुमानित पूर्णता:
        </mj-text>

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" color="#065f46" font-weight="bold" align="center">
              {{ estimated_completion }}
            </mj-text>
            <mj-text font-size="14px" color="#065f46" align="center">
              ({{ word_count }} शब्दों के आधार पर)
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          अगला क्या होता है:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. एआई अनुवाद सेवा आपकी सामग्री को प्रोसेस करती है<br/>
          2. अनुवाद रिव्यू के लिए ड्राफ्ट के रूप में सहेजे जाते हैं<br/>
          3. जब कार्य पूरा हो जाता है तो आपको एक ईमेल प्राप्त होगा<br/>
          4. अपने प्रशासन पैनल से अनुवादों की समीक्षा और प्रकाशित करें
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ job_status_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          कार्य स्थिति देखें
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          आप इस ईमेल को बंद कर सकते हैं। अनुवाद पूरा होने पर हम आपको सूचना देंगे।
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🌐 अनुवाद कार्य शुरू हुआ

बैच अनुवाद प्रगति में

आपका बैच अनुवाद कार्य शुरू हो गया है और अब प्रोसेस कर रहा है।

कार्य विवरण:
- कार्य ID: {{ job_id }}
- कंटेंट प्रकार: {{ content_type }}
- मूल भाषा: {{ source_language }}
- लक्ष्य भाषाएं: {{ target_languages }}
- अनुवाद के लिए आइटम: {{ item_count }}
- शुरू हुआ: {{ started_at }}

अनुमानित पूर्णता:
{{ estimated_completion }}
(शब्दों के आधार पर {{ word_count }})

अगला क्या होता है:
1. एआई अनुवाद सेवा आपकी सामग्री को प्रोसेस करती है
2. अनुवाद रिव्यू के लिए ड्राफ्ट के रूप में सहेजे जाते हैं
3. जब कार्य पूरा हो जाता है तो आपको एक ईमेल प्राप्त होगा
4. अपने प्रशासन पैनल से अनुवादों की समीक्षा और प्रकाशित करें

कार्य स्थिति देखें: {{ job_status_url }}

आप इस ईमेल को बंद कर सकते हैं। अनुवाद पूरा होने पर हम आपको सूचना देंगे।