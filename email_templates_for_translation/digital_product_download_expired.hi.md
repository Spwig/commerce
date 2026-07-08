---
template_type: digital_product_download_expired
category: Digital Products
---

# Email Template: digital_product_download_expired

## Subject
डाउनलोड लिंक समाप्त - आदेश #{{ order_number }}

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
    <mj-section background-color="{{ theme.color.error|default:'#ef4444' }}" padding="20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          डाउनलोड लिंक समाप्त
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
          आदेश #{{ order_number }} से {{ product_name }} के लिए आपका डाउनलोड लिंक समाप्त हो गया है।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Expired Information -->
    <mj-section background-color="#fef2f2" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="14px" color="#991b1b">
          सुरक्षा के कारण, खरीदारी के {{ expiration_days }} दिन बाद डाउनलोड लिंक समाप्त हो जाता है।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Request New Link -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold">
          एक नया डाउनलोड लिंक की आवश्यकता है?
        </mj-text>
        <mj-text>
          आप अपने खाते में लॉग इन करके या हमारी समर्थन टीम से संपर्क करके एक नया डाउनलोड लिंक अनुरोध कर सकते हैं।
        </mj-text>
        <mj-button href="{{ account_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" padding="15px 30px" border-radius="6px">
          मेरे खाते तक जाएं
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Support -->
    <mj-section>
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          प्रश्न हैं? {{ support_email }} पर संपर्क करें
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
डाउनलोड लिंक समाप्त

हेलो {{ customer_name }},

आदेश #{{ order_number }} से {{ product_name }} के लिए आपका डाउनलोड लिंक समाप्त हो गया है।

डाउनलोड लिंक सुरक्षा के कारण खरीदारी के {{ expiration_days }} दिन बाद समाप्त हो जाता है।

एक नया डाउनलोड लिंक की आवश्यकता है?
आप अपने खाते में लॉग इन करके या हमारी समर्थन टीम से संपर्क करके एक नया डाउनलोड लिंक अनुरोध कर सकते हैं।

मेरे खाते तक जाएं: {{ account_url }}

प्रश्न हैं? {{ support_email }} पर संपर्क करें