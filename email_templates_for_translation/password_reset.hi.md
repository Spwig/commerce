---
template_type: password_reset
category: Authentication
---

# Email Template: password_reset

## Subject
पासवर्ड रीसेट के लिए अनुरोध

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          पासवर्ड रीसेट के लिए अनुरोध
        </mj-text>
        <mj-text>
          हमें आपके पासवर्ड को रीसेट करने के लिए एक अनुरोध मिला। नीचे दिए गए बटन पर क्लिक करके इसे रीसेट करें।
        </mj-text>
        <mj-button href="{{ reset_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          पासवर्ड रीसेट करें
        </mj-button>
        <mj-text color="#666666" font-size="12px">
          यदि आपने इस अनुरोध नहीं किया था, तो आप इस ईमेल को अनुचित रूप से अन्य ईमेल के रूप में अनदेखा कर सकते हैं।
        </mj-text>
        <mj-text color="#666666" font-size="12px">
          यह लिंक {{ expiry_hours }} घंटों के बाद अपन अपन रहेगा।
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
पासवर्ड रीसेट के लिए अनुरोध

हमें आपके पासवर्ड को रीसेट करने के लिए एक अनुरोध मिला। नीचे दिए गए लिंक पर क्लिक करके इसे रीसेट करें।

{{ reset_url }}

यदि आपने इस अनुरोध नहीं किया था, तो आप इस ईमेल को अनुचित रूप से अन्य ईमेल के रूप में अनदेखा कर सकते हैं।
यह लिंक {{ expiry_hours }} घंटों के बाद अपन अपन रहेगा।
