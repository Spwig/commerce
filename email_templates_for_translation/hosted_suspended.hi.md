---
template_type: hosted_suspended
category: License
---

# Email Template: hosted_suspended

## Subject
स्टोर बंद - {{ store_name }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="#dc2626" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          खाता बंद कर दिया गया है
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          हेलो {{ name|default:'there' }},
        </mj-text>
        <mj-text>
          आपका स्टोर <strong>{{ store_name }}</strong> अदेखा बिलिंग के कारण बंद कर दिया गया है।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What This Means -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          यह क्या दर्शाता है
        </mj-text>
        <mj-text font-size="14px">
          अब आपका स्टोर केवल पढ़ने के लिए उपलब्ध है - ग्राहक ब्राउज़ कर सकते हैं लेकिन ऑर्डर अक्टूबर के लिए बंद हैं। आपके डेटा सुरक्षित है और 30 दिनों तक संरक्षित रहेगा।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Reactivate -->
    <mj-section>
      <mj-column>
        <mj-text>
          पूर्ण पहुँच को पुनः जोड़ने के लिए, कृपया अपनी भुगतान विधि को अपडेट करें और बचे हुए बैलेंस को जमा करें।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="Reactivate Your Store" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
खाता बंद - {{ store_name }}

हेलो {{ name|default:'there' }},

आपका स्टोर {{ store_name }} अदेखा बिलिंग के कारण बंद कर दिया गया है।

यह क्या दर्शाता है:
आपका स्टोर अब केवल पढ़ने के लिए उपलब्ध है - ग्राहक ब्राउज़ कर सकते हैं लेकिन ऑर्डर अक्टूबर के लिए बंद हैं। आपके डेटा सुरक्षित है और 30 दिनों तक संरक्षित रहेगा।

पूर्ण पहुँच को पुनः जोड़ने के लिए, कृपया अपनी भुगतान विधि को अपडेट करें और बचे हुए बैलेंस को जमा करें।

आपका स्टोर पुनः शुरू करें: https://spwig.com/account

मदद की आवश्यकता है? {{ support_email }} पर संपर्क करें