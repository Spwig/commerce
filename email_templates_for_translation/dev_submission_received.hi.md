---
template_type: dev_submission_received
category: Developer Portal
---

# Email Template: dev_submission_received

## Subject
कम्पोनेंट उपलब्धता प्राप्त: {{ component_name }} v{{ version }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          उपलब्धता प्राप्त
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          आपका कम्पोनेंट अब समीक्षा के लिए है
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          हेलो {{ developer_name }},
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-top="20px">
          हमने आपके कम्पोनेंट की उपलब्धता प्राप्त की है और यह स्वचालित जांच के माध्यम से स्वीकृत हो गया है। हमारी टीम अब इसकी समीक्षा करेगी।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Component Details -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="25px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="8px">
          <strong>कम्पोनेंट:</strong> {{ component_name }}
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="8px">
          <strong>प्रकार:</strong> {{ component_type }}
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>संस्करण:</strong> v{{ version }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Timeline Info -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="25px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          समीक्षा आमतौर पर 2-3 व्यावसायिक दिन लेती है। जब हमारी समीक्षा पूरी हो जाएगी, तो आपको सूचना दी जाएगी।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Button -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ submission_url }}" border-radius="6px" font-size="16px" font-weight="bold" padding="15px 30px">
          उपलब्धता देखें
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" padding-bottom="20px"></mj-divider>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          <strong>Spwig डेवलपर पोर्टल</strong>
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          प्रश्न हैं? डेवलपर समर्थन से संपर्क करें
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
हेलो {{ developer_name }},

हमने आपके कम्पोनेंट की उपलब्धता प्राप्त की है और यह स्वचालित जांच के माध्यम से स्वीकृत हो गया है। हमारी टीम अब इसकी समीक्षा करेगी।

कम्पोनेंट: {{ component_name }}
प्रकार: {{ component_type }}
संस्करण: v{{ version }}

समीक्षा आमतौर पर 2-3 व्यावसायिक दिन लेती है। जब हमारी समीक्षा पूरी हो जाएगी, तो आपको सूचना दी जाएगी।

उपलब्धता देखें: {{ submission_url }}

---
Spwig डेवलपर पोर्टल