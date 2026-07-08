---
template_type: affiliate_account_suspended
category: Affiliate Program
---

# Email Template: affiliate_account_suspended

## Subject
Важно: Аккаунт приостановлен

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
        <mj-text font-size="32px" font-weight="bold" color="#dc3545" align="center">
          Аккаунт приостановлен
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          Здравствуйте, {{ affiliate_name }},
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Ваш аккаунт аффилиат-программы {{ shop_name }} был приостановлен.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Обычно это происходит из-за нарушения условий и положений нашей аффилиат-программы.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Если вы считаете, что это ошибка, или хотите обсудить это решение, пожалуйста, свяжитесь с нашей службой поддержки.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          Вопросы? <a href="mailto:{{ support_email }}" style="color: #007bff;">Связаться с поддержкой</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Важно: Аккаунт приостановлен

Здравствуйте, {{ affiliate_name }},

Ваш аккаунт аффилиат-программы {{ shop_name }} был приостановлен.

Обычно это происходит из-за нарушения условий и положений нашей аффилиат-программы.

Если вы считаете, что это ошибка, или хотите обсудить это решение, пожалуйста, свяжитесь с нашей службой поддержки.

{{ shop_name }}
Вопросы? Связаться с {{ support_email }}