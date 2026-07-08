---
template_type: email_verification
category: Authentication
---

# Email Template: email_verification

## Subject
ईमेल पता सत्यापित करें

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          ईमेल सत्यापित करें
        </mj-text>
        <mj-text>
          कृपया नीचे दिए गए बटन पर क्लिक करके अपना ईमेल पता सत्यापित करें।
        </mj-text>
        <mj-button href="{{ verification_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          ईमेल सत्यापित करें
        </mj-button>
        <mj-text color="#666666" font-size="12px">
          यह लिंक {{ expiry_hours }} घंटों में अपना जीवन खो देगा।
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
ईमेल सत्यापित करें

कृपया नीचे दिए गए लिंक पर क्लिक करके अपना ईमेल पता सत्यापित करें।

{{ verification_url }}

यह लिंक {{ expiry_hours }} घंटों में अपना जीवन खो देगा।