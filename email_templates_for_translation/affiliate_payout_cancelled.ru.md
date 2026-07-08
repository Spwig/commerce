---
template_type: affiliate_payout_cancelled
category: Affiliate Program
---

# Email Template: affiliate_payout_cancelled

## Subject
Выплата отменена - {{ payout_amount }}

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
          Выплата отменена
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
          Ваша выплата в размере {{ payout_amount }} (ID выплаты: {{ payout_id }}) была отменена.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Если у вас есть вопросы по поводу отмены этой выплаты, пожалуйста, свяжитесь с нашей службой поддержки.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#6c757d" color="#ffffff" href="{{ portal_url }}">
          Перейти к панели аффилиатов
        </mj-button>
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
Выплата отменена - {{ payout_amount }}

Здравствуйте, {{ affiliate_name }},

Ваша выплата в размере {{ payout_amount }} (ID выплаты: {{ payout_id }}) была отменена.

Если у вас есть вопросы по поводу отмены этой выплаты, пожалуйста, свяжитесь с нашей службой поддержки.

Посмотреть панель: {{ portal_url }}

{{ shop_name }}
Вопросы? Свяжитесь с {{ support_email }}