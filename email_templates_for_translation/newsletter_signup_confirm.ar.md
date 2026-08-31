---
template_type: newsletter_signup_confirm
category: Newsletter
---

# Email Template: newsletter_signup_confirm

## Subject
يرجى تأكيد الاشتراك في {{ store_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          تأكيد الاشتراك
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          شكرًا لتسجيلك للحصول على أخبار {{ store_name }}! يرجى تأكيد عنوان بريدك الإلكتروني لبدء تلقي تحديثاتنا وعروضنا.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ confirmation_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          تأكيد الاشتراك
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              لا تستطيع النقر على الزر؟ انسخ وصِق هذا الرابط في متصفحك:
              <br/>
              <span style="color: {{ theme.color.primary|default:'#2563eb' }}; font-family: 'Courier New', monospace;">{{ confirmation_url }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>لماذا يجب التأكيد؟</strong><br/>
          يساعدنا تأكيد بريدك الإلكتروني في التأكد من أنك تريد حقًا تلقي تحديثاتنا، ويحافظ على بريدك الإلكتروني خاليًا من الرسائل العشوائية.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          لم تقم بالتسجيل؟ يمكنك إهمال هذه البريد الإلكتروني بشكل آمن.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
تأكيد الاشتراك في {{ store_name }}

شكرًا لتسجيلك للحصول على أخبار {{ store_name }}! يرجى تأكيد عنوان بريدك الإلكتروني لبدء تلقي تحديثاتنا وعروضنا:

{{ confirmation_url }}

يُساعدنا تأكيد البريد الإلكتروني في التأكد من أنك تريد حقًا تلقي تحديثاتنا، ويحافظ على بريدك الإلكتروني خاليًا من الرسائل العشوائية.

لم تقم بالتسجيل؟ يمكنك إهمال هذه البريد الإلكتروني بشكل آمن.