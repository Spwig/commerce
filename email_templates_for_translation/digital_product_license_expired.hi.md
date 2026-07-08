---
template_type: digital_product_license_expired
category: Digital Products
---

# Email Template: digital_product_license_expired

## Subject
लाइसेंस कुंजी जल्दी खत्म हो रही है - {{ product_name }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.warning|default:'#f59e0b' }}" padding="20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          लाइसेंस जल्दी खत्म हो रही है
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Main Content -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          हेलो {{ customer_name }},
        </mj-text>
        <mj-text>
          आपका {{ product_name }} के लिए लाइसेंस जल्दी खत्म हो जाएगा।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- License Details -->
    <mj-section background-color="#fffbeb" padding="20px" border="2px solid {{ theme.color.warning|default:'#f59e0b' }}" border-radius="8px">
      <mj-column>
        <mj-text font-size="14px" color="#92400e">
          <strong>लाइसेंस कुंजी:</strong> {{ license_key }}
        </mj-text>
        <mj-text font-size="14px" color="#92400e">
          <strong>खत्म होता है:</strong> {{ expiration_date }}
        </mj-text>
        <mj-text font-size="14px" color="#92400e">
          <strong>बचे हुए दिन:</strong> {{ days_remaining }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Renewal -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold">
          अपना लाइसेंस नवीनीकरण करें
        </mj-text>
        <mj-text>
          आज अपने लाइसेंस के नवीनीकरण करके {{ product_name }} का आनंद लाएं।
        </mj-text>
        <mj-button href="{{ renewal_url }}" background-color="{{ theme.color.warning|default:'#f59e0b' }}" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" padding="15px 30px" border-radius="6px">
          अब नवीनीकरण करें
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Support -->
    <mj-section>
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          नवीनीकरण के बारे में प्रश्न? {{ support_email }} पर संपर्क करें
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
लाइसेंस जल्दी खत्म हो रहा है

हेलो {{ customer_name }},

आपका {{ product_name }} के लिए लाइसेंस जल्दी खत्म हो जाएगा।

लाइसेंस विवरण:
• लाइसेंस कुंजी: {{ license_key }}
• खत्म होता है: {{ expiration_date }}
• बचे हुए दिन: {{ days_remaining }}

अपना लाइसेंस नवीनीकरण करें:
आज अपने लाइसेंस के नवीनीकरण करके {{ product_name }} का आनंद लाएं।

अब नवीनीकरण करें: {{ renewal_url }}

नवीनीकरण के बारे में प्रश्न? {{ support_email }} पर संपर्क करें