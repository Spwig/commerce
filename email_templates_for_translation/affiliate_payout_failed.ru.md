---
template_type: affiliate_payout_failed
category: Affiliate Program
---

# Email Template: affiliate_payout_failed

## Subject
Действие требуется: Неудачный вывод средств

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
          ⚠️ Неудачный вывод средств
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Warning Display -->
    <mj-section background-color="#fff3cd" padding="40px 20px">
      <mj-column>
        <mj-text font-size="48px" font-weight="bold" color="#856404" align="center" line-height="1">
          {{ payout_amount }}
        </mj-text>
        <mj-text font-size="16px" color="#856404" align="center" padding-top="10px">
          Идентификатор вывода средств: {{ payout_id }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          Здравствуйте {{ affiliate_name }},
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Мы столкнулись с проблемой при обработке вашего вывода средств в размере {{ payout_amount }}.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Это обычно связано с неправильной информацией о платеже или проблемой с вашим платежным провайдером.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Пожалуйста, обновите информацию о платеже в вашем дашборде аффилиатов и свяжитесь с нашей службой поддержки, чтобы решить эту проблему.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#dc3545" color="#ffffff" href="{{ portal_url }}">
          Обновить информацию о платеже
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          Нужна помощь? <a href="mailto:{{ support_email }}" style="color: #007bff;">Свяжитесь с поддержкой</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Действие требуется: Неудачный вывод средств

Здравствуйте {{ affiliate_name }},

Мы столкнулись с проблемой при обработке вашего вывода средств в размере {{ payout_amount }} (Идентификатор вывода средств: {{ payout_id }}).

Это обычно связано с неправильной информацией о платеже или проблемой с вашим платежным провайдером.

Пожалуйста, обновите информацию о платеже в вашем дашборде аффилиатов и свяжитесь с нашей службой поддержки, чтобы решить эту проблему.

Обновить информацию о платеже: {{ portal_url }}

{{ shop_name }}
Нужна помощь? Свяжитесь с {{ support_email }}