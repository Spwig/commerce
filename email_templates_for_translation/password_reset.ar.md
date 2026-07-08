---
template_type: password_reset
category: Authentication
---

# Email Template: password_reset

## Subject
طلب إعادة تعيين كلمة المرور

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          طلب إعادة تعيين كلمة المرور
        </mj-text>
        <mj-text>
          تلقينا طلبًا لإعادة تعيين كلمة المرور الخاصة بك. اضغط على الزر أدناه لإعادة تعيينها.
        </mj-text>
        <mj-button href="{{ reset_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          إعادة تعيين كلمة المرور
        </mj-button>
        <mj-text color="#666666" font-size="12px">
          إذا لم تكن قد طلبت هذا، فيمكنك تجاهل هذا البريد الإلكتروني بأمان.
        </mj-text>
        <mj-text color="#666666" font-size="12px">
          سيتم إلغاء هذا الرابط بعد {{ expiry_hours }} ساعات.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
طلب إعادة تعيين كلمة المرور

تلقينا طلبًا لإعادة تعيين كلمة المرور الخاصة بك. اضغط على الرابط أدناه لإعادة تعيينها.

{{ reset_url }}

إذا لم تكن قد طلبت هذا، فيمكنك تجاهل هذا البريد الإلكتروني بأمان. سيتم إلغاء هذا الرابط بعد {{ expiry_hours }} ساعات.