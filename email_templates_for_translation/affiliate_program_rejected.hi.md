---
template_type: affiliate_program_rejected
category: Affiliate Program
---

# Email Template: affiliate_program_rejected

## Subject
अनुप्रयोग अपडेट

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="#f8f9fa">
    <!-- Header -->
    <mj-section background-color="#ffffff" padding="40px 20px">
      <mj-column>
        <mj-text font-size="32px" font-weight="bold" color="#212529" align="center">
          अनुप्रयोग अपडेट
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          हेलो {{ affiliate_name }},
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          {{ program_name }} के लिए आपके अनुप्रयोग के लिए धन्यवाद।
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          आपके अनुप्रयोग की समीक्षा के बाद, हम इसे इस समय मंजूरी देने के लिए निर्णय लिया है।
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          आप अभी भी हमारे अफिलिएट नेटवर्क में अन्य कार्यक्रमों के लिए प्रचार कर सकते हैं।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#6c757d" color="#ffffff" href="{{ portal_url }}">
          अन्य कार्यक्रमों की सूची
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          प्रश्न हैं? <a href="mailto:{{ support_email }}" style="color: #007bff;">
          समर्थन से संपर्क करें</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
अनुप्रयोग अपडेट

हेलो {{ affiliate_name }},

{{ program_name }} के लिए आपके अनुप्रयोग के लिए धन्यवाद।

आपके अनुप्रयोग की समीक्षा के बाद, हम इसे इस समय मंजूरी देने के लिए निर्णय लिया है।

आप अभी भी हमारे अफिलिएट नेटवर्क में अन्य कार्यक्रमों के लिए प्रचार कर सकते हैं।

अन्य कार्यक्रमों की सूची: {{ portal_url }}

{{ shop_name }}
प्रश्न हैं? {{ support_email }} से संपर्क करें
