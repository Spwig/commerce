---
template_type: email_verification
category: Authentication
---

# Email Template: email_verification

## Subject
تأكيد بريدك الإلكتروني

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          تأكيد بريدك الإلكتروني
        </mj-text>
        <mj-text>
          يرجى تأكيد بريدك الإلكتروني بالنقر على الزر أدناه.
        </mj-text>
        <mj-button href="{{ verification_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          تأكيد البريد
        </mj-button>
        <mj-text color="#666666" font-size="12px">
          سيتم إلغاء هذا الرابط بعد {{ expiry_hours }} ساعات.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
تأكيد بريدك الإلكتروني

يرجى تأكيد بريدك الإلكتروني بالنقر على الرابط أدناه.

{{ verification_url }}

سيتم إلغاء هذا الرابط بعد {{ expiry_hours }} ساعات.